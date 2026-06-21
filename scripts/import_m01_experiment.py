#!/usr/bin/env python3
"""Publish the historical M01 three-strategy BERTopic run as Pages views."""

from __future__ import annotations

import ast
import csv
import html
import json
import shutil
from pathlib import Path


SOURCE = Path(
    "/workspaces/Dev-BT/#運行BERTopic整理/#6. M01主程式（三參數-廢用）（未整理）/"
    "M01-8(orig)_tok(para12-80)"
)
ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs/results"
ASSETS = ROOT / "docs/assets/results/m01-8-historical"

LABELS = {
    "lowest_noise": "最低雜訊",
    "most_topics": "最多主題",
    "best_balance": "最佳平衡",
}
METHODS = {
    "lowest_noise": "以最低 noise ratio 為優先，觀察離群句是否最少。",
    "most_topics": "以保留最多有效主題為優先，保留較細的主題切分。",
    "best_balance": "依既定平衡條件與 balance score 選取，兼顧離群、集中度與主題數。",
}
MODELS = {
    "default": "Default c-TF-IDF",
    "keybert": "KeyBERT-Inspired",
    "pos": "Part-of-Speech",
    "mmr": "MMR",
    "llm_anthropic_claude_opus_4_7": "Claude Opus 4.7",
    "llm_openai_gpt_5_5": "GPT-5.5",
    "llm_google_gemini_3_1_pro_preview": "Gemini 3.1 Pro Preview",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pct(value: object) -> str:
    return f"{float(value) * 100:.2f}%"


def code(value: object) -> str:
    return f"<code>{html.escape(str(value))}</code>"


def clean_words(value: str) -> str:
    try:
        words = ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value
    return ", ".join(str(word) for word in words[:10])


def label_name(value: str) -> str:
    return value.split("_", 1)[1] if "_" in value else value


def copy_outputs() -> list[Path]:
    shutil.rmtree(ASSETS, ignore_errors=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for path in SOURCE.iterdir():
        if not path.is_file() or path.suffix in {".npy", ".pyc"}:
            continue
        target = ASSETS / path.name
        shutil.copy2(path, target)
        copied.append(target)
    for strategy in LABELS:
        for path in (SOURCE / strategy).iterdir():
            if not path.is_file() or path.name == "document_topics.csv":
                continue
            target = ASSETS / strategy / path.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            copied.append(target)
    return copied


def config_table(config: dict[str, object]) -> str:
    umap = config["umap"]
    hdbscan = config["hdbscan"]
    return f'''<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td>{code(config['dataset'])}</td></tr>
<tr><td>選擇依據</td><td>{html.escape(str(config['selection_reason']))}</td></tr>
<tr><td>Embedding</td><td>{code(config['embedding_model'])}</td></tr>
<tr><td>UMAP</td><td>neighbors {umap['n_neighbors']} / components {umap['n_components']} / min dist {umap['min_dist']} / {umap['metric']}</td></tr>
<tr><td>HDBSCAN</td><td>cluster {hdbscan['min_cluster_size']} / samples {hdbscan['min_samples']} / {hdbscan['cluster_selection_method']} / eps {hdbscan['cluster_selection_epsilon']}</td></tr>
</tbody></table>'''


def strategy_table(rows: list[dict[str, object]]) -> str:
    body = []
    for row in rows:
        strategy = str(row["selection_label"])
        page = f"/results/m01-8-{strategy.replace('_', '-')}.html"
        body.append(
            '<tr class="candidate-{}"><td><a href="{{{{ \'{}\' | relative_url }}}}">{}</a></td>'
            '<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                strategy,
                page,
                LABELS[strategy],
                html.escape(METHODS[strategy]),
                row["n_clusters"],
                pct(row["noise_ratio"]),
                pct(row["largest_topic_ratio"]),
                pct(row["top3_topic_ratio"]),
                f"{float(row['balance_score']):.4f}",
                row["llm_topic_label_errors"],
            )
        )
    return '''<div class="table-scroll"><table class="candidate-table m01-strategy-table"><thead><tr>
<th>策略</th><th>選擇方式</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>前三主題比例</th><th>balance score</th><th>LLM 命名失敗</th>
</tr></thead><tbody>''' + "".join(body) + "</tbody></table></div>"


def baseline_table(config: dict[str, object]) -> str:
    baseline = config["baseline_metrics"]
    current = config["a06_metrics"]
    metrics = (
        ("有效主題數", "n_clusters", ""),
        ("noise ratio", "noise_ratio", "%"),
        ("最大主題比例", "largest_topic_ratio", "%"),
        ("前三主題比例", "top3_topic_ratio", "%"),
        ("balance score", "balance_score", "score"),
    )
    rows = []
    for title, key, kind in metrics:
        render = (lambda value: pct(value)) if kind == "%" else (lambda value: f"{float(value):.4f}") if kind == "score" else str
        rows.append(f"<tr><td>{title}</td><td>{render(baseline[key])}</td><td>{render(current[key])}</td></tr>")
    return '<div class="table-scroll"><table class="m01-baseline-table"><thead><tr><th>指標</th><th>A04 基準</th><th>M01 結果</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>"


def topic_table(strategy: str) -> str:
    folder = SOURCE / strategy
    default = {row["Topic"]: row for row in read_csv(folder / "topic_info_default.csv")}
    claude = {row["Topic"]: row for row in read_csv(folder / "topic_info_llm_anthropic_claude_opus_4_7.csv")}
    gemini = {row["Topic"]: row for row in read_csv(folder / "topic_info_llm_google_gemini_3_1_pro_preview.csv")}
    rows = []
    for topic, row in default.items():
        if topic == "-1" or len(rows) >= 10:
            continue
        rows.append(
            "<tr><td>{}</td><td>{:,}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                html.escape(topic), int(row["Count"]), html.escape(clean_words(row["Representation"])),
                html.escape(label_name(claude.get(topic, row)["Name"])),
                html.escape(label_name(gemini.get(topic, row)["Name"])),
            )
        )
    return '''<p class="section-intro">分群結果在各表徵方法之間相同；下表以 Default 的代表詞搭配 Claude 與 Gemini 命名，供檢視命名是否有助於主題判讀。僅先列前 10 個有效主題，完整輸出保留在下方。</p>
<div class="table-scroll"><table class="semantic-table m01-topic-table"><thead><tr><th>主題</th><th>句數</th><th>Default 代表詞</th><th>Claude 命名</th><th>Gemini 命名</th></tr></thead><tbody>''' + "".join(rows) + "</tbody></table></div>"


