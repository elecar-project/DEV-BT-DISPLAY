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
    "[B]01-(orig)_08-19_tok(para12-80)": ("a04-b01-08-19", "A04｜2020 前（2008-2019）"),
    "[B]01-(orig)_20-25_tok(para12-80)": ("a04-b01-20-25", "A04｜2020 後（2020-2025）"),
}

CHART_LABELS = {
    "best_three_comparison": "三種候選策略比較",
    "parameter_heatmap": "參數組合熱圖",
    "best_balance_topic_size_bar": "最佳平衡的主題規模分布",
    "cluster_selection_method_comparison": "HDBSCAN 切分方式比較",
    "min_cluster_size_dual_axis": "min_cluster_size 與主題數／noise ratio",
    "min_samples_noise_ratio": "min_samples 與 noise ratio",
    "n_components_n_clusters": "n_components 與主題數",
    "n_neighbors_largest_topic_ratio": "n_neighbors 與最大主題比例",
    "selected_topic_size_distributions": "三種候選的主題規模分布",
}


def pct(value: object) -> str:
    return f"{float(value) * 100:.2f}%"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def report_used_rows(report_text: str) -> str | None:
    lines = report_text.splitlines()
    for index, line in enumerate(lines[:-2]):
        if "used_rows" not in line or not line.startswith("|"):
            continue
        headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
        values = [cell.strip() for cell in lines[index + 2].strip().strip("|").split("|")]
        if len(headers) == len(values) and "used_rows" in headers:
            return values[headers.index("used_rows")]
    return None


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
        "best_balance": "在預設平衡條件下，選取 balance score 最高者。",
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
</table></div>
<aside class="table-note"><strong>註記｜最佳平衡的判定：</strong>先篩選 <code>n_clusters ≥ 4</code>、<code>noise ratio ≤ 0.35</code>、<code>最大主題比例 ≤ 0.65</code>、<code>前三主題比例 ≤ 0.85</code> 的組合；再以 <code>balance score = 0.30 × (1 − noise ratio) + 0.30 × (1 − 最大主題比例) + 0.20 × (1 − 前三主題比例) + 0.20 × min(主題數 / 25, 1)</code> 選取最高分。</aside>""".format("".join(body))


def best_balance(rows: list[dict[str, object]]) -> dict[str, object] | None:
    return next((row for row in rows if val(row, "selection_label") == "best_balance"), None)


def same_value(left: object, right: object) -> bool:
    try:
        return abs(float(left) - float(right)) < 1e-9
    except (TypeError, ValueError):
        return str(left) == str(right)


def stability_summary(folder: Path, candidate: dict[str, object] | None) -> str:
    if candidate is None:
        return '<p class="result-empty">未找到最佳平衡候選設定，無法產生穩定性摘要。</p>'
    required = (
        "umap_n_neighbors", "umap_n_components", "umap_min_dist",
        "hdbscan_min_cluster_size", "hdbscan_min_samples",
        "hdbscan_cluster_selection_method", "hdbscan_cluster_selection_epsilon",
        "n_clusters", "noise_ratio", "balance_score",
    )
    matching: list[dict[str, str]] = []
    fields = required[:7]
    for path in folder.glob("*stability*.csv"):
        values = read_csv(path)
        if not values or not all(key in values[0] for key in required):
            continue
        seed_key = "umap_random_state" if "umap_random_state" in values[0] else "random_state"
        if seed_key not in values[0]:
            continue
        current = [row for row in values if all(same_value(row[key], candidate[key]) for key in fields)]
        if len(current) > len(matching):
            matching = current
    if not matching:
        return '<p class="result-empty">原始資料保留穩定性檔案，但沒有與最佳平衡設定完全對應的 seed 結果。</p>'
    seed_key = "umap_random_state" if "umap_random_state" in matching[0] else "random_state"
    seeds = {row[seed_key] for row in matching}
    topics = [float(row["n_clusters"]) for row in matching]
    noise = [float(row["noise_ratio"]) for row in matching]
    scores = [float(row["balance_score"]) for row in matching]
    return """<div class="stability-summary">
