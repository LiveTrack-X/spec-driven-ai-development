from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PATH = Path("docs/no-clone-quick-install.md")
CANONICAL_HEADING = "## Option 1: Give This To Your AI Agent"
README_PATH = Path("README.md")
README_HEADING = "## Copy-Paste Start Prompt"


def fenced_prompt_span(text: str, heading: str) -> tuple[int, int, str]:
    heading_match = re.search(rf"(?m)^{re.escape(heading)}\s*$", text)
    if heading_match is None:
        raise ValueError(f"Missing prompt heading: {heading}")

    section_start = heading_match.end()
    next_heading = re.search(r"(?m)^##\s+", text[section_start:])
    section_end = (
        section_start + next_heading.start() if next_heading is not None else len(text)
    )
    section = text[section_start:section_end]
    fence_match = re.search(r"(?ms)^```text\s*\n(.*?)^```\s*$", section)
    if fence_match is None:
        raise ValueError(f"Missing text fence under prompt heading: {heading}")

    content_start = section_start + fence_match.start(1)
    content_end = section_start + fence_match.end(1)
    return content_start, content_end, fence_match.group(1)


def prompt_content(text: str, heading: str) -> str:
    return fenced_prompt_span(text, heading)[2]


def synchronized_readme(root: Path = ROOT) -> tuple[str, str]:
    canonical_text = (root / CANONICAL_PATH).read_text(encoding="utf-8")
    readme_path = root / README_PATH
    readme = readme_path.read_text(encoding="utf-8")
    canonical = prompt_content(canonical_text, CANONICAL_HEADING)
    start, end, _ = fenced_prompt_span(readme, README_HEADING)
    return readme, readme[:start] + canonical + readme[end:]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Keep the README start prompt identical to no-clone Option 1."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when README does not match the canonical Option 1 prompt.",
    )
    args = parser.parse_args()

    current, expected = synchronized_readme()
    if args.check:
        if current == expected:
            print("README copy-paste prompt matches no-clone Option 1.")
            return 0
        print("README copy-paste prompt differs from no-clone Option 1.")
        return 1

    with (ROOT / README_PATH).open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(expected)
    print("Synchronized README copy-paste prompt from no-clone Option 1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
