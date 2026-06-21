#!/usr/bin/env python3
"""Create compact GitHub Pages views for the A04 UMAP search experiments."""

from __future__ import annotations

import csv
import html
import json
import re
import shutil
from pathlib import Path


SOURCE = Path("/workspaces/Dev-BT/#運行BERTopic整理/#4. UMAP（未整理）")
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/results"
PAGES = ROOT / "docs/results"

EXPERIMENTS = {
    "A04-2(del)_tok": ("a04-2-del-tok", "A04-2｜del + tok"),
    "A04-3(del)_tok(para12-80)": ("a04-3-del-tok-para12-80", "A04-3｜del + tok + 段落 12-80"),
    "A04-5(repl)_tok": ("a04-5-repl-tok", "A04-5｜repl + tok"),
    "A04-6(repl)_tok(para12-80)": ("a04-6-repl-tok-para12-80", "A04-6｜repl + tok + 段落 12-80"),
    "A04-7(orig)_tok": ("a04-7-orig-tok", "A04-7｜orig + tok"),
    "A04-8(orig)_tok(para12-80)": ("a04-8-orig-tok-para12-80", "A04-8｜orig + tok + 段落 12-80"),
    "[B]01-(orig)_08-19_tok(para12-80)": ("a04-b01-08-19", "A04 B01｜2008-2019"),
    "[B]01-(orig)_20-25_tok(para12-80)": ("a04-b01-20-25", "A04 B01｜2020-2025"),
}


def pct(value: object) -> str:
    return f"{float(value) * 100:.2f}%"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def selected(folder: Path) -> list[dict[str, object]]:
    candidates = list(folder.glob("selected_configs*.csv"))
    if candidates:
        rows = read_csv(candidates[0])
        for row in rows:
            row["selection_label"] = row.get("selection_label") or row.get("selection") or "candidate"
        return rows
    run_log = next(folder.glob("*-run_log.json"))
    payload = json.loads(run_log.read_text(encoding="utf-8"))
    return [{"selection_label": label, **values} for label, values in payload["best"].items()]


def val(row: dict[str, object], key: str, default: str = "-") -> object:
    return row.get(key, default) if row.get(key, "") not in (None, "") else default


def candidate_table(rows: list[dict[str, object]]) -> str:
    labels = {"lowest_noise": "最低雜訊", "most_topics": "最多主題", "best_balance": "最佳平衡"}
    methods = {
        "lowest_noise": "有效結果中 noise ratio 最低；同分時優先較低最大主題比例與較多主題。",
        "most_topics": "在可接受離群比例下，保留有效主題數最多者。",
        "best_balance": "在預設平衡條件下選取最高分：n_clusters ≥ 4、noise ≤ 0.35、最大主題比例 ≤ 0.65、前三主題比例 ≤ 0.85。<br>balance score = 0.30 × (1 − noise ratio) + 0.30 × (1 − 最大主題比例) + 0.20 × (1 − 前三主題比例) + 0.20 × min(主題數 / 25, 1)。",
    }
    body = []
    for row in rows:
        label = str(val(row, "selection_label"))
        body.append(
            "<tr class=\"{}\"><td>{}</td><td>{}</td><td>n_neighbors {} / components {} / min dist {}</td>"
            "<td>cluster {} / samples {} / {} / eps {}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                f"candidate-{label}", labels.get(label, label),
                methods.get(label, "依研究目標選取候選設定。"),
                val(row, "umap_n_neighbors"), val(row, "umap_n_components"), val(row, "umap_min_dist"),
                val(row, "hdbscan_min_cluster_size"), val(row, "hdbscan_min_samples"),
                val(row, "hdbscan_cluster_selection_method"), val(row, "hdbscan_cluster_selection_epsilon"),
                val(row, "n_clusters"), pct(val(row, "noise_ratio", 0)), pct(val(row, "largest_topic_ratio", 0)), val(row, "balance_score"),
            )
        )
    return """<div class="table-scroll"><table class="candidate-table">
<thead><tr><th>策略</th><th>選擇方法</th><th>UMAP</th><th>HDBSCAN</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>balance score</th></tr></thead>
<tbody>{}</tbody>
</table></div>""".format("".join(body))


