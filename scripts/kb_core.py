"""Read and search Markdown knowledge cards using the Python standard library."""
import io
import json
import os
import re
import subprocess
import unicodedata
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ("id", "title", "platform", "market", "topic", "status", "source",
          "checked", "effective", "expires", "tags")
STATES = ("approved", "draft", "expired", "withdrawn")
SLUG = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*\Z")


def today():
    return datetime.now(timezone(timedelta(hours=8))).date().isoformat()


def split_card(text):
    lines = text.lstrip("\ufeff").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text.lstrip("\ufeff")
    closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if closing is None:
        raise ValueError("卡头缺少结束分隔线 ---")
    meta = {}
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.rstrip("\r\n").partition(":")
        if not sep or not re.fullmatch(r"[a-z][a-z0-9_]*", key) or key in meta:
            raise ValueError("卡头字段格式错误或字段重复")
        value = value.strip()
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except ValueError as exc:
                raise ValueError("卡头双引号字符串有误") from exc
        elif value.startswith("'"):
            if len(value) < 2 or not value.endswith("'"):
                raise ValueError("卡头单引号未闭合")
            value = value[1:-1].replace("''", "'")
        if not isinstance(value, str) or any(ord(char) < 32 for char in value):
            raise ValueError("卡头字段须为单行字符串")
        meta[key] = value
    return meta, "".join(lines[closing + 1:]).strip()


def encode_card(meta, body):
    head = "\n".join(f"{key}: {json.dumps(meta[key], ensure_ascii=False)}" for key in FIELDS)
    return f"---\n{head}\n---\n\n{body.strip()}\n"


def within_repo(path):
    """Refuse symlinks, including links in parent directories."""
    rel = path.relative_to(ROOT)
    current = ROOT
    for part in rel.parts:
        if part in ("..", "."):
            raise ValueError("不允许上级路径")
        current = current / part
        if current.is_symlink():
            raise ValueError("不读取或写入符号链接")
    return path


def card_paths():
    base = within_repo(ROOT / "knowledge")
    if not base.is_dir():
        return []
    return sorted(p for p in base.rglob("*.md") if p != base / "INDEX.md")


