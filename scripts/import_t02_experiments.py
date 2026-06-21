#!/usr/bin/env python3
"""Publish T02 year-boundary validation experiments."""

from __future__ import annotations

import ast
import csv
import html
import json
import shutil
from pathlib import Path


SOURCE = Path("/workspaces/Dev-BT/#運行BERTopic整理/#8.1 T03不同年份切段")
ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs/results"
ASSETS = ROOT / "docs/assets/results"

EXPERIMENTS = {
    "t02-2018-before": ("06.17_T02-1(orig_08-17_tp-X)", "2018 前", "2008-2017", "以 2018 為切點的前段資料。", "mRq0KLDsOoRAvhbJz9B0-89"),
    "t02-2018-after": ("06.17_T02-2(orig_18-25_tp-X)", "2018 後", "2018-2025", "以 2018 為切點的後段資料。", "mRq0KLDsOoRAvhbJz9B0-90"),
    "t02-2019-before": ("06.17_T02-3(orig_08-18_tp-X)", "2019 前", "2008-2018", "以 2019 為切點的前段資料。", "mRq0KLDsOoRAvhbJz9B0-92"),
    "t02-2019-after": ("06.17_T02-4(orig_19-25_tp-X)", "2019 後", "2019-2025", "以 2019 為切點的後段資料。", "mRq0KLDsOoRAvhbJz9B0-91"),
    "t02-2021-before": ("06.17_T02-5(orig_08-20_tp-X)", "2021 前", "2008-2020", "以 2021 為切點的前段資料。", "mRq0KLDsOoRAvhbJz9B0-93"),
    "t02-2021-after": ("06.17_T02-6(orig_21-25_tp-X)", "2021 後", "2021-2025", "以 2021 為切點的後段資料。", "mRq0KLDsOoRAvhbJz9B0-94"),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pct(value: object) -> str:
    return f"{float(value) * 100:.2f}%"


def words(value: str) -> str:
    try:
        return ", ".join(str(item) for item in ast.literal_eval(value)[:10])
    except (ValueError, SyntaxError):
        return value


def metrics(config: dict[str, object], log: dict[str, object]) -> dict[str, object]:
    values = config.get("metrics") or config.get("m02_metrics") or log.get("metrics") or {}
    if "n_topics_without_noise" in values and "n_clusters" not in values:
        values["n_clusters"] = values["n_topics_without_noise"]
    return values


def copy_outputs(slug: str, source: Path) -> list[Path]:
    target_root = ASSETS / slug
    shutil.rmtree(target_root, ignore_errors=True)
    target_root.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for path in source.rglob("*"):
        if not path.is_file() or path.suffix in {".npy", ".pyc", ".jsonl"}:
            continue
        if path.name == "document_topics.csv" or path.stat().st_size > 3_000_000:
            continue
        target = target_root / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied.append(target)
    return copied


def settings(config: dict[str, object], log: dict[str, object]) -> str:
    umap = config["umap"]
    hdbscan = config["hdbscan"]
    stopword_count = config.get("custom_stopword_count", config.get("custom_stopwords_count", "未記錄"))
    return f'''<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>{html.escape(str(config['dataset']))}</code></td></tr>
<tr><td>可用句子</td><td>{int(log['rows']):,}</td></tr>
<tr><td>Embedding</td><td><code>{html.escape(str(config['embedding_model']))}</code></td></tr>
<tr><td>UMAP</td><td>neighbors {umap['n_neighbors']} / components {umap['n_components']} / min dist {umap['min_dist']} / {umap['metric']}</td></tr>
<tr><td>HDBSCAN</td><td>cluster {hdbscan['min_cluster_size']} / samples {hdbscan['min_samples']} / {hdbscan['cluster_selection_method']} / eps {hdbscan['cluster_selection_epsilon']}</td></tr>
<tr><td>Topic reduction</td><td><code>nr_topics={config['nr_topics']}</code></td></tr>
</tbody></table>
<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>停用詞</td><td><a href="{{{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}}}">A05-8.4 human</a>，客製 {stopword_count} 個</td></tr>
<tr><td>LLM 設計</td><td>未設定／未執行</td></tr>
<tr><td>代表句</td><td>{config['representative_docs_per_topic']} 句 / topic</td></tr>
</tbody></table>'''


def topic_table(source: Path) -> str:
    rows = read_csv(source / "artifacts/topic_info_default.csv")
    body = []
    for row in rows:
        if row["Topic"] == "-1" or len(body) >= 10:
            continue
        body.append("<tr><td>{}</td><td>{:,}</td><td>{}</td></tr>".format(
            html.escape(row["Topic"]), int(row["Count"]), html.escape(words(row["Representation"]))
        ))
    return '<div class="table-scroll"><table class="semantic-table"><thead><tr><th>Topic</th><th>句數</th><th>Default 代表詞（前 10）</th></tr></thead><tbody>' + "".join(body) + "</tbody></table></div>"


def output_table(slug: str, copied: list[Path]) -> str:
    descriptions = {
        "LLM_validation": "LLM 驗證輸出；本次未執行或未保留可用結果",
        "_LLM.md": "LLM 命名輸出或報告",
        "combined_representations": "Default、KeyBERT、POS、MMR 表徵對照",
        "final_config": "最終模型設定",
        "run_log": "執行資料與參數紀錄",
        "run_summary": "模型量化結果摘要",
        "summary.csv": "模型量化結果摘要 CSV",
        "representation_errors": "表徵與 LLM 錯誤紀錄",
        "topic_info": "主題資訊與表徵輸出",
        "topic_words": "主題代表詞輸出",
        "representative_docs": "各主題代表文本",
        "topic_size_distribution": "主題大小分布",
        "custom_stopwords": "本次實際使用的客製停用詞",
    }
    rows = []
    for path in sorted(copied):
        relative = path.relative_to(ASSETS / slug).as_posix()
        purpose = next((text for key, text in descriptions.items() if key in path.name), "原始實驗輸出")
        rows.append(f'<tr><td><a href="{{{{ \'/assets/results/{slug}/{relative}\' | relative_url }}}}">{html.escape(relative)}</a></td><td>{purpose}</td></tr>')
    return '<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>"


def write_detail(slug: str, item: tuple[str, str, str, str, str]) -> dict[str, object]:
    folder, label, period, description, _ = item
    source = SOURCE / folder
    config = json.loads((source / "artifacts/final_config.json").read_text(encoding="utf-8"))
    log = json.loads(next(source.glob("*_run_log.json")).read_text(encoding="utf-8"))
    values = metrics(config, log)
    copied = copy_outputs(slug, source)
    page = f'''---
title: T02 {label} 年份切分
description: T02 年份切分驗證：{period}。
---

# T02｜{label}（{period}）

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料與模型

{settings(config, log)}

### 來源資料夾

<p><code>#運行BERTopic整理/#8.1 T03不同年份切段/{html.escape(folder)}</code></p>
<p><a href="{{{{ '/results/t02-overview.html' | relative_url }}}}">回到 T02 年份切分驗證總覽</a></p>
</aside>

<section markdown="1">
<div class="run-summary">
<div class="run-stat"><strong>{values['n_clusters']}</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>{pct(values['noise_ratio'])}</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>{pct(values['largest_topic_ratio'])}</strong><span>最大主題比例</span></div>
<div class="run-stat"><strong>{float(values['balance_score']):.3f}</strong><span>balance score</span></div>
</div>

## 結果摘要

{description} 此頁用於與同一年度切點的另一側資料比較，檢查不同年份界線是否改變主題結構、離群比例或主題集中度。

<aside class="table-note"><strong>LLM 狀態：</strong>原始輸出未保留可用的 LLM 命名驗證結果，因此本頁標示為「未設定／未執行」。Default、KeyBERT、POS 與 MMR 的主題表徵輸出均已保留。</aside>

## 預設主題語意摘要

<p class="section-intro">以下列出前 10 個有效主題的 Default c-TF-IDF 代表詞，供比較不同年份切分後的主題內容。</p>

{topic_table(source)}

## 原始輸出

{output_table(slug, copied)}
</section>
</div>
'''
    (PAGES / f"{slug}.md").write_text(page, encoding="utf-8")
    return {"slug": slug, "label": label, "period": period, "metrics": values, "rows": log["rows"], "description": description}


def write_overview(items: list[dict[str, object]]) -> None:
    rows = []
    for item in items:
        m = item["metrics"]
        rows.append(f'<tr><td><a href="{{{{ \'/results/{item["slug"]}.html\' | relative_url }}}}">{item["label"]}</a></td><td>{item["period"]}</td><td>{item["rows"]:,}</td><td>{m["n_clusters"]}</td><td>{pct(m["noise_ratio"])}</td><td>{pct(m["largest_topic_ratio"])}</td><td>{float(m["balance_score"]):.3f}</td></tr>')
    page = '''---
title: T02 年份切分驗證
description: 以 2018、2019、2021 為界的年份切分 BERTopic 驗證。
---

# T02｜年份切分驗證

T02 分別以 2018、2019、2021 為切點，將同一資料脈絡分成前後兩段，檢查不同年份劃分下的主題結構是否穩定。各組使用原始輸出記錄的單一模型設定，因此比較時需同時閱讀切分期間與 UMAP／HDBSCAN 參數。

<aside class="table-note"><strong>LLM 狀態：</strong>這六份原始輸出未保留可用的 LLM 命名驗證結果。網站保留既有 BERTopic 與非 LLM 表徵結果，並一律標示為「未設定／未執行」。</aside>

## 六種年份分段比較

<div class="table-scroll"><table class="m01-strategy-table"><thead><tr><th>節點</th><th>資料期間</th><th>句數</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>balance score</th></tr></thead><tbody>''' + "".join(rows) + '''</tbody></table></div>

## 個別結果

流程圖中的六個 T02 綠色節點可直接進入對應結果頁。
'''
    (PAGES / "t02-overview.md").write_text(page, encoding="utf-8")


def run() -> None:
    items = [write_detail(slug, item) for slug, item in EXPERIMENTS.items()]
    write_overview(items)


if __name__ == "__main__":
    run()
