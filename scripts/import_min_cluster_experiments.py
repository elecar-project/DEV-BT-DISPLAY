#!/usr/bin/env python3
"""Import the remaining min_cluster_size experiments into the Pages site."""

from __future__ import annotations

import ast
import csv
import html
import json
import re
import shutil
from pathlib import Path


SOURCE = Path("/workspaces/Dev-BT/#運行BERTopic整理/#3. min_cluster（未整理）")
ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "docs/assets/results"
PAGE_ROOT = ROOT / "docs/results"

EXPERIMENTS = {
    "A03-3(del)_tok(para12-80)": ("a03-3-del-tok-para12-80", "A03-3｜del + tok + 段落 12-80"),
    "A03-5(repl)_tok": ("a03-5-repl-tok", "A03-5｜repl + tok"),
    "A03-5.1(repl-y)_tok": ("a03-5-1-repl-y-tok", "A03-5.1｜repl-y + tok"),
    "A03-6(repl)_tok(para12-80)": ("a03-6-repl-tok-para12-80", "A03-6｜repl + tok + 段落 12-80"),
    "A03-6.1(repl-y)_tok(para12-80)": ("a03-6-1-repl-y-tok-para12-80", "A03-6.1｜repl-y + tok + 段落 12-80"),
    "A03-7(orig)_tok": ("a03-7-orig-tok", "A03-7｜orig + tok"),
    "A03-8(orig)_tok(para12-80)": ("a03-8-orig-tok-para12-80", "A03-8｜orig + tok + 段落 12-80"),
    "[B]01-(orig)_08-19(240)_tok(para12-80)": ("b01-08-19-min-cluster", "B01｜2008-2019 min_cluster_size 掃描"),
    "[B]01-(orig)_20-25(194)_tok(para12-80)": ("b01-20-25-min-cluster", "B01｜2020-2025 min_cluster_size 掃描"),
}

EXTRA_CHARTS = {
    "A03-5.1(repl-y)_tok": Path(
        "/workspaces/Dev-BT/#運行BERTopic整理/#3.1 min圖/06.03_PNG_ver.1_2,3,5,6,7,8+5.1,6.1/"
        "A03-5.1(repl-y)_tok_min_cluster_chart.png"
    ),
}


def pct(value: str | float) -> str:
    return f"{float(value) * 100:.2f}%"


def first(folder: Path, pattern: str) -> Path:
    matches = list(folder.glob(pattern))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {pattern} in {folder}, found {len(matches)}")
    return matches[0]


def html_table(rows: list[dict[str, str]], best_size: int) -> str:
    body = []
    for row in rows:
        selected = int(row["min_cluster_size"]) == best_size
        label = '<span class="scan-badge">自動選擇：最低雜訊</span>' if selected else ""
        body.append(
            "<tr{}><td>{}</td><td>{}</td><td>{}</td><td>{:,}</td><td>{:,}</td><td>{:,}</td><td>{}</td></tr>".format(
                ' class="selection-row"' if selected else "",
                row["min_cluster_size"],
                row["n_clusters"],
                pct(row["noise_ratio"]),
                int(row["topic_-1_count"]),
                int(row["topic_0_count"]),
                int(row["topic_1_count"]),
                label,
            )
        )
    return """<div class="table-scroll">
<table class="scan-table">
  <thead><tr><th>min cluster size</th><th>非 noise 主題數</th><th>noise ratio</th><th>離群句數</th><th>主題 0</th><th>主題 1</th><th>自動選擇</th></tr></thead>
  <tbody>{}</tbody>
</table>
</div>""".format("".join(body))


def topic_table(rows: list[dict[str, str]]) -> str:
    total = sum(int(row["Count"]) for row in rows)
    body = []
    for row in rows:
        words = ", ".join(ast.literal_eval(row["Representation"]))
        topic = "-1（noise）" if row["Topic"] == "-1" else row["Topic"]
        body.append(
            "<tr><td>{}</td><td>{:,}</td><td>{}</td><td>{}</td></tr>".format(
                topic, int(row["Count"]), pct(int(row["Count"]) / total), html.escape(words)
            )
        )
    return """<div class="table-scroll">
<table class="topic-table">
  <thead><tr><th>Topic</th><th>句數</th><th>比例</th><th>前十個代表詞</th></tr></thead>
  <tbody>{}</tbody>
</table>
</div>""".format("".join(body))


def settings_table(dataset_source: str, meta: dict[str, object]) -> str:
    source = html.escape(dataset_source)
    text_col = html.escape(str(meta["text_col"]))
    return f'''<table class="settings-table">
  <thead><tr><th>項目</th><th>設定</th></tr></thead>
  <tbody>
    <tr><td>資料集</td><td><code>{source}</code></td></tr>
    <tr><td>使用欄位</td><td><code>{text_col}</code></td></tr>
    <tr><td>可用句子</td><td>{int(meta["used_rows"]):,}</td></tr>
    <tr><td>短句</td><td>{int(meta["short_rows_lt_3_words_count"]):,} 筆少於 3 words</td></tr>
  </tbody>
</table>

<table class="settings-table">
  <thead><tr><th>項目</th><th>設定</th></tr></thead>
  <tbody>
    <tr><td>Embedding</td><td><code>all-MiniLM-L6-v2</code></td></tr>
    <tr><td>UMAP</td><td>neighbors 15 / components 5 / min dist 0 / cosine</td></tr>
    <tr><td>HDBSCAN</td><td>euclidean / eom / prediction data</td></tr>
    <tr><td>Vectorizer</td><td>English stop words / ngram 1-2 / min df 2</td></tr>
  </tbody>
</table>'''


