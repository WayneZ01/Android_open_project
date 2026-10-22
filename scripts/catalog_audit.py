#!/usr/bin/env python3
"""Audit the size and structure of the curated Android catalog."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

EXTERNAL_LINK = re.compile(r"\[[^\]]+\]\((https?://[^)\s]+)\)")
CATEGORY = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)


def audit(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    links = EXTERNAL_LINK.findall(text)
    categories = CATEGORY.findall(text)
    counts = Counter(links)
    duplicates = sorted(url for url, count in counts.items() if count > 1)
    return {
        "file": str(path),
        "links": len(links),
        "unique_links": len(counts),
        "categories": len(categories),
        "duplicate_urls": duplicates,
    }


def write_summary(result: dict[str, object]) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    duplicates = result["duplicate_urls"]
    lines = [
        "## Catalog audit",
        "",
        f"- Links: **{result['links']}**",
        f"- Unique links: **{result['unique_links']}**",
        f"- Categories: **{result['categories']}**",
        f"- Duplicate URLs: **{len(duplicates)}**",
    ]
    if duplicates:
        lines.extend(["", "### Duplicate URLs", ""])
        lines.extend(f"- `{url}`" for url in duplicates)
    with open(summary_path, "a", encoding="utf-8") as summary:
        summary.write("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--min-links", type=int, default=0)
    parser.add_argument("--min-categories", type=int, default=0)
    parser.add_argument("--max-duplicates", type=int, default=0)
    args = parser.parse_args()

    result = audit(args.catalog)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    write_summary(result)

    failures: list[str] = []
    if result["links"] < args.min_links:
        failures.append(f"expected at least {args.min_links} links")
    if result["categories"] < args.min_categories:
        failures.append(f"expected at least {args.min_categories} categories")
    if len(result["duplicate_urls"]) > args.max_duplicates:
        failures.append(f"expected at most {args.max_duplicates} duplicate URLs")

    if failures:
        print("Catalog audit failed: " + "; ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
