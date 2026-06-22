#!/usr/bin/env python3
"""Build and validate the single-source experiment registry for GitHub Pages.

The registry owns repeatable metadata: result-page identity, setting panels,
result-index rows, and experiment-map destinations. Rich analysis content stays
in the individual Markdown page where it belongs.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
RESULTS = DOCS / "results"
DATA_FILE = DOCS / "_data" / "experiments.json"
PUBLIC_FILE = DOCS / "assets" / "data" / "experiments.json"
INCLUDE_FILE = DOCS / "_includes" / "result-settings.html"
RESULT_INDEX = DOCS / "results.md"
MAP_FILE = DOCS / "assets" / "img" / "experiment-map-full.svg"

ASIDE_RE = re.compile(
    r'<aside class="result-settings" markdown="1">\n(?P<content>.*?)\n</aside>',
    re.DOTALL,
)
FRONT_MATTER_RE = re.compile(r"\A---\n(?P<data>.*?)\n---\n", re.DOTALL)
H1_RE = re.compile(r"^# (?P<title>.+)$", re.MULTILINE)
LIQUID_URL_RE = re.compile(
    r"\{\{\s*['\"](?P<path>/(?:results|assets)/[^'\"]+)['\"]\s*\|\s*relative_url\s*\}\}"
)

GROUPS = [
    {
        "id": "a03",
        "title": "A03 min_cluster_size 掃描",
        "description": "固定其他設定，檢查資料處理版本與最小群集大小對主題結構的影響。",
    },
    {
        "id": "a04",
        "title": "A04 UMAP 搜尋",
        "description": "聯合搜尋 UMAP 與 HDBSCAN 參數，保留不同研究取捨的候選策略。",
    },
    {
        "id": "a05",
        "title": "A05 停用詞設計",
        "description": "記錄 A05-6 與 A05-8 orig REV 的停用詞版本線與人工收斂結果。",
    },
    {
        "id": "b01",
        "title": "年份切分 min_cluster_size 掃描",
        "description": "分別以 2008-2019 與 2020-2025 資料進行最小群集大小掃描。",
    },
    {
        "id": "m01",
        "title": "M01 歷史主程式",
        "description": "保留三種候選策略的歷史比較結果，供研究追溯。",
    },
    {
        "id": "m02",
        "title": "M02 單一參數主程式",
        "description": "以選定參數進行 BERTopic 訓練與 LLM 命名穩定性驗證。",
    },
    {
        "id": "m03",
        "title": "M03 年份切分主程式",
        "description": "以 2020 為界比較前後資料期間的主題結構。",
    },
    {
        "id": "t01",
        "title": "T01 刪除／替換驗證",
        "description": "比較移除品牌／車款詞與替換為 Brand／Model 的差異。",
    },
    {
        "id": "t02",
        "title": "T02 年份切分驗證",
        "description": "以 2018、2019、2021 為界檢查不同年份分段的穩定性。",
    },
]
GROUP_IDS = {group["id"] for group in GROUPS}
FEATURED = {
    "a03-2-del-tok",
    "m01-8-historical",
    "m02-llm30",
    "m02-llm50",
    "m03-2020-before",
    "m03-2020-after",
    "t01-overview",
    "t02-overview",
}
PENDING = [
    {
        "label": "T03-T04 節點",
        "description": "資料篩選與 repl 停用詞驗證",
        "status": "待整理",
    }
]


def group_for(slug: str) -> str | None:
    for group in GROUP_IDS:
        if slug.startswith(group):
            return group
    return None


def read_front_matter(source: str) -> tuple[dict[str, str], str]:
    match = FRONT_MATTER_RE.match(source)
    if not match:
        raise ValueError("Missing YAML front matter")
    values: dict[str, str] = {}
    for line in match.group("data").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values, source[match.end() :]


def page_metadata(path: Path) -> dict[str, str]:
    source = path.read_text(encoding="utf-8")
    front_matter, body = read_front_matter(source)
    heading = H1_RE.search(body)
    return {
        "title": front_matter.get("title", path.stem),
        "description": front_matter.get("description", ""),
        "heading": heading.group("title") if heading else front_matter.get("title", path.stem),
    }


def target_slug(target: str) -> str | None:
    match = re.search(r"/results/([^/'\"]+)\.html$", target)
    return match.group(1) if match else None


def map_bindings() -> dict[str, dict[str, list[str]]]:
    """Read destinations from the shipped SVG, preserving the confirmed map."""
    source = MAP_FILE.read_text(encoding="utf-8")
    bindings: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"labels": [], "node_ids": []})

    def add(slug: str | None, key: str, value: str) -> None:
        if slug and value not in bindings[slug][key]:
            bindings[slug][key].append(value)

    for object_name, key in (("resultLinks", "labels"), ("resultLinksById", "node_ids")):
        block = re.search(rf"const {object_name} = \{{(?P<body>.*?)\n    \}};", source, re.DOTALL)
        if not block:
            continue
        for value, destination in re.findall(r"'([^']+)': '([^']+)'", block.group("body")):
            add(target_slug(destination), key, value)

    anchor_pattern = re.compile(
        r'<a href="(?P<href>[^"]+)" target="_top">\s*'
        r'<g class="[^"]+" data-id="(?P<node_id>[^"]+)" data-label="(?P<label>[^"]+)"',
        re.DOTALL,
    )
    for match in anchor_pattern.finditer(source):
        slug = target_slug(match.group("href"))
        add(slug, "node_ids", match.group("node_id"))
        add(slug, "labels", match.group("label"))

    return dict(bindings)


def normalize_sidebar_line(line: str) -> str:
    def replace_url(match: re.Match[str]) -> str:
        path = match.group("path")
        if path.startswith("/results/"):
            return Path(path).name
        return "../" + path.lstrip("/")

    return LIQUID_URL_RE.sub(replace_url, line)


def page_record(
    path: Path,
    settings_lines: list[str] | None,
    bindings: dict[str, dict[str, list[str]]],
) -> dict[str, object]:
    slug = path.stem
    metadata = page_metadata(path)
    record: dict[str, object] = {
        "id": slug,
        "page": f"/results/{slug}.html",
        "title": metadata["heading"],
        "description": metadata["description"],
        "group": group_for(slug),
        "status": "可檢視",
        "featured": slug in FEATURED,
        "map": bindings.get(slug, {"labels": [], "node_ids": []}),
    }
    if settings_lines is not None:
        record["kind"] = "detail"
        record["settings_lines"] = settings_lines
    else:
        record["kind"] = "overview"
    return record


def replace_sidebar_with_include(path: Path, source: str, slug: str) -> str:
    front_matter, _ = read_front_matter(source)
    if "experiment_id" not in front_matter:
        match = FRONT_MATTER_RE.match(source)
        assert match
        lines = match.group("data").splitlines()
        lines.append(f"experiment_id: {slug}")
        source = "---\n" + "\n".join(lines) + "\n---\n" + source[match.end() :]

    return ASIDE_RE.sub("{% include result-settings.html id=page.experiment_id %}", source, count=1)


def natural_key(record: dict[str, object]) -> list[object]:
    group = str(record.get("group") or "zz")
    group_position = next((index for index, item in enumerate(GROUPS) if item["id"] == group), len(GROUPS))
    chunks = re.split(r"(\d+)", str(record["id"]))
    return [group_position, *[int(chunk) if chunk.isdigit() else chunk for chunk in chunks]]


def load_existing() -> dict[str, dict[str, object]]:
    if not DATA_FILE.exists():
        return {}
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {str(item["id"]): item for item in data.get("experiments", [])}


def build_registry(migrate: bool) -> dict[str, object]:
    existing = load_existing()
    bindings = map_bindings()
    for slug, record in existing.items():
        stored = record.get("map", {})
        current = bindings.setdefault(slug, {"labels": [], "node_ids": []})
        for key in ("labels", "node_ids"):
            for value in stored.get(key, []):
                if value not in current[key]:
                    current[key].append(value)
    records: dict[str, dict[str, object]] = dict(existing)

    for path in sorted(RESULTS.glob("*.md")):
        source = path.read_text(encoding="utf-8")
        aside = ASIDE_RE.search(source)
        slug = path.stem
        if aside:
            settings_lines = [normalize_sidebar_line(line) for line in aside.group("content").splitlines()]
            records[slug] = page_record(path, settings_lines, bindings)
            if migrate:
                path.write_text(replace_sidebar_with_include(path, source, slug), encoding="utf-8")
        elif slug in records:
            records[slug] = page_record(path, records[slug].get("settings_lines"), bindings)

    # Map targets without a setting panel remain in the registry, so the index
    # and the map continue to use the same page identity.
    for slug in bindings:
        path = RESULTS / f"{slug}.md"
        if path.exists() and slug not in records:
            records[slug] = page_record(path, None, bindings)

    published = [record for record in records.values() if record.get("group")]
    published.sort(key=natural_key)
    return {
        "schema_version": 1,
        "groups": GROUPS,
        "experiments": published,
        "pending": PENDING,
    }


def write_include() -> None:
    INCLUDE_FILE.parent.mkdir(parents=True, exist_ok=True)
    INCLUDE_FILE.write_text(
        """{% assign experiment = site.data.experiments.experiments | where: "id", include.id | first %}