def run() -> None:
    for folder_name, (slug, title) in EXPERIMENTS.items():
        folder = SOURCE / folder_name
        report = first(folder, "*.md").read_text(encoding="utf-8")
        run_log = json.loads(first(folder, "*-run_log.json").read_text(encoding="utf-8"))
        with first(folder, "*-min_cluster_size.csv").open(encoding="utf-8", newline="") as handle:
            scan_rows = list(csv.DictReader(handle))
        with first(folder, "*-best_topic_info.csv").open(encoding="utf-8", newline="") as handle:
            topic_rows = list(csv.DictReader(handle))

        meta = run_log["dataset_meta"]
        best = run_log["best"]["best_row"]
        best_size = int(best["min_cluster_size"])
        source_match = re.search(r"資料來源：`([^`]+)`", report)
        dataset_source = source_match.group(1) if source_match else meta["dataset_dir"]
        total = sum(int(row["Count"]) for row in topic_rows)
        non_noise = [row for row in topic_rows if row["Topic"] != "-1"]
        largest = max(non_noise, key=lambda row: int(row["Count"]))
        largest_share = pct(int(largest["Count"]) / total)

        asset_dir = ASSET_ROOT / slug
        asset_dir.mkdir(parents=True, exist_ok=True)
        copied: list[Path] = []
        for path in folder.iterdir():
            if path.suffix == ".npy" or not path.is_file():
                continue
            target = asset_dir / path.name
            shutil.copy2(path, target)
            copied.append(target)

        extra_chart = EXTRA_CHARTS.get(folder_name)
        if extra_chart:
            target = asset_dir / extra_chart.name
            shutil.copy2(extra_chart, target)
            copied.append(target)

        chart = next((path.name for path in copied if path.name.endswith("_min_cluster_chart.png")), None)
        chart_html = (
            f'''<div class="result-figure-scroller" aria-label="{html.escape(title)} 圖表檢視">
  <figure><img src="{{{{ '/assets/results/{slug}/{chart}' | relative_url }}}}" alt="{html.escape(title)} min cluster size 掃描圖"><figcaption>min_cluster_size 掃描圖</figcaption></figure>
</div>'''
            if chart
            else ""
        )
        download_rows = []
        names = {
            "-min_cluster_size.csv": "參數掃描 CSV",
            "-best_topic_info.csv": "主題摘要 CSV",
            "-best_document_topics.csv": "句子－主題對照 CSV",
            "-run_log.json": "run log JSON",
            ".md": "實驗報告 Markdown",
            ".py": "執行程式 Python",
        }
        for suffix, display in names.items():
            match = next((path.name for path in copied if path.name.endswith(suffix)), None)
            if match:
                download_rows.append(
                    f"| [{display}]({{{{ '/assets/results/{slug}/{match}' | relative_url }}}}) | {display}原始檔 |"
                )

        page = f'''---
title: {title}
description: {title} 的 HDBSCAN min_cluster_size 敏感度分析。
---

# {title}

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

{settings_table(dataset_source, meta).split('</table>')[0]}</table>

### 固定模型設定

{settings_table(dataset_source, meta).split('</table>', 1)[1]}
</aside>

<section markdown="1">
<div class="run-summary">
  <div class="run-stat"><strong>{len(scan_rows)}</strong><span>測試參數組數</span></div>
  <div class="run-stat"><strong>{best_size}</strong><span>自動選擇值</span></div>
  <div class="run-stat"><strong>{pct(best['noise_ratio'])}</strong><span>該設定 noise ratio</span></div>
  <div class="run-stat"><strong>{best['n_clusters']}</strong><span>非 noise 主題數</span></div>
</div>

## 結果摘要

本實驗固定 embedding 與 UMAP 設定，只掃描 HDBSCAN 的 `min_cluster_size`。自動選擇規則為：先保留至少兩個非 noise 主題，再選取 noise ratio 最低的設定。

> **判讀提醒：** 自動選擇的 `min_cluster_size={best_size}` 最大非 noise 主題占 {largest_share}。noise ratio 是重要指標，但仍應搭配代表詞、代表句與主題大小分布進行人工審查。

{chart_html}

## 參數掃描結果

{html_table(scan_rows, best_size)}

## 自動選擇值的主題分布

{topic_table(topic_rows)}

## 來源檔案與下載

| 檔案 | 用途 |
| --- | --- |
{chr(10).join(download_rows)}

</section>
</div>
'''
        (PAGE_ROOT / f"{slug}.md").write_text(page, encoding="utf-8")
        print(f"Imported {folder_name} -> {slug}")


if __name__ == "__main__":
    run()