def representation_table(strategy: str) -> str:
    errors = json.loads((SOURCE / strategy / "representation_errors.json").read_text(encoding="utf-8"))
    grouped: dict[str, list[dict[str, object]]] = {}
    for error in errors:
        grouped.setdefault(str(error["representation_model"]), []).append(error)
    rows = []
    for model, display in MODELS.items():
        count = len(grouped.get(model, []))
        status = "完成" if not count else f"{count} 個 topic 命名失敗"
        file_name = f"topic_info_{model}.csv"
        rows.append(
            f'<tr><td>{html.escape(display)}</td><td>{status}</td><td><a href="{{{{ \'/assets/results/m01-8-historical/{strategy}/{file_name}\' | relative_url }}}}">topic info</a></td></tr>'
        )
    error_link = f"{{{{ '/assets/results/m01-8-historical/{strategy}/representation_errors.json' | relative_url }}}}"
    note = (
        f'<aside class="table-note"><strong>LLM 命名狀態：</strong>GPT-5.5 在此策略有 {len(grouped.get("llm_openai_gpt_5_5", []))} 個 topic 因 API 回應缺值而未取得名稱；完整錯誤紀錄見 <a href="{error_link}">representation_errors.json</a>。</aside>'
        if grouped else
        '<aside class="table-note"><strong>LLM 命名狀態：</strong>本策略沒有保留的表徵錯誤。</aside>'
    )
    return '<div class="table-scroll"><table class="m01-representation-table"><thead><tr><th>表徵／命名方式</th><th>狀態</th><th>完整輸出</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>" + note


def downloads(strategy: str) -> str:
    descriptions = {
        "final_config.json": "此策略的 UMAP、HDBSCAN、停用詞與表徵模型設定",
        "topic_size_distribution.csv": "各 topic 的句數與比例",
        "representative_docs.csv": "各主題的代表文本",
        "topic_info.csv": "預設主題資訊",
        "topic_words.csv": "預設主題詞",
        "representation_errors.json": "LLM 命名與表徵失敗紀錄",
    }
    rows = []
    for name, description in descriptions.items():
        rows.append(f'<tr><td><a href="{{{{ \'/assets/results/m01-8-historical/{strategy}/{name}\' | relative_url }}}}">{name}</a></td><td>{description}</td></tr>')
    for model, display in MODELS.items():
        rows.append(f'<tr><td><a href="{{{{ \'/assets/results/m01-8-historical/{strategy}/topic_info_{model}.csv\' | relative_url }}}}">topic_info_{model}.csv</a></td><td>{display} 的主題表徵或命名輸出</td></tr>')
    return '<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>"