def download_table(copied: list[Path], asset_dir: Path, slug: str) -> str:
    descriptions = {
        "stage1": "第一階段 UMAP 與精簡 HDBSCAN 的廣泛搜尋結果",
        "stage2": "第二階段候選 UMAP 的深入 HDBSCAN 搜尋結果",
        "selected_configs": "三種候選策略的選定參數與指標",
        "stability": "前段候選在不同 random state 下的穩定性結果",
        "final_configs": "最終 BERTopic 訓練的設定檔",
        "comparison_summary": "三種候選策略的最終比較摘要",
        "run_log": "執行紀錄與資料統計",
        "topic_info": "最終主題資訊摘要",
        "topic_words": "主題關鍵詞輸出",
        "representative_docs": "代表句輸出",
        "brand_model": "品牌與車款詞彙影響檢查",
    }
    rows = []
    for path in copied:
        if path.suffix not in {".csv", ".json", ".md", ".py"} or path.parent != asset_dir:
            continue
        name = path.name
        purpose = next((text for key, text in descriptions.items() if key in name), None)
        if purpose is None:
            if name.endswith(".py"):
                purpose = "本次 UMAP + HDBSCAN 實驗的執行程式"
            elif name.endswith(".md"):
                purpose = "原始實驗報告"
            elif name.endswith(".json"):
                purpose = "設定或中間候選資料"
            else:
                purpose = "實驗輸出資料"
        url = path.relative_to(asset_dir).as_posix()
        rows.append(f'<tr><td><a href="{{{{ \'/assets/results/{slug}/{url}\' | relative_url }}}}">{html.escape(name)}</a></td><td>{purpose}</td></tr>')
    return '<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>"