<aside class="result-settings" markdown="1">
{% if experiment and experiment.settings_lines %}
{% for line in experiment.settings_lines %}
{{ line }}
{% endfor %}
{% else %}
## 實驗設定

<p>此頁尚未登錄設定資料。</p>
{% endif %}
</aside>
""",
        encoding="utf-8",
    )


def render_results_index() -> str:
    return """---
title: 結果
description: DEV-BT 實驗資料血緣、處理順序與已整理結果。
---

# 結果

本頁依實驗的資料血緣與處理順序呈現。可點擊的節點已有完整結果與設定摘要；其他節點保留在地圖中，待後續整理後開放。

<div class="experiment-map-scroll" aria-label="DEV-BT 完整實驗地圖">
  <object class="experiment-map-full" type="image/svg+xml" data="{{ '/assets/img/experiment-map-full.svg?v=registry-v1' | relative_url }}">
    <img src="{{ '/assets/img/experiment-map-full.svg?v=registry-v1' | relative_url }}" alt="DEV-BT 完整實驗運行架構圖">
  </object>
</div>

## 如何閱讀

A03-A05 是資料版本、UMAP 與停用詞處理的探索階段；M01-M03 是選定設定後的主要模型運行；T01-T04 則用不同資料處理、年份切分與資料篩選條件檢驗結果是否穩定。

