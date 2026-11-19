"""Validate the structure of every knowledge card, including drafts."""
import sys
from kb_core import inventory


def main():
    try:
        records, problems = inventory()
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 1
    print(f"结构校验通过，共 {len(records)} 张知识卡片。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
