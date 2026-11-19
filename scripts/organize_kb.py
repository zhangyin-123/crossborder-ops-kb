"""Import local inbox Markdown as drafts and rebuild the human-readable index."""
import argparse
import fcntl
import hashlib
import os
import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

from kb_core import FIELDS, ROOT, SLUG, encode_card, fold, inventory, issues
from kb_core import split_card, today, within_repo

PLATFORMS = {
    "tiktok-shop": r"tik\s*tok|抖音跨境",
    "amazon": r"amazon|亚马逊",
    "shopee": r"shopee|虾皮",
    "lazada": r"lazada|来赞达",
    "shopify": r"shopify",
    "temu": r"\btemu\b|拼多多跨境",
    "ebay": r"\bebay\b",
}
TOPICS = {
    "inventory": r"库存|补货|断货|inventory|restock|stock alert",
    "fulfillment": r"履约|物流|发货|运单|仓库|fulfill?ment|shipping|delivery|warehouse",
    "after-sales": r"售后|退货|退款|return[s ]|refund",
    "listing": r"商品详情|商品标题|上架|listing|product description",
    "marketing": r"营销|促销|优惠券|投放|广告|marketing|advertising|campaign|voucher",
    "affiliate": r"联盟|达人|affiliate|creator",
    "analytics": r"数据分析|指标|报表|analytics|metrics|report",
    "policy": r"政策|规则|合规|policy|policies|compliance",
    "storefront": r"店铺装修|店面|storefront",
}
MARKETS = {
    "UK": r"英国|英区|\bunited kingdom\b|\bgreat britain\b",
    "MY": r"马来西亚|马来站|马区|\bmalaysia\b",
    "US": r"美国|美区|\busa\b|\bunited states\b",
}


def inferred(text, rules):
    for key, pattern in rules.items():
        if re.search(pattern, text, re.I):
            return key
    return ""


def market_from(title, stem, body):
    for text in (title, stem, body):
        # Lowercase "my" and "us" are ordinary words in English prose.
        markets = [code for code, pattern in MARKETS.items()
                   if re.search(pattern, text, re.I)
                   or re.search(rf"(?<![A-Za-z]){code}(?![A-Za-z])", text)]
        if markets:
            return ", ".join(markets)
    return ""


def prepare(path, raw):
    incoming, body = split_card(raw)
    heading = re.search(r"^#\s+(.+)$", body, re.M)
    title = incoming.get("title") or (heading.group(1).strip() if heading else "")
    source = incoming.get("source", "")
    if not source:
        label = re.search(r"^(?:[-*]\s*)?(?:原始来源|来源链接|来源|source)\s*[：:]\s*(.+)$", body, re.I | re.M)
        if label:
            value = label.group(1).strip()
            link = re.search(r"https?://[^\s)>\]]+", value)
            source = link.group() if link else value
        else:
            link = re.search(r"\[(?:原始来源|来源|source)\]\((https?://[^\s)]+)\)", body, re.I)
            source = link.group(1) if link else ""
    # Prefer the title, since an example in the body can refer to another market or topic.
    hints = [fold(title), fold(path.stem), fold(body)]
    meta = {key: incoming.get(key, "") for key in FIELDS}
    for key, rules in (("platform", PLATFORMS), ("topic", TOPICS)):
        if not meta[key]:
            meta[key] = next((guess for hint in hints if (guess := inferred(hint, rules))), "")
    meta.update(title=title or path.stem, source=source, status="draft")
    if not meta["platform"]:
        meta["platform"] = "unclassified"
    if not title or not source or not meta["topic"]:
        meta["topic"] = "needs-review"
    if not meta["market"]:
        meta["market"] = market_from(title, path.stem, body) or "待补"
    if not meta["id"]:
        prefix = re.sub(r"[^a-z0-9]+", "-", fold(path.stem)).strip("-")[:55].rstrip("-")
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
        meta["id"] = f"{prefix or 'note'}-{digest}"
    for key in ("id", "topic", "platform"):
        if not SLUG.fullmatch(meta[key]):
            raise ValueError(f"{key} 含无效字符")
    if not body.strip():
        raise ValueError("文档无正文，已保留在 inbox")
    return meta, body


def target(meta):
    return within_repo(ROOT / "knowledge" / meta["platform"] / meta["topic"] / (meta["id"] + ".md"))