{% assign registry = site.data.experiments %}

## 已整理結果

| 終點 | 實驗意義 | 目前狀態 |
| --- | --- | --- |
{% for item in registry.experiments %}{% if item.featured %}
| [{{ item.title }}]({{ item.page | relative_url }}) | {{ item.description }} | {{ item.status }} |
{% endif %}{% endfor %}
{% for item in registry.pending %}
| {{ item.label }} | {{ item.description }} | {{ item.status }} |
{% endfor %}

{% for group in registry.groups %}
## {{ group.title }}

{{ group.description }}

| 節點 | 實驗意義 | 目前狀態 |
| --- | --- | --- |
{% for item in registry.experiments %}{% if item.group == group.id %}
| [{{ item.title }}]({{ item.page | relative_url }}) | {{ item.description }} | {{ item.status }} |
{% endif %}{% endfor %}
{% endfor %}
"""


def map_href(page: str) -> str:
    return "../../" + page.lstrip("/")


def sync_map(registry: dict[str, object]) -> None:
    """Synchronize the interactive SVG's JavaScript maps without draw.io input."""
    source = MAP_FILE.read_text(encoding="utf-8")
    labels: dict[str, str] = {}
    node_ids: dict[str, str] = {}
    for item in registry["experiments"]:
        destination = map_href(str(item["page"]))
        mapping = item.get("map", {})
        for label in mapping.get("labels", []):
            labels[str(label)] = destination
        for node_id in mapping.get("node_ids", []):
            node_ids[str(node_id)] = destination

    def object_literal(name: str, values: dict[str, str]) -> str:
        rows = [f"      {json.dumps(key, ensure_ascii=False)}: {json.dumps(value)}" for key, value in values.items()]
        return f"const {name} = {{\n" + ",\n".join(rows) + "\n    };"

    for name, values in (("resultLinks", labels), ("resultLinksById", node_ids)):
        source, count = re.subn(
            rf"const {name} = \{{.*?\n    \}};",
            object_literal(name, values),
            source,
            count=1,
            flags=re.DOTALL,
        )
        if count != 1:
            raise RuntimeError(f"Could not update {name} in {MAP_FILE}")

    anchor_pattern = re.compile(
        r'(<a href=")[^"]+(" target="_top">\s*<g class="[^"]+" data-id="(?P<node_id>[^"]+)" data-label="(?P<label>[^"]+)")',
        re.DOTALL,
    )

    def replace_anchor(match: re.Match[str]) -> str:
        destination = node_ids.get(match.group("node_id")) or labels.get(match.group("label"))
        return f'{match.group(1)}{destination}{match.group(2)}' if destination else match.group(0)

    MAP_FILE.write_text(anchor_pattern.sub(replace_anchor, source), encoding="utf-8")


