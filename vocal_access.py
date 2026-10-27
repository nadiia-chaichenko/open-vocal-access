"""A small, dependency-free discovery tool for classical vocal repertoire.

Educational repertoire metadata; classifications are indicative, not casting rules.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

CATALOGUE = Path(__file__).parent / "data" / "repertoire.csv"


def load_catalogue(path: Path = CATALOGUE) -> list[dict[str, str]]:
    """Load the CSV catalogue without requiring third-party packages."""
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def search_repertoire(
    catalogue: list[dict[str, str]], *,
    language: str = "",
    voice: str = "",
    keyword: str = "",
) -> list[dict[str, str]]:
    """Case-insensitive filters that may be combined."""
    matches = []
    for row in catalogue:
        if language and language.casefold() not in row["language"].casefold():
            continue
        if voice and voice.casefold() not in row["voice_types"].casefold():
            continue
        if keyword and keyword.casefold() not in " ".join(row.values()).casefold():
            continue
        matches.append(row)
    return matches


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Explore a small open catalogue of classical vocal repertoire"
    )
    parser.add_argument("--language", default="", help="e.g. Italian, French")
    parser.add_argument("--voice", default="", help="e.g. mezzo-soprano, contralto")
    parser.add_argument("--keyword", default="", help="Search names, titles, notes")
    parser.add_argument("--json", action="store_true", help="Print results as JSON")
    args = parser.parse_args(argv)

    result = search_repertoire(
        load_catalogue(), language=args.language,
        voice=args.voice, keyword=args.keyword,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif not result:
        print("No matches. Try a broader search.")
    else:
        for row in result:
            print(f"{row['title']} | {row['composer']} | {row['opera']} | "
                  f"{row['language']} | {row['voice_types']}")
        print(f"\n{len(result)} result(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
