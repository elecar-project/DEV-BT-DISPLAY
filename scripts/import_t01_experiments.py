#!/usr/bin/env python3
"""Publish T01 deletion/replacement validation results."""

from __future__ import annotations

import ast
import csv
import html
import json
import shutil
from pathlib import Path


SOURCE = Path("/workspaces/Dev-BT/#運行BERTopic整理/#7.1 T01刪&移廠商、模型與原版的比較（未整理）")
ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs/results"
ASSETS = ROOT / "docs/assets/results"

EXPERIMENTS = {
    "t01-del": {
        "folder": "06.08_Test1-1(del-new-tp-X)",
        "title": "T01-3｜刪除品牌／車款",
        "method": "del",
        "description": "將品牌與車款名稱從資料集中刪除，檢查移除專有名詞後主題結構的變化。",
    },
    "t01-repl": {
        "folder": "06.08_Test1-2(repl-new-tp-X)",
        "title": "T01-6｜替換品牌／車款",
        "method": "repl",
        "description": "將品牌與車款名稱分別替換為 Brand／Model，保留詞類位置但降低特定品牌名稱的主導性。",
    },
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
<tr><td>LLM 設計</td><td>未設定／未執行</td></tr>
<tr><td>代表句</td><td>{config['representative_docs_per_topic']} 句 / topic</td></tr>
</tbody></table>'''


def topic_table(source: Path) -> str:
    rows = read_csv(source / "artifacts/topic_info_default.csv")
    body = []
    for row in rows:
        if row["Topic"] == "-1" or len(body) >= 10:
            continue
        body.append(
            "<tr><td>{}</td><td>{:,}</td><td>{}</td></tr>".format(
                html.escape(row["Topic"]), int(row["Count"]), html.escape(words(row["Representation"]))
            )
        )
    return '<div class="table-scroll"><table class="semantic-table"><thead><tr><th>Topic</th><th>句數</th><th>Default 代表詞（前 10）</th></tr></thead><tbody>' + "".join(body) + "</tbody></table></div>"


def output_table(slug: str, copied: list[Path]) -> str:
    descriptions = {
        "LLM_validation": "LLM50 驗證輸出；本次因 API key 缺失而跳過",
        "_LLM.md": "LLM 命名輸出或驗證報告",
        "combined_representations": "Default、KeyBERT、POS、MMR 與 LLM 表徵對照",
        "final_config": "最終模型與 LLM 設定",
        "run_log": "執行資料、停用詞與錯誤紀錄",
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


def write_detail(slug: str, spec: dict[str, object]) -> dict[str, object]:
    source = SOURCE / str(spec["folder"])
    artifact = source / "artifacts"
    config = json.loads((artifact / "final_config.json").read_text(encoding="utf-8"))
    run_log = json.loads(next(source.glob("*_run_log.json")).read_text(encoding="utf-8"))
    summary = json.loads(next(source.glob("*_run_summary.json")).read_text(encoding="utf-8"))[0]
    copied = copy_outputs(slug, source)
    metrics = config["m02_metrics"]
    page = f'''---
title: {spec['title']}
description: T01 品牌與車款文字處理驗證：{spec['method']}。
---

# {spec['title']}

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料與模型

{settings(config, run_log)}

### 來源資料夾

<p><code>#運行BERTopic整理/#7.1 T01刪&移廠商、模型與原版的比較（未整理）/{html.escape(str(spec['folder']))}</code></p>

<p><a href="{{{{ '/results/t01-overview.html' | relative_url }}}}">回到 T01 刪除／替換驗證總覽</a></p>
</aside>

<section markdown="1">
<div class="run-summary">
<div class="run-stat"><strong>{metrics['n_clusters']}</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>{pct(metrics['noise_ratio'])}</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>{pct(metrics['largest_topic_ratio'])}</strong><span>最大主題比例</span></div>
<div class="run-stat"><strong>{float(metrics['balance_score']):.3f}</strong><span>balance score</span></div>
</div>

## 結果摘要

{spec['description']} 此頁用來與原始語料及另一種處理方式比較，判讀品牌／車款名稱是否主導主題結構。

<aside class="table-note"><strong>LLM50 未執行：</strong>本次分群與 Default、KeyBERT、POS、MMR 表徵皆已輸出；但當時未提供 <code>OPENROUTER_API_KEY</code>，因此 LLM topic label 與 50 次穩定性驗證被跳過。這不是「0 個穩定主題」，而是沒有可判定的 LLM 驗證結果。</aside>

## 預設主題語意摘要

<p class="section-intro">以下列出前 10 個有效主題的 Default c-TF-IDF 代表詞；可作為檢查刪除或替換後是否仍殘留品牌／車款語意的起點。</p>

{topic_table(source)}

## 原始輸出

{output_table(slug, copied)}
</section>
</div>
'''
    (PAGES / f"{slug}.md").write_text(page, encoding="utf-8")
    return {"slug": slug, "spec": spec, "metrics": metrics, "rows": run_log["rows"]}


def write_overview(results: list[dict[str, object]]) -> None:
    rows = []
    for item in results:
        spec = item["spec"]
        metrics = item["metrics"]
        rows.append(
            f'<tr><td><a href="{{{{ \'/results/{item["slug"]}.html\' | relative_url }}}}">{html.escape(str(spec["method"]))}</a></td><td>{html.escape(str(spec["description"]))}</td><td>{item["rows"]:,}</td><td>{metrics["n_clusters"]}</td><td>{pct(metrics["noise_ratio"])}</td><td>{pct(metrics["largest_topic_ratio"])}</td><td>{float(metrics["balance_score"]):.3f}</td><td>未執行</td></tr>'
        )
    page = '''---
title: T01 刪除與替換驗證
description: 比較刪除與替換品牌／車款名稱對 BERTopic 主題結構的影響。
---

# T01｜刪除與替換品牌／車款驗證

T01 固定 M02 類型的單一 UMAP／HDBSCAN 設定，將同一研究問題分別用刪除品牌／車款詞（del）與替換為 Brand／Model（repl）處理，檢查資料處理方法是否影響主題數、離群比例與主題集中度。

<aside class="table-note"><strong>閱讀方式：</strong>del 直接移除專有名詞；repl 保留語句中的詞類位置，但以 Brand／Model 取代特定名稱。兩者都應和原始語料的結果一併判讀，而非只比較單一 balance score。</aside>

## 結果比較

<div class="table-scroll"><table class="m01-strategy-table"><thead><tr><th>處理方式</th><th>資料處理意義</th><th>句數</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>balance score</th><th>LLM50</th></tr></thead><tbody>''' + "".join(rows) + '''</tbody></table></div>

<aside class="table-note"><strong>LLM 驗證狀態：</strong>兩份實驗均因缺少 <code>OPENROUTER_API_KEY</code> 而未執行 LLM50 命名與穩定性驗證；網站保留該錯誤與原始輸出，避免將未執行誤讀為驗證失敗。</aside>

## 個別結果

可進入 [T01-3｜刪除品牌／車款]({{ '/results/t01-del.html' | relative_url }}) 與 [T01-6｜替換品牌／車款]({{ '/results/t01-repl.html' | relative_url }}) 查看完整模型設定、主題摘要與輸出檔。
'''
    (PAGES / "t01-overview.md").write_text(page, encoding="utf-8")


def run() -> None:
    results = [write_detail(slug, spec) for slug, spec in EXPERIMENTS.items()]
    write_overview(results)


if __name__ == "__main__":
    run()
    from build_experiment_registry import sync_registry
    sync_registry(migrate=True)