def published_files():
    """Read one immutable main snapshot. Never fall back to HEAD or disk files."""
    if not (ROOT / ".git").exists():
        return {}
    def git(*args, data=None):
        command = ["git", "--no-replace-objects", "--git-dir", str(ROOT / ".git"), *args]
        env = dict(os.environ, GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0")
        try:
            result = subprocess.run(command, input=data, capture_output=True, cwd=ROOT, env=env)
        except OSError as exc:
            raise ValueError("无法读取 Git 主线") from exc
        if result.returncode:
            raise ValueError("无法读取 Git 主线对象，请检查本地仓库")
        return result.stdout

    upstream, local = b"refs/remotes/origin/main", b"refs/heads/main"
    refs = git("for-each-ref", "--format=%(refname) %(objectname)", upstream, local)
    commits = dict(line.split() for line in refs.splitlines())
    commit = commits.get(upstream) or commits.get(local)
    if not commit:
        return {}
    paths = []
    for entry in git("ls-tree", "-r", "-z", commit, "--", "knowledge").split(b"\0"):
        if not entry:
            continue
        info, name = entry.split(b"\t", 1)
        mode, kind, oid = info.split()
        if mode not in (b"100644", b"100755") or kind != b"blob":
            continue
        if name.endswith(b".md") and name != b"knowledge/INDEX.md":
            paths.append((os.fsdecode(name), oid))
    if not paths:
        return {}
    # One cat-file invocation for all cards, regardless of collection size.
    blobs = io.BytesIO(git("cat-file", "--batch", data=b"".join(oid + b"\n" for _, oid in paths)))
    snapshot = {}
    for name, expected in paths:
        header = blobs.readline().split()
        if len(header) != 3 or header[:2] != [expected, b"blob"]:
            raise ValueError("Git 主线知识卡片对象不完整")
        size = int(header[2])
        content = blobs.read(size)
        if len(content) != size or blobs.read(1) != b"\n":
            raise ValueError("Git 主线知识卡片读取不完整")
        snapshot[name] = content
    return snapshot


def issues(record):
    errors = []
    for key in FIELDS:
        if key not in record:
            errors.append(f"缺少字段 {key}")
    for key in ("id", "platform", "topic"):
        if not SLUG.fullmatch(record.get(key, "")):
            errors.append(f"{key} 需为小写 slug")
    if not record.get("title", "").strip() or not record.get("body", "").strip():
        errors.append("缺少标题或正文")
    state = record.get("status", "")
    if state not in STATES:
        errors.append("无效状态")
    if state == "approved":
        for key in ("market", "source", "checked"):
            if record.get(key, "").strip().casefold() in ("", "unknown", "pending", "待补", "待确认"):
                errors.append(f"已审核条目需补充 {key}")
    for key in ("checked", "effective", "expires"):
        value = record.get(key, "")
        if value:
            try:
                if date.fromisoformat(value).isoformat() != value:
                    raise ValueError
            except ValueError:
                errors.append(f"{key} 需为 YYYY-MM-DD")
    if record.get("effective") and record.get("expires") and record["effective"] > record["expires"]:
        errors.append("生效日期晚于截止日期")
    parts = [record.get(k, "") for k in ("platform", "topic", "id")]
    if record["path"] != f"knowledge/{parts[0]}/{parts[1]}/{parts[2]}.md":
        errors.append("文件路径与 platform/topic/id 不符")
    return errors


def inventory(snapshot=None):
    records, errors = [], []
    seen = Counter()
    paths = ([p.relative_to(ROOT).as_posix() for p in card_paths()]
             if snapshot is None else snapshot.keys())
    for path in paths:
        try:
            content = within_repo(ROOT / path).read_bytes() if snapshot is None else snapshot[path]
            meta, body = split_card(content.decode("utf-8"))
            record = dict(meta, body=body, path=path)
            if record.get("id"):
                seen[record["id"]] += 1
            invalid = issues(record)
            if invalid:
                errors.append(f"{path}：{'，'.join(invalid)}")
            else:
                records.append(record)
        except (OSError, ValueError) as exc:
            errors.append(f"{path}：{exc}")
    duplicate = {key for key, count in seen.items() if count > 1}
    for key in sorted(duplicate):
        errors.append(f"重复 id：{key}")
    return [r for r in records if r["id"] not in duplicate], errors


def available(status):
    if status not in STATES:
        raise ValueError("无效状态")
    day = today()
    records, _ = inventory(published_files()) if status == "approved" else inventory()
    for record in records:
        state = record["status"]
        if state == "approved" and record["expires"] and record["expires"] < day:
            state = "expired"
        if state != status:
            continue
        if status == "approved" and record["effective"] and record["effective"] > day:
            continue
        if state != record["status"]:
            record = dict(record, status=state, recorded_status=record["status"])
        yield record


def fold(text):
    return unicodedata.normalize("NFKC", text).casefold()


def search(query, status="approved", limit=10):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("请输入搜索词")
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("limit 需为 1 至 100 的整数")
    phrase = fold(query).strip()
    terms = list(dict.fromkeys(re.findall(r"[\w-]+", phrase)))
    if not terms:
        raise ValueError("请输入有效搜索词")
    matches = []
    for record in available(status):
        fields = [(fold(record[k]), w) for k, w in
                  (("title", 10), ("tags", 7), ("market", 5), ("platform", 4),
                   ("topic", 4), ("id", 3), ("body", 1))]
        scores = [sum(w for content, w in fields if term in content) for term in terms]
        if all(scores):
            score = sum(scores) + sum(w for content, w in fields if phrase in content)
            matches.append((score, record))
    matches.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [{k: v for k, v in record.items() if k != "body"} for _, record in matches[:limit]]


def read_card(id, status="approved"):
    if not isinstance(id, str) or not SLUG.fullmatch(id):
        raise ValueError("无效卡片 id")
    for record in available(status):
        if record["id"] == id:
            return record
    raise KeyError(id)