def write_detail(strategy: str, summary: dict[str, object]) -> None:
    config = json.loads((SOURCE / strategy / "final_config.json").read_text(encoding="utf-8"))
    label = LABELS[strategy]
    page = f'''---
title: M01-8 {label}
description: M01-8 歷史主程式的 {label} BERTopic 結果。
---

# M01-8｜{label}

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

{config_table(config)}

### 停用詞與命名

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>停用詞來源</td><td><a href="{{{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}}}">A05-8.4 human</a></td></tr>
<tr><td>客製停用詞</td><td>{config['custom_stopwords_count']} 個；合併英文停用詞共 462 個</td></tr>
<tr><td>LLM Provider</td><td>{html.escape(str(config['llm_provider']))}</td></tr>
<tr><td>LLM models</td><td>{html.escape(' / '.join(config['llm_models']))}</td></tr>
</tbody></table>

### 導覽

<p><a href="{{{{ '/results/m01-8-historical.html' | relative_url }}}}">回到 M01 三策略總覽</a></p>
</aside>

<section markdown="1">
<aside class="table-note"><strong>歷史比較用途：</strong>此頁對應資料夾「M01主程式（三參數-廢用）」。保留它是為了追溯三種策略與 A05-8.4 human 停用詞導入後的結果，不作為後續 M02 正式模型的唯一依據。</aside>

<div class="run-summary">
<div class="run-stat"><strong>{summary['n_clusters']}</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>{pct(summary['noise_ratio'])}</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>{pct(summary['largest_topic_ratio'])}</strong><span>最大主題比例</span></div>
<div class="run-stat"><strong>{float(summary['balance_score']):.4f}</strong><span>balance score</span></div>
</div>

## 結果摘要

{METHODS[strategy]} 本次使用 11,136 句資料，並重用 A04-8 的 embedding 快取。A05-8.4 human 停用詞僅作用於 c-TF-IDF 與主題表徵；embedding 與 HDBSCAN 分群仍使用原始 orig 文本向量。

## 與 A04 基準的對照

{baseline_table(config)}

## 主題語意與 LLM 命名

{topic_table(strategy)}

## 表徵方法與錯誤紀錄

{representation_table(strategy)}

## 原始輸出

{downloads(strategy)}
</section>
</div>
'''
    (PAGES / f"m01-8-{strategy.replace('_', '-')}.md").write_text(page, encoding="utf-8")


def write_overview(rows: list[dict[str, object]]) -> None:
    links = "".join(
        f'<a class="m01-strategy-link candidate-{row["selection_label"]}" href="{{{{ \'/results/m01-8-{str(row["selection_label"]).replace("_", "-")}.html\' | relative_url }}}}"><strong>{LABELS[str(row["selection_label"])]}</strong><span>{METHODS[str(row["selection_label"])]}</span></a>'
        for row in rows
    )
    page = f'''---
title: M01-8 三策略主程式
description: M01-8 歷史主程式的三種 BERTopic 策略比較。
---

# M01-8｜三策略主程式

<aside class="table-note"><strong>歷史比較用途：</strong>本頁整理「M01主程式（三參數-廢用）」中唯一完整的 M01-8 實驗。保留其資料來源、三種策略、停用詞與 LLM 命名結果，供研究追溯；它不取代後續 M02 的正式單一參數模型。</aside>

<div class="m01-strategy-links">{links}</div>

## 運行設定

<div class="run-summary">
<div class="run-stat"><strong>11,136</strong><span>使用句子</span></div>
<div class="run-stat"><strong>170</strong><span>A05-8.4 human 客製停用詞</span></div>
<div class="run-stat"><strong>462</strong><span>合併英文停用詞總數</span></div>
<div class="run-stat"><strong>7</strong><span>主題表徵／命名方式</span></div>
</div>

資料使用 <code>Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok(para12-80)_dataset</code>，重用 A04-8 的 <code>all-MiniLM-L6-v2</code> embedding 快取。客製停用詞取自 <a href="{{{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}}}">A05-8.4 human</a>；它只影響 c-TF-IDF／主題表徵，並不改變 embedding 或 HDBSCAN 分群輸入。

## 三策略比較

{strategy_table(rows)}

<aside class="table-note"><strong>如何判讀：</strong>最低雜訊策略雖使離群句較少，但最大主題高度集中；最多主題策略的 balance score 最高，但 LLM 命名失敗也較多；最佳平衡策略則在較低雜訊與 51 個主題之間取得另一種取捨。三者均保留，供語意品質的人工檢閱。</aside>

## 資料與原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody>
<tr><td><a href="{{{{ '/assets/results/m01-8-historical/M01-8_comparison_summary.csv' | relative_url }}}}">M01-8_comparison_summary.csv</a></td><td>三種策略的量化比較摘要</td></tr>
<tr><td><a href="{{{{ '/assets/results/m01-8-historical/M01-8_run_log.json' | relative_url }}}}">M01-8_run_log.json</a></td><td>資料、停用詞、embedding 快取與 LLM 執行紀錄</td></tr>
<tr><td><a href="{{{{ '/assets/results/m01-8-historical/M01-8_custom_stopwords_used.txt' | relative_url }}}}">M01-8_custom_stopwords_used.txt</a></td><td>本次實際使用的客製停用詞清單</td></tr>
<tr><td><a href="{{{{ '/assets/results/m01-8-historical/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py' | relative_url }}}}">執行程式</a></td><td>M01-8 主程式與表徵模型執行流程</td></tr>
</tbody></table>
'''
    (PAGES / "m01-8-historical.md").write_text(page, encoding="utf-8")


def run() -> None:
    copy_outputs()
    rows = json.loads((SOURCE / "M01-8_run_summary.json").read_text(encoding="utf-8"))
    for row in rows:
        write_detail(str(row["selection_label"]), row)
    write_overview(rows)


if __name__ == "__main__":
    run()