<div><span>測試 seed</span><strong>{}</strong></div>
<div><span>主題數範圍</span><strong>{}–{}</strong></div>
<div><span>noise ratio 範圍</span><strong>{}–{}</strong></div>
<div><span>balance score 範圍</span><strong>{:.3f}–{:.3f}</strong></div>
</div>
<p class="stability-note">以最佳平衡參數在不同 random state 下重跑；範圍用於檢視分群結果對初始化的敏感程度。</p>""".format(
        len(seeds), int(min(topics)), int(max(topics)), pct(min(noise)), pct(max(noise)), min(scores), max(scores)
    )


def semantic_summary(folder: Path) -> str:
    model_dir = folder / "final_models" / "best_balance"
    word_path = model_dir / "topic_words.csv"
    if not word_path.is_file():
        return '<p class="result-empty">此實驗未保留最佳平衡的主題詞輸出。</p>'
    representative_path = model_dir / "representative_docs.csv"
    representative: dict[str, str] = {}
    if representative_path.is_file():
        for row in read_csv(representative_path):
            topic = row.get("topic") or row.get("Topic") or ""
            text = row.get("representative_text") or row.get("representative_doc") or ""
            if topic not in representative and text:
                representative[topic] = text
    word_rows = read_csv(word_path)
    rows = []
    if word_rows and "words" in word_rows[0]:
        grouped_words = [(row.get("topic", ""), row.get("words", "")) for row in word_rows]
    else:
        grouped: dict[str, list[tuple[int, str]]] = {}
        for row in word_rows:
            topic = row.get("topic") or row.get("Topic") or ""
            word = row.get("word", "")
            if topic and word:
                grouped.setdefault(topic, []).append((int(row.get("rank", "999") or 999), word))
        grouped_words = [(topic, ", ".join(word for _, word in sorted(words)[:10])) for topic, words in grouped.items()]
    for topic, words in grouped_words:
        if topic == "-1" or not words:
            continue
        text = representative.get(topic, "—")
        if len(text) > 220:
            text = text[:217].rstrip() + "..."
        rows.append((int(topic) if topic.lstrip("-").isdigit() else 999999, topic, words, text))
    rows.sort(key=lambda item: item[0])
    body = "".join(
        "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            html.escape(topic), html.escape(words), html.escape(text)
        )
        for _, topic, words, text in rows[:8]
    )
    if not body:
        return '<p class="result-empty">最佳平衡結果沒有可顯示的有效主題詞。</p>'
    return """<p class="section-intro">以下為最佳平衡結果的前 8 個有效主題；每列保留前 10 個代表詞與第一則代表句，供快速判讀語意品質。</p>
<div class="table-scroll"><table class="semantic-table"><thead><tr><th>主題</th><th>代表詞（前 10）</th><th>代表句</th></tr></thead><tbody>{}</tbody></table></div>""".format(body)


def brand_model_summary(folder: Path) -> str:
    path = folder / "brand_model_topic_word_check.csv"
    if not path.is_file():
        return ""
    rows = [row for row in read_csv(path) if row.get("selection_label") == "best_balance"]
    if not rows:
        return ""
    hit_topics = sum(int(float(row.get("brand_model_hit_count", "0") or 0)) > 0 for row in rows)
    total_hits = sum(int(float(row.get("brand_model_hit_count", "0") or 0)) for row in rows)
    return """<h3>品牌／車款詞彙檢查</h3>
