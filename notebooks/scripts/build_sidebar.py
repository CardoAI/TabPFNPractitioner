#!/usr/bin/env python3
"""Build Quarto sidebar metadata from notebook front matter."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
NAV_PATH = ROOT / "_site-nav.yml"
IGNORED_PARTS = {".ipynb_checkpoints", ".quarto", "_site", "_freeze"}
REQUIRED_KEYS = ("title", "section", "section-order")
STATIC_PAGES = ("index.qmd", "site-contract.qmd")


@dataclass
class NotebookPage:
    path: Path
    metadata: dict[str, Any]
    heading_title: str

    @property
    def rel(self) -> str:
        return self.path.relative_to(ROOT).as_posix()

    @property
    def section(self) -> str:
        value = self.metadata.get("section")
        if isinstance(value, str) and value.strip():
            return value.strip()
        return "Needs metadata"

    @property
    def section_order(self) -> float:
        value = as_number(self.metadata.get("section-order"))
        if value is not None:
            return value
        return 100000.0

    @property
    def order(self) -> float:
        value = as_number(self.metadata.get("order"))
        if value is not None:
            return value
        return 100000.0


def as_number(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"true", "false"}:
        return value == "true"
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    number = as_number(value)
    if number is not None:
        return int(number) if number.is_integer() else number
    return value


def parse_front_matter(source: str) -> dict[str, Any]:
    lines = source.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    metadata: dict[str, Any] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            continue
        key, sep, value = line.partition(":")
        if sep and key.strip():
            metadata[key.strip()] = parse_scalar(value)
    return metadata


def first_markdown_cell(cells: list[dict[str, Any]]) -> str:
    for cell in cells:
        if cell.get("cell_type") == "markdown":
            return "".join(cell.get("source", []))
    return ""


def first_heading(source: str) -> str:
    match = re.search(r"^#\s+(.+)$", source, re.MULTILINE)
    return match.group(1).strip() if match else ""


def is_notebook_path(path: Path) -> bool:
    return path.suffix == ".ipynb" and not any(part in IGNORED_PARTS for part in path.parts)


def warn(path: Path, message: str) -> None:
    rel = path.relative_to(ROOT).as_posix()
    print(f"::warning file={rel}::{message}", file=sys.stderr)


def read_notebooks() -> list[NotebookPage]:
    pages: list[NotebookPage] = []
    for path in sorted(ROOT.rglob("*.ipynb")):
        if not is_notebook_path(path.relative_to(ROOT)):
            continue
        with path.open(encoding="utf-8") as handle:
            notebook = json.load(handle)
        cells = notebook.get("cells", [])
        first_md = first_markdown_cell(cells)
        metadata = parse_front_matter(first_md)
        pages.append(NotebookPage(path=path, metadata=metadata, heading_title=first_heading(first_md)))
        validate_notebook(path, metadata, cells)
    return pages


def validate_notebook(path: Path, metadata: dict[str, Any], cells: list[dict[str, Any]]) -> None:
    missing = [key for key in REQUIRED_KEYS if key not in metadata]
    if missing:
        warn(path, "Missing notebook front matter keys: " + ", ".join(missing))

    if "section-order" in metadata and as_number(metadata["section-order"]) is None:
        warn(path, "section-order must be numeric")
    if "order" in metadata and as_number(metadata["order"]) is None:
        warn(path, "order must be numeric")

    for index, cell in enumerate(cells, start=1):
        tags = set(cell.get("metadata", {}).get("tags", []))
        cf_tags = [tag for tag in tags if tag == "counterfactual" or tag.startswith("cf-")]
        if not cf_tags:
            continue
        has_knob = any(tag.startswith("cf-knob:") for tag in tags)
        has_setting = any(tag.startswith("cf-setting:") for tag in tags)
        if not has_knob or not has_setting:
            warn(path, f"Counterfactual cell {index} needs cf-knob and cf-setting tags")


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_nav(pages: list[NotebookPage]) -> str:
    groups: dict[str, list[NotebookPage]] = {}
    section_orders: dict[str, float] = {}
    for page in pages:
        groups.setdefault(page.section, []).append(page)
        section_orders[page.section] = min(section_orders.get(page.section, page.section_order), page.section_order)

    lines = [
        "# Generated by scripts/build_sidebar.py. Do not edit.",
        "website:",
        "  sidebar:",
        "    style: docked",
        "    search: true",
        "    collapse-level: 1",
        "    contents:",
    ]
    for page in STATIC_PAGES:
        lines.append(f"      - {page}")

    for section in sorted(groups, key=lambda item: (section_orders[item], item == "Needs metadata", item)):
        lines.append(f"      - section: {yaml_quote(section)}")
        lines.append("        contents:")
        for page in sorted(groups[section], key=lambda item: (item.order, item.rel)):
            lines.append(f"          - {page.rel}")

    return "\n".join(lines) + "\n"


def main() -> int:
    pages = read_notebooks()
    NAV_PATH.write_text(build_nav(pages), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

