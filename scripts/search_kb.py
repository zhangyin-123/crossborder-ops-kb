"""Search vetted cards, or explicitly select an editorial status."""
import argparse
import json
from kb_core import STATES, search


def main():
    parser = argparse.ArgumentParser(description="按多个关键词检索知识卡片，默认只返回当前有效的已批准资料。")
    parser.add_argument("query", nargs="+", help="关键词，用空格分开")
    parser.add_argument("--status", choices=STATES, default="approved")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        rows = search(" ".join(args.query), args.status, args.limit)
    except ValueError as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif not rows:
        print("知识库暂无经审核依据" if args.status == "approved" else "没有符合条件的条目")
    else:
        for row in rows:
            print(f"[{row['status']}] {row['title']}  ·  {row['path']}")
            print(f"  地区 {row['market'] or '待补'}  核对 {row['checked'] or '待补'}"
                  f"  生效 {row['effective'] or '未注明'}  来源 {row['source'] or '待补'}")


if __name__ == "__main__":
    main()
