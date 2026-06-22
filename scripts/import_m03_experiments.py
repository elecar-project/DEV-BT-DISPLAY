#!/usr/bin/env python3
"""Publish the two M03 year-split BERTopic runs and LLM50 validation."""

from __future__ import annotations

import csv
import html
import json
import shutil
from pathlib import Path


SOURCE = Path("/workspaces/Dev-BT/#運行BERTopic整理/#8. M03主程式（切年份）（未整理）")
ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs/results"
ASSETS = ROOT / "docs/assets/results"

EXPERIMENTS = {
    "m03-2020-before": {
        "folder": "06.17_M03-1(orig_08-19_tp-50)",
        "title": "2020 前｜年份切分",
        "period": "2008-2019",
        "validation": "06.17_M03-1(orig_08-19_tp-50)_LLM_validation.csv",
        "includes_outlier": True,
    },
    "m03-2020-after": {
        "folder": "06.17_M03-2(orig_20-25_tp-50)",
        "title": "2020 後｜年份切分",
        "period": "2020-2025",
        "validation": "06.17_M03-2(orig_20-25_tp-50)_LLM_validation.csv",
        "includes_outlier": False,
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pct(value: object) -> str:
    return f"{float(value) * 100:.2f}%"


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


def config_values(config: dict[str, object]) -> dict[str, object]:
    return config.get("metrics") or config.get("m02_metrics") or {}


def settings(config: dict[str, object], run_log: dict[str, object]) -> str:
    umap = config["umap"]
    hdbscan = config["hdbscan"]
    return f'''<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>{html.escape(str(config['dataset']))}</code></td></tr>
<tr><td>可用句子</td><td>{int(run_log['rows']):,}</td></tr>
<tr><td>Embedding</td><td><code>{html.escape(str(config['embedding_model']))}</code></td></tr>
<tr><td>UMAP</td><td>neighbors {umap['n_neighbors']} / components {umap['n_components']} / min dist {umap['min_dist']} / {umap['metric']}</td></tr>
<tr><td>HDBSCAN</td><td>cluster {hdbscan['min_cluster_size']} / samples {hdbscan['min_samples']} / {hdbscan['cluster_selection_method']} / eps {hdbscan['cluster_selection_epsilon']}</td></tr>
<tr><td>Topic reduction</td><td><code>nr_topics={config['nr_topics']}</code></td></tr>
</tbody></table>

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>停用詞</td><td><a href="{{{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}}}">A05-8.4 human</a>，客製 {config['custom_stopwords_count']} 個</td></tr>
<tr><td>LLM</td><td>{html.escape(str(config['llm_provider']))} / <code>{html.escape(str(config['llm_model']))}</code></td></tr>
<tr><td>命名次數</td><td>每個 topic 50 次</td></tr>
<tr><td>代表句</td><td>{config['representative_docs_per_topic']} 句 / topic</td></tr>
</tbody></table>'''


def validation_table(rows: list[dict[str, str]]) -> str:
    body = []
    for row in rows:
        stable = row["stable"] == "True"
        topic = "-1（noise）" if row["topic"] == "-1" else row["topic"]
        body.append(
            '<tr class="{}"><td>{}</td><td>{}/{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><span class="{}">{}</span></td></tr>'.format(
                "validation-stable" if stable else "validation-review",
                html.escape(topic), row["successful_runs"], row["runs_requested"],
                html.escape(row["mode_label"]), html.escape(row["keywords"]), row["unique_normalized_labels"],
                f"{float(row['mode_ratio']):.2%} / {float(row['avg_jaccard_to_mode']):.3f}",
                "validation-badge stable" if stable else "validation-badge review",
                "穩定" if stable else "建議檢查",
            )
        )
    return '''<div class="table-scroll"><table class="m02-validation-table"><thead><tr>
<th>Topic</th><th>成功／要求</th><th>主要命名</th><th>代表詞</th><th>不同命名數</th><th>mode ratio / Jaccard</th><th>判定</th>
</tr></thead><tbody>''' + "".join(body) + "</tbody></table></div>"


def output_table(slug: str, copied: list[Path]) -> str:
    descriptions = {
        "LLM_validation": "LLM 50 次驗證結果與穩定性判定",
        "_LLM.md": "LLM 命名輸出或驗證報告",
        "LLM_prompts": "LLM 提示詞與輸入紀錄",
        "combined_representations": "Default、KeyBERT、POS、MMR 與 LLM 表徵對照",
        "final_config": "最終模型與 LLM 設定",
        "run_log": "執行資料、停用詞與快取紀錄",
        "run_summary": "模型量化結果摘要",
        "summary.csv": "模型量化結果摘要 CSV",
        "representation_errors": "表徵與 LLM 命名錯誤紀錄",
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


def write_page(slug: str, spec: dict[str, object]) -> None:
    source = SOURCE / str(spec["folder"])
    artifact = source / "artifacts"
    config = json.loads((artifact / "final_config.json").read_text(encoding="utf-8"))
    run_log = json.loads(next(source.glob("*_run_log.json")).read_text(encoding="utf-8"))
    validation = read_csv(source / str(spec["validation"]))
    copied = copy_outputs(slug, source)
    metrics = config_values(config)
    stable = sum(row["stable"] == "True" for row in validation)
    successful = sum(int(row["successful_runs"]) for row in validation)
    requested = sum(int(row["runs_requested"]) for row in validation)
    error_runs = sum(int(row["error_runs"]) for row in validation)
    representation_errors = json.loads((artifact / "representation_errors.json").read_text(encoding="utf-8"))
    validation_scope = "包含 noise topic -1，故驗證 topic 數可能比有效主題數多 1。" if spec["includes_outlier"] else "僅針對有效主題進行驗證。"
    other_link = "/results/m03-2020-after.html" if slug == "m03-2020-before" else "/results/m03-2020-before.html"
    other_title = "2020 後" if slug == "m03-2020-before" else "2020 前"
    page = f'''---
title: {spec['title']}
description: M03 年份切分後的 {spec['period']} BERTopic 結果與 LLM50 命名驗證。
---

# {spec['title']}

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料與模型

{settings(config, run_log)}

### 來源資料夾

<p><code>#運行BERTopic整理/#8. M03主程式（切年份）（未整理）/{html.escape(str(spec['folder']))}</code></p>

<p><a href="{{{{ '{other_link}' | relative_url }}}}">查看 {other_title} 年份切分結果</a></p>
</aside>

<section markdown="1">
<div class="run-summary">
<div class="run-stat"><strong>{metrics['n_clusters']}</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>{pct(metrics['noise_ratio'])}</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>{stable} / {len(validation)}</strong><span>穩定命名主題</span></div>
<div class="run-stat"><strong>{float(metrics['balance_score']):.3f}</strong><span>balance score</span></div>
</div>

## 結果摘要

此模型將資料依年份切為 {spec['period']}，用以比較不同時期的 EV 產品文本能否產生不同的主題結構。兩個年份分組各自使用選定的單一 UMAP／HDBSCAN 組合，因此主題數與集中度應搭配資料期間與參數共同判讀，而非只看單一分數。

<aside class="table-note"><strong>驗證範圍：</strong>{validation_scope} A05-8.4 human 停用詞僅作用於 c-TF-IDF／主題表徵，不會改變 embedding 與 HDBSCAN 分群輸入。</aside>

## LLM 命名穩定性

<p class="section-intro">穩定判定規則為 <code>mode_ratio ≥ 0.70</code> 或 <code>avg_jaccard_to_mode ≥ 0.65</code>。mode ratio 表示最常出現名稱的比例；Jaccard 指標則衡量其餘命名與主要命名的詞彙重疊程度。</p>

{validation_table(validation)}

<aside class="table-note"><strong>呼叫狀態：</strong>{successful:,} / {requested:,} 次驗證呼叫成功；驗證 CSV 記錄的空白或失敗呼叫為 {error_runs} 次。另有 {len(representation_errors)} 筆表徵／命名錯誤紀錄，保留於 <code>representation_errors.json</code>。</aside>

## 原始輸出

{output_table(slug, copied)}
</section>
</div>
'''
    (PAGES / f"{slug}.md").write_text(page, encoding="utf-8")


def run() -> None:
    for slug, spec in EXPERIMENTS.items():
        write_page(slug, spec)


if __name__ == "__main__":
    run()
    from build_experiment_registry import sync_registry
    sync_registry(migrate=True)