<aside class="table-note">最佳平衡結果中，共檢查 {} 個主題的前 {} 個詞；{} 個主題含有品牌或車款詞彙（合計 {} 次）。此數字用來判讀主題是否仍可能被品牌／車款名稱主導。</aside>""".format(
        len(rows), rows[0].get("top_word_count", "10"), hit_topics, total_hits
    )


def chart_figure(path: Path, asset_dir: Path, slug: str) -> str:
    label = CHART_LABELS.get(path.stem, path.stem.replace("_", " "))
    return (
        '<figure><img src="{{{{ \'/assets/results/{}/{ }\' | relative_url }}}}" alt="{}">'
        '<figcaption>{}</figcaption></figure>'
    ).replace("{ }", path.relative_to(asset_dir).as_posix()).format(
        slug, html.escape(label), html.escape(label)
    )


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
    overview_rows = []
    for folder_name, (slug, title) in EXPERIMENTS.items():
        folder = SOURCE / folder_name
        rows = selected(folder)
        balance_candidate = best_balance(rows)
        log_path = next(iter(folder.glob("*-run_log.json")), None)
        if log_path is None and (folder / "run_log.json").is_file():
            log_path = folder / "run_log.json"
        payload = json.loads(log_path.read_text(encoding="utf-8")) if log_path else {}
        meta = payload.get("dataset_meta") or payload.get("meta") or {}
        report = next(iter(folder.glob("*.md")), None)
        report_text = report.read_text(encoding="utf-8") if report else ""
        match = re.search(r"(?:資料來源|dataset_dir)[：:]?\s*`?([^`\n|]+)", report_text)
        dataset = meta.get("dataset_dir") or payload.get("dataset") or (match.group(1).strip() if match else "-")
        used_rows = meta.get("used_rows") or meta.get("source_rows") or report_used_rows(report_text) or "-"

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
        chart_paths = [path for path in copied if path.suffix.lower() == ".png"]
        key_charts = [path for path in chart_paths if any(x in path.name for x in ("best_three", "parameter_heatmap", "selected_configs"))][:3]
        figures = "".join(chart_figure(path, asset_dir, slug) for path in key_charts)
        figure_block = f'<div class="result-figure-scroller">{figures}</div>' if figures else ""
        remaining_charts = [path for path in chart_paths if path not in key_charts]
        full_chart_block = ""
        if remaining_charts:
            all_figures = "".join(chart_figure(path, asset_dir, slug) for path in remaining_charts)
            full_chart_block = f'''<details class="result-chart-details">
<summary>完整參數圖表（{len(remaining_charts)} 張）</summary>
<p>用於追查各 UMAP／HDBSCAN 參數與主題數、離群比例、主題集中度之間的關係。</p>
<div class="result-figure-scroller">{all_figures}</div>
</details>'''
        stability_block = stability_summary(folder, balance_candidate)
        semantic_block = semantic_summary(folder)
        brand_block = brand_model_summary(folder)
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
<tr><td>來源資料夾</td><td><code>#運行BERTopic整理/#4. UMAP（未整理）/{html.escape(folder_name)}</code></td></tr>
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

## 穩定性檢測

{stability_block}

## 最佳平衡的主題語意摘要

{semantic_block}

{brand_block}

## 圖表檢視

候選策略比較圖用來並列三種策略的主題數、noise ratio 與主題集中度；參數熱圖或選定設定比較圖則用來觀察不同 UMAP／HDBSCAN 組合對分群結果的影響。

{figure_block}

{full_chart_block}

## 原始輸出

{download_table(copied, asset_dir, slug)}
</section>
</div>
'''
        (PAGES / f"{slug}.md").write_text(page, encoding="utf-8")
        overview_links.append(f"[{title}]({{{{ '/results/{slug}.html' | relative_url }}}})")
        if balance_candidate:
            overview_rows.append(
                "<tr><td><a href=\"{{{{ '/results/{}.html' | relative_url }}}}\">{}</a></td>"
                "<td>neighbors {} / components {} / min dist {}</td>"
                "<td>cluster {} / samples {} / {} / eps {}</td>"
                "<td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                    slug, html.escape(title),
                    val(balance_candidate, "umap_n_neighbors"), val(balance_candidate, "umap_n_components"), val(balance_candidate, "umap_min_dist"),
                    val(balance_candidate, "hdbscan_min_cluster_size"), val(balance_candidate, "hdbscan_min_samples"),
                    val(balance_candidate, "hdbscan_cluster_selection_method"), val(balance_candidate, "hdbscan_cluster_selection_epsilon"),
                    val(balance_candidate, "n_clusters"), pct(val(balance_candidate, "noise_ratio", 0)),
                    pct(val(balance_candidate, "largest_topic_ratio", 0)), val(balance_candidate, "balance_score"),
                )
            )
        print(f"Imported {folder_name}")

    (PAGES / "a04-umap-overview.md").write_text(
        "---\ntitle: A04 UMAP 整體比較\ndescription: A04 UMAP 與 HDBSCAN 聯合搜尋結果。\n---\n\n"
        "# A04｜UMAP 整體比較\n\n"
        "A04 階段同時探索 UMAP 降維與 HDBSCAN 分群設定；每個資料版本均保留最低雜訊、最多主題與最佳平衡三種候選策略。\n\n"
        "## 最佳平衡跨資料集比較\n\n"
        "此表將各資料版本的最佳平衡候選並列，便於比較資料處理策略與年份切分造成的差異；分數僅適合搭配 noise ratio、主題數與主題集中度共同解讀。\n\n"
        "<div class=\"table-scroll\"><table class=\"umap-overview-table\"><thead><tr><th>資料版本</th><th>UMAP</th><th>HDBSCAN</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>balance score</th></tr></thead><tbody>"
        + "".join(overview_rows)
        + "</tbody></table></div>\n\n"
        "## 個別實驗\n\n可直接查看：" + "、".join(overview_links) + "。\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    run()
    from build_experiment_registry import sync_registry
    sync_registry(migrate=True)