def atomic_write(path, content, *, replace):
    within_repo(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".kb-", delete=False,
                                     mode="w", encoding="utf-8") as temp:
        temp_path = Path(temp.name)
        try:
            temp.write(content)
            temp.flush()
            os.fsync(temp.fileno())
        except BaseException:
            temp_path.unlink()
            raise
    try:
        if replace:
            os.replace(temp_path, path)
        else:
            # The target is published whole and an existing file is never overwritten.
            os.link(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)


def import_one(path, by_id):
    raw = within_repo(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    stamp = within_repo(ROOT / "inbox" / ".kb-imported" / digest)
    # The local inbox is retained. A repeated run must not undo subsequent manual edits.
    if stamp.is_file():
        known_id = stamp.read_text(encoding="utf-8").strip()
        if known_id in by_id:
            return False
    meta, body = prepare(path, raw.decode("utf-8-sig"))
    base_id = meta["id"]
    attempt = 0
    while True:
        file = target(meta)
        value = dict(meta, body=body.strip(), path=file.relative_to(ROOT).as_posix())
        invalid = issues(value)
        if invalid:
            raise ValueError("，".join(invalid))
        previous = by_id.get(meta["id"])
        if previous is None and not file.exists():
            atomic_write(file, encode_card(meta, body), replace=False)
            by_id[meta["id"]] = value
            added = True
            break
        if previous and all(previous[k] == value[k] for k in
                            ("title", "body", "source", "platform", "topic", "market",
                             "effective", "expires", "tags")):
            added = False
            break
        attempt += 1
        suffix = digest[:12] if attempt == 1 else f"{digest[:12]}-{attempt}"
        meta["id"] = f"{base_id}-{suffix}"
    atomic_write(stamp, meta["id"] + "\n", replace=True)
    return added


def index_text(records):
    groups = defaultdict(list)
    for row in records:
        groups[(row["platform"], row["topic"])].append(row)
    lines = ["# 跨境电商知识索引", "",
             "按平台和主题浏览。对外答复只引用已生效且仍在有效期内的 approved 资料。", ""]
    if not records:
        lines.extend(["当前没有知识卡片。", ""])
    day = today()
    for (platform, topic), cards in sorted(groups.items()):
        lines += [f"## {platform} / {topic}", ""]
        for row in sorted(cards, key=lambda r: (r["title"], r["id"])):
            state = row["status"]
            if state == "approved" and row["expires"] and row["expires"] < day:
                state += "（已到期）"
            elif state == "approved" and row["effective"] and row["effective"] > day:
                state += "（尚未生效）"
            title = row["title"].replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
            file = Path(row["path"]).relative_to("knowledge").as_posix()
            lines.append(f"- [{title}]({file}) · {state} · {row['market'] or '地区待补'}"
                         f" · 核对 {row['checked'] or '待补'}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run(index_only):
    records, problems = inventory()
    if problems:
        raise ValueError("已有知识卡片结构异常，请先运行 validate_kb.py：\n" + "\n".join(problems))
    by_id = {r["id"]: r for r in records}
    added = 0
    errors = []
    inbox = within_repo(ROOT / "inbox")
    if not index_only and inbox.is_dir():
        for path in sorted(inbox.rglob("*.md")):
            if any(part.startswith(".") for part in path.relative_to(inbox).parts):
                continue
            try:
                added += import_one(path, by_id)
            except (OSError, ValueError) as exc:
                errors.append(f"{path.relative_to(ROOT)}：{exc}")
    index = within_repo(ROOT / "knowledge" / "INDEX.md")
    content = index_text(by_id.values())
    if not index.exists() or index.read_text(encoding="utf-8") != content:
        atomic_write(index, content, replace=True)
    print(f"新增草稿 {added} 张，索引共 {len(by_id)} 张。")
    for error in errors:
        print(error, file=sys.stderr)
    return int(bool(errors))


def main():
    parser = argparse.ArgumentParser(description="将 inbox 中的 Markdown 整理为草稿并刷新索引。")
    parser.add_argument("--index-only", action="store_true", help="仅重建索引")
    args = parser.parse_args()
    # Lock the directory itself, so no lock file must be created or removed.
    fd = os.open(ROOT, os.O_RDONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        return run(args.index_only)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    finally:
        os.close(fd)


if __name__ == "__main__":
    raise SystemExit(main())