def run() -> None:
    overview_links = []
    for folder_name, (slug, title) in EXPERIMENTS.items():
        folder = SOURCE / folder_name
        rows = selected(folder)
        log_path = next(iter(folder.glob("*-run_log.json")), None)
        if log_path is None and (folder / "run_log.json").is_file():
            log_path = folder / "run_log.json"
        payload = json.loads(log_path.read_text(encoding="utf-8")) if log_path else {}
        meta = payload.get("dataset_meta") or payload.get("meta") or {}
        report = next(iter(folder.glob("*.md")), None)
        report_text = report.read_text(encoding="utf-8") if report else ""
        match = re.search(r"(?:資料來源|dataset_dir)[：:]?\s*`?([^`\n|]+)", report_text)
        dataset = meta.get("dataset_dir") or payload.get("dataset") or (match.group(1).strip() if match else "-")
        used_rows = meta.get("used_rows") or meta.get("source_rows") or "-"

        asset_dir = ASSETS / slug
        asset_dir.mkdir(parents=True, exist_ok=True)
        copied = []
        # Deliberately avoid traversing final_models/: it contains large,
        # sentence-level artifacts that do not belong on a static Pages site.
        source_files = [path for path in folder.iterdir() if path.is_file()]
        for directory in (folder / "charts", folder / "plots"):
            if directory.is_dir():
                source_files.extend(path for path in directory.iterdir() if path.is_file())
        for path in source_files:
            relative = path.relative_to(folder)
            if path.suffix == ".npy" or path.stat().st_size > 3_000_000:
                continue
            target = asset_dir / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            copied.append(target)

        stage1 = next((path for path in copied if "stage1" in path.name and path.suffix == ".csv"), None)
        stage2 = next((path for path in copied if "stage2" in path.name and path.suffix == ".csv"), None)
        stage1_count = len(read_csv(stage1)) if stage1 else "-"
        stage2_count = len(read_csv(stage2)) if stage2 else "-"
        key_charts = [p for p in copied if p.suffix == ".png" and any(x in p.name for x in ("best_three", "parameter_heatmap", "selected_configs"))][:3]
        figures = "".join(
            f'<figure><img src="{{{{ \'/assets/results/{slug}/{path.relative_to(asset_dir).as_posix()}\' | relative_url }}}}" alt="{html.escape(path.stem)}"><figcaption>{html.escape(path.stem.replace("_", " "))}</figcaption></figure>'
            for path in key_charts
        )
        figure_block = f'<div class="result-figure-scroller">{figures}</div>' if figures else ""
        page = f'''---
title: {title} UMAP 搜尋
description: {title} 的 UMAP 與 HDBSCAN 聯合參數搜尋。
---

# {title}｜UMAP 搜尋

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>{html.escape(str(dataset))}</code></td></tr>
<tr><td>可用句子</td><td>{used_rows}</td></tr>
<tr><td>Embedding</td><td><code>all-MiniLM-L6-v2</code></td></tr>
<tr><td>UMAP</td><td>cosine / random state 42</td></tr>
</tbody></table>

### 搜尋流程

<table class="settings-table"><thead><tr><th>階段</th><th>設定</th></tr></thead><tbody>
<tr><td>第一階段</td><td>{stage1_count} 組廣泛搜尋</td></tr>
<tr><td>第二階段</td><td>{stage2_count} 組候選深入搜尋</td></tr>
<tr><td>候選策略</td><td>最低雜訊 / 最多主題 / 最佳平衡</td></tr>
</tbody></table>
</aside>

<section markdown="1">
## UMAP 測試目的


本測試在固定語意向量模型後，同時探索 UMAP 降維與 HDBSCAN 分群設定，檢查目前資料版本能否比前一階段的 min_cluster_size 掃描取得更平衡的主題結構。UMAP 的 `n_neighbors` 調整局部與全域結構的取捨，`n_components` 決定降維後的維度數，`min_dist` 則控制群集在低維空間中的緊密程度；後續再搭配 HDBSCAN 的群集大小、保守程度與切分方式進行評估。

## UMAP 參數設定

### 共通設定

<table class="umap-config-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>Embedding</td><td><code>all-MiniLM-L6-v2</code>；每個資料集僅計算一次並快取</td></tr>
<tr><td>距離度量</td><td>UMAP：<code>cosine</code>；HDBSCAN：<code>euclidean</code></td></tr>
<tr><td>基準 random state</td><td><code>42</code></td></tr>
<tr><td>穩定性檢測</td><td>前 10 組候選使用 <code>42</code>、<code>123</code>、<code>2026</code>、<code>3407</code>、<code>20240603</code></td></tr>
</tbody></table>

### 第一階段：廣泛搜尋

<table class="umap-config-table"><thead><tr><th>模組</th><th>測試設定</th></tr></thead><tbody>
<tr><td>UMAP</td><td><code>n_neighbors</code>：5、10、15、30、50、75、100；<code>n_components</code>：5、10、15；<code>min_dist</code>：0.0、0.05、0.1、0.25</td></tr>
<tr><td>HDBSCAN</td><td><code>min_cluster_size</code>：50 至 300 的 10 組；<code>min_samples</code>：None、10、30；<code>method</code>：eom；<code>epsilon</code>：0.0</td></tr>
</tbody></table>

### 第二階段：候選深入搜尋

<table class="umap-config-table"><thead><tr><th>模組</th><th>測試設定</th></tr></thead><tbody>
<tr><td>UMAP</td><td>取第一階段前 10 組 UMAP 設定</td></tr>
<tr><td>HDBSCAN</td><td><code>min_cluster_size</code>：50 至 1000 的 21 組；<code>min_samples</code>：None、5、10、15、30、50、75、100；<code>method</code>：eom、leaf；<code>epsilon</code>：0.0、0.05、0.1、0.2</td></tr>
<tr><td>每組統計</td><td>UMAP／HDBSCAN 參數、主題數、noise ratio、離群筆數、最大主題比例、前三主題比例、entropy、balance score、狀態與備註</td></tr>
</tbody></table>

## 三種候選策略

最低雜訊、最多主題與最佳平衡代表不同的研究取捨；本頁保留三者，避免以單一 noise ratio 取代語意品質判讀。

{candidate_table(rows)}

## 圖表檢視

候選策略比較圖用來並列三種策略的主題數、noise ratio 與主題集中度；參數熱圖或選定設定比較圖則用來觀察不同 UMAP／HDBSCAN 組合對分群結果的影響。

{figure_block}

## 原始輸出

{download_table(copied, asset_dir, slug)}
</section>
</div>
'''
        (PAGES / f"{slug}.md").write_text(page, encoding="utf-8")
        overview_links.append(f"[{title}]({{{{ '/results/{slug}.html' | relative_url }}}})")
        print(f"Imported {folder_name}")

    (PAGES / "a04-umap-overview.md").write_text(
        "---\ntitle: A04 UMAP 整體比較\ndescription: A04 UMAP 與 HDBSCAN 聯合搜尋結果。\n---\n\n"
        "# A04｜UMAP 整體比較\n\n"
        "A04 階段同時探索 UMAP 降維與 HDBSCAN 分群設定；每個資料版本均保留最低雜訊、最多主題與最佳平衡三種候選策略。\n\n"
        "## 個別實驗\n\n可直接查看：" + "、".join(overview_links) + "。\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    run()
