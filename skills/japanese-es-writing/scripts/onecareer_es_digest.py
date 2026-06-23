#!/usr/bin/env python3
"""Create a compact ES-writing digest from saved OneCareer text files.

This does not rewrite or copy ES answers into the skill. It extracts reusable
signals for writing support: frequent question prompts, selection stages, and
company-specific keywords. Review the digest manually before using it to update
reference files.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path


QUESTION_MARKERS = (
    "志望動機",
    "自己PR",
    "学生時代",
    "ガクチカ",
    "研究",
    "ゼミ",
    "強み",
    "弱み",
    "キャリア",
    "入社後",
    "挑戦",
    "困難",
    "挫折",
)

STAGE_MARKERS = (
    "エントリーシート",
    "ES",
    "WEBテスト",
    "面接",
    "グループディスカッション",
    "GD",
    "インターン",
    "本選考",
    "リクルーター",
    "OB訪問",
    "内定",
)


def normalize(text: str) -> str:
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_candidate_prompts(text: str) -> list[str]:
    prompts: list[str] = []
    for match in re.finditer(r"〖([^〗]{8,160})〗", text):
        prompt = normalize(match.group(1))
        if any(marker in prompt for marker in QUESTION_MARKERS):
            prompts.append(prompt)
    return prompts


def marker_counts(text: str, markers: tuple[str, ...]) -> collections.Counter[str]:
    counts: collections.Counter[str] = collections.Counter()
    for marker in markers:
        count = text.count(marker)
        if count:
            counts[marker] = count
    return counts


def load_index(input_dir: Path) -> list[dict[str, str]]:
    index_path = input_dir / "index.jsonl"
    if index_path.exists():
        rows = []
        with index_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
        return rows
    return [{"company": path.stem, "text": str(path)} for path in sorted(input_dir.glob("*.txt"))]


def build_digest(input_dir: Path) -> str:
    rows = load_index(input_dir)
    if not rows:
        raise SystemExit(f"No saved OneCareer text files found in {input_dir}")

    by_company: dict[str, list[Path]] = collections.defaultdict(list)
    for row in rows:
        text_path = Path(row["text"])
        if not text_path.is_absolute():
            text_path = Path(row["text"])
        if text_path.exists():
            by_company[row.get("company", text_path.stem)].append(text_path)

    lines = [
        "# OneCareer ES Research Digest",
        "",
        "Use this digest as writing-pattern research only. Do not copy candidate ES answers verbatim.",
        "",
    ]

    all_prompts: collections.Counter[str] = collections.Counter()
    all_stages: collections.Counter[str] = collections.Counter()

    for company, paths in sorted(by_company.items()):
        company_text = "\n\n".join(path.read_text(encoding="utf-8", errors="replace") for path in paths)
        prompts = split_candidate_prompts(company_text)
        prompt_counts = collections.Counter(prompts)
        stage_counts = marker_counts(company_text, STAGE_MARKERS)
        all_prompts.update(prompt_counts)
        all_stages.update(stage_counts)

        lines.extend([f"## {company}", ""])
        if stage_counts:
            lines.append("Selection-stage keywords:")
            for marker, count in stage_counts.most_common():
                lines.append(f"- {marker}: {count}")
            lines.append("")
        if prompt_counts:
            lines.append("Frequent ES/question prompts:")
            for prompt, count in prompt_counts.most_common(20):
                suffix = f" ({count})" if count > 1 else ""
                lines.append(f"- {prompt}{suffix}")
            lines.append("")

    lines.extend(["## Overall Patterns", ""])
    if all_stages:
        lines.append("Common selection-stage keywords:")
        for marker, count in all_stages.most_common():
            lines.append(f"- {marker}: {count}")
        lines.append("")
    if all_prompts:
        lines.append("Common ES/question prompts:")
        for prompt, count in all_prompts.most_common(30):
            suffix = f" ({count})" if count > 1 else ""
            lines.append(f"- {prompt}{suffix}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize saved OneCareer text for ES writing research.")
    parser.add_argument("--input", default="fetched/onecareer", help="Directory from onecareer_browser_fetch.py.")
    parser.add_argument("--out", default="fetched/onecareer_digest.md", help="Digest markdown path.")
    args = parser.parse_args()

    digest = build_digest(Path(args.input))
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(digest, encoding="utf-8")
    print(f"Wrote digest: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