def validate(registry: dict[str, object]) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    records = registry["experiments"]
    for item in records:
        item_id = str(item["id"])
        if item_id in ids:
            errors.append(f"Duplicate id: {item_id}")
        ids.add(item_id)
        page = DOCS / Path(str(item["page"]).lstrip("/")).with_suffix(".md")
        if not page.exists():
            errors.append(f"Missing page: {page}")
        if item.get("kind") == "detail" and not item.get("settings_lines"):
            errors.append(f"Missing settings_lines: {item_id}")

    for path in RESULTS.glob("*.md"):
        source = path.read_text(encoding="utf-8")
        if ASIDE_RE.search(source):
            errors.append(f"Inline settings panel remains in {path.name}; run with --migrate")
        if "experiment_id:" not in source:
            continue
        match = re.search(r"^experiment_id:\s*(\S+)\s*$", source, re.MULTILINE)
        if not match or match.group(1) not in ids:
            errors.append(f"Unknown experiment_id in {path.name}")
    return errors


def write_registry(registry: dict[str, object]) -> None:
    payload = json.dumps(registry, ensure_ascii=False, indent=2) + "\n"
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(payload, encoding="utf-8")
    PUBLIC_FILE.write_text(payload, encoding="utf-8")
    RESULT_INDEX.write_text(render_results_index(), encoding="utf-8")
    write_include()


def sync_registry(*, migrate: bool = False) -> dict[str, object]:
    """Refresh every registry-derived surface after an experiment import."""
    registry = build_registry(migrate=migrate)
    errors = validate(registry)
    if errors:
        raise RuntimeError("\n".join(errors))
    write_registry(registry)
    sync_map(registry)
    return registry


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--migrate", action="store_true", help="move existing setting panels into the registry")
    parser.add_argument("--check", action="store_true", help="validate the existing registry without writing")
    args = parser.parse_args()

    if args.check:
        registry = build_registry(migrate=False)
        errors = validate(registry)
        if errors:
            raise SystemExit("\n".join(errors))
        print(f"Registry valid: {len(registry['experiments'])} published records")
        return
    try:
        registry = sync_registry(migrate=args.migrate)
    except RuntimeError as error:
        raise SystemExit(str(error)) from error
    print(f"Wrote registry, shared setting panel, result index, and map links for {len(registry['experiments'])} records")


if __name__ == "__main__":
    main()
