from __future__ import annotations

import json
import sys
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bertopic import BERTopic
from datasets import load_from_disk
from hdbscan import HDBSCAN
from matplotlib.ticker import FuncFormatter, MaxNLocator
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP


ROOT = Path(__file__).resolve().parents[3]
DATASET_DIR = ROOT / "Result/06.13_[B]tok/06.13_[B]01-pre_LLM(orig)_08-19(240)_tok(para12-80)_dataset"
OUTPUT_DIR = ROOT / "Result/06.13_[C]min/[B]01-(orig)_08-19(240)_tok(para12-80)"

RUN_LABEL = "06.13_[C]min_[B]01-(orig)_08-19(240)_tok(para12-80)"
FILE_STEM = "Result_06.13_[C]min_[B]01-(orig)_08-19(240)_tok(para12-80)"

REPORT_PATH = OUTPUT_DIR / f"{FILE_STEM}.md"
MIN_TEST_CSV = OUTPUT_DIR / f"{FILE_STEM}-min_cluster_size.csv"
BEST_TOPIC_INFO_CSV = OUTPUT_DIR / f"{FILE_STEM}-best_topic_info.csv"
BEST_DOC_TOPICS_CSV = OUTPUT_DIR / f"{FILE_STEM}-best_document_topics.csv"
RUN_LOG_JSON = OUTPUT_DIR / f"{FILE_STEM}-run_log.json"
CHART_PATH = OUTPUT_DIR / "[B]01-(orig)_08-19(240)_tok(para12-80)_min_cluster_chart.png"
CHART_SVG_PATH = CHART_PATH.with_suffix(".svg")
CACHE_DIR = OUTPUT_DIR / "cache"
EMBEDDINGS_CACHE = CACHE_DIR / "embeddings_all-MiniLM-L6-v2.npy"
UMAP_CACHE = CACHE_DIR / "umap_nn15_nc5_md0p0_cosine_rs42.npy"

CLUSTER_SIZES = [
    50,
    75,
    100,
    125,
    150,
    175,
    200,
    225,
    250,
    275,
    300,
    325,
    350,
    375,
    400,
    500,
    600,
    700,
    800,
    900,
    1000,
]


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = []
        for col in columns:
            value = row.get(col, "")
            text = "" if value is None else str(value)
            values.append(text.replace("\n", "<br>").replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"


def load_documents() -> tuple[list[str], pd.DataFrame, dict[str, Any], list[dict[str, str]]]:
    dataset = load_from_disk(str(DATASET_DIR))
    columns = list(dataset.column_names)
    text_col = "sentence" if "sentence" in columns else columns[0]

    records: list[dict[str, Any]] = []
    empty_rows: list[int] = []
    short_rows: list[int] = []
    for idx, item in enumerate(dataset):
        text = "" if item.get(text_col) is None else str(item.get(text_col)).strip()
        if not text:
            empty_rows.append(idx)
            continue
        record = {column: item.get(column) for column in columns}
        record["dataset_row"] = idx
        record["document"] = text
        records.append(record)
        if len(text.split()) < 3:
            short_rows.append(idx)

    documents = [str(record["document"]) for record in records]
    doc_meta = pd.DataFrame(records)
    lengths = [len(doc) for doc in documents]
    word_counts = [len(doc.split()) for doc in documents]
    meta = {
        "dataset_dir": str(DATASET_DIR.relative_to(ROOT)),
        "columns": columns,
        "text_col": text_col,
        "source_rows": len(dataset),
        "used_rows": len(documents),
        "empty_rows_count": len(empty_rows),
        "empty_rows_sample": empty_rows[:20],
        "short_rows_lt_3_words_count": len(short_rows),
        "short_rows_lt_3_words_sample": short_rows[:20],
        "min_text_len": min(lengths, default=0),
        "max_text_len": max(lengths, default=0),
        "avg_text_len": float(np.mean(lengths)) if lengths else 0.0,
        "min_word_count": min(word_counts, default=0),
        "max_word_count": max(word_counts, default=0),
        "avg_word_count": float(np.mean(word_counts)) if word_counts else 0.0,
    }

    notices: list[dict[str, str]] = []
    if empty_rows:
        notices.append({"流程": "前處理", "問題": f"有 {len(empty_rows)} 筆空白文本已排除。"})
    if short_rows:
        notices.append({"流程": "前處理", "問題": f"有 {len(short_rows)} 筆少於 3 words 的短句保留在測試中，可能增加離群值。"})
    return documents, doc_meta, meta, notices


def load_or_create_embeddings(
    documents: list[str],
    embedding_model: SentenceTransformer,
    notices: list[dict[str, str]],
) -> np.ndarray:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if EMBEDDINGS_CACHE.exists():
        embeddings = np.load(EMBEDDINGS_CACHE)
        if embeddings.shape[0] == len(documents):
            notices.append({"流程": "Embedding", "問題": f"讀取既有快取：{EMBEDDINGS_CACHE.relative_to(ROOT)}"})
            return embeddings
        notices.append({"流程": "Embedding", "問題": "既有 embeddings 快取筆數與 documents 不一致，已重新計算。"})

    embeddings = embedding_model.encode(documents, show_progress_bar=True, batch_size=64)
    np.save(EMBEDDINGS_CACHE, embeddings)
    notices.append({"流程": "Embedding", "問題": f"已完成 embeddings 並寫入快取：{EMBEDDINGS_CACHE.relative_to(ROOT)}"})
    return embeddings


def load_or_create_umap(embeddings: np.ndarray, notices: list[dict[str, str]]) -> np.ndarray:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if UMAP_CACHE.exists():
        reduced_embeddings = np.load(UMAP_CACHE)
        if reduced_embeddings.shape[0] == embeddings.shape[0]:
            notices.append({"流程": "UMAP", "問題": f"讀取既有快取：{UMAP_CACHE.relative_to(ROOT)}"})
            return reduced_embeddings
        notices.append({"流程": "UMAP", "問題": "既有 UMAP 快取筆數與 embeddings 不一致，已重新計算。"})

    reduced_embeddings = UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric="cosine",
        random_state=42,
    ).fit_transform(embeddings)
    np.save(UMAP_CACHE, reduced_embeddings)
    notices.append({"流程": "UMAP", "問題": f"已完成 UMAP 降維並寫入快取：{UMAP_CACHE.relative_to(ROOT)}"})
    return reduced_embeddings


def remap_hdbscan_labels(labels: np.ndarray) -> np.ndarray:
    counts = Counter(int(label) for label in labels if int(label) != -1)
    mapping = {
        old_label: new_label
        for new_label, (old_label, _) in enumerate(sorted(counts.items(), key=lambda item: (-item[1], item[0])))
    }
    return np.array([-1 if int(label) == -1 else mapping[int(label)] for label in labels], dtype=int)


def count_labels(labels: np.ndarray) -> dict[str, Any]:
    remapped = remap_hdbscan_labels(labels)
    counts = Counter(int(label) for label in remapped)
    n_clusters = len([topic for topic in counts if topic != -1])
    return {
        "n_clusters": int(n_clusters),
        "noise_ratio": float(counts.get(-1, 0) / len(remapped)),
        "topic_-1_count": int(counts.get(-1, 0)),
        "topic_0_count": int(counts.get(0, 0)),
        "topic_1_count": int(counts.get(1, 0)),
    }


def pick_best(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidates = [row for row in rows if row.get("status") == "ok" and row.get("n_clusters", 0) >= 2]
    if not candidates:
        candidates = [row for row in rows if row.get("status") == "ok" and row.get("n_clusters", 0) >= 1]
    if not candidates:
        return None
    return sorted(candidates, key=lambda row: (row["noise_ratio"], -row["n_clusters"], row["min_cluster_size"]))[0]


def train_best_topic_model(
    documents: list[str],
    doc_meta: pd.DataFrame,
    embedding_model: SentenceTransformer,
    embeddings: np.ndarray,
    best_size: int,
) -> dict[str, Any]:
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric="cosine", random_state=42),
        hdbscan_model=HDBSCAN(
            min_cluster_size=best_size,
            metric="euclidean",
            cluster_selection_method="eom",
            prediction_data=True,
        ),
        vectorizer_model=CountVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2),
        top_n_words=10,
        calculate_probabilities=False,
        verbose=False,
    )
    topics, _ = topic_model.fit_transform(documents, embeddings)
    topic_info = topic_model.get_topic_info()
    doc_topics = doc_meta.copy()
    doc_topics["topic"] = [int(topic) for topic in topics]

    preferred_columns = [
        "dataset_row",
        "title",
        "source_row",
        "paragraph_id",
        "sentence_start_id",
        "sentence_end_id",
        "sentence_count",
        "word_count",
        "char_count",
        "topic",
        "document",
    ]
    ordered_columns = [column for column in preferred_columns if column in doc_topics.columns]
    ordered_columns.extend(column for column in doc_topics.columns if column not in ordered_columns)

    topic_info.to_csv(BEST_TOPIC_INFO_CSV, index=False)
    doc_topics[ordered_columns].to_csv(BEST_DOC_TOPICS_CSV, index=False)
    return {"topic_count": int(len(topic_info)), "topic_info_rows": int(len(topic_info))}


def plot_elbow_chart(chart_title: str = "[B]01 orig 08-19 tok para12-80") -> None:
    df = pd.read_csv(MIN_TEST_CSV)
    ok = df[df["status"].eq("ok")].copy()
    if ok.empty:
        return

    ok["noise_ratio_pct"] = ok["noise_ratio"].astype(float) * 100
    orange = "#ed7d31"
    green = "#1f7a3a"
    grid = "#dddddd"
    text = "#555555"

    fig, ax = plt.subplots(figsize=(8.8, 5.6), dpi=180)
    ax2 = ax.twinx()
    line1 = ax.plot(
        ok["min_cluster_size"],
        ok["n_clusters"],
        color=orange,
        marker="o",
        linewidth=2.2,
        markersize=4.5,
        label="n_clusters",
    )[0]
    line2 = ax2.plot(
        ok["min_cluster_size"],
        ok["noise_ratio_pct"],
        color=green,
        marker="D",
        linewidth=2.2,
        markersize=4.0,
        label="noise_ratio (%)",
    )[0]

    sizes = ok["min_cluster_size"].astype(int).tolist()
    ax.set_xticks(sizes)
    ax.set_xticklabels([str(size) for size in sizes], rotation=45, ha="right", fontsize=8, color=text)
    ax.tick_params(axis="x", pad=3)
    ax.tick_params(axis="y", colors=text, labelsize=9)
    ax2.tick_params(axis="y", colors=text, labelsize=9)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}%"))
    ax2.set_ylim(0, 100)
    ax.grid(True, axis="y", color=grid, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color("#d9d9d9")
    for spine in ax2.spines.values():
        spine.set_color("#d9d9d9")

    ax.set_xlabel("min_cluster_size", color=text, fontsize=10)
    ax.set_ylabel("n_clusters", color=text, fontsize=10)
    ax2.set_ylabel("noise_ratio (%)", color=text, fontsize=10)
    ax.set_title(chart_title, color=text, fontsize=11, pad=10)
    legend = ax.legend(
        [line1, line2],
        [line1.get_label(), line2.get_label()],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.22),
        ncol=2,
        frameon=False,
        fontsize=9,
    )
    for legend_text in legend.get_texts():
        legend_text.set_color(text)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(CHART_PATH, dpi=180, bbox_inches="tight")
    fig.savefig(CHART_SVG_PATH, bbox_inches="tight")
    plt.close(fig)


def write_report(
    meta: dict[str, Any],
    rows: list[dict[str, Any]],
    notices: list[dict[str, str]],
    full_failures: list[str],
    improvements: list[str],
    best_payload: dict[str, Any] | None,
) -> None:
    best = best_payload["best_row"] if best_payload else None
    param_rows = [
        {"參數": "Dataset", "設定": meta["dataset_dir"], "統計/原因": f"{meta['used_rows']} usable documents; text_col={meta['text_col']}"},
        {"參數": "Embedding Model", "設定": "all-MiniLM-L6-v2", "統計/原因": "通用英文語意向量模型，與既有專案設定一致"},
        {"參數": "UMAP", "設定": "n_neighbors=15, n_components=5, min_dist=0.0, metric=cosine, random_state=42", "統計/原因": "固定降維設定，讓不同 min_cluster_size 可比較"},
        {"參數": "HDBSCAN", "設定": "metric=euclidean, cluster_selection_method=eom, prediction_data=True", "統計/原因": "對固定 UMAP 結果測試 min_cluster_size；測試表 topic 0/1 已按群集大小重編號"},
        {"參數": "CountVectorizer", "設定": "stop_words=english, ngram_range=(1, 2), min_df=2", "統計/原因": "最佳參數 BERTopic 訓練時使用，降低極低頻詞干擾"},
        {"參數": "min_cluster_size 測試範圍", "設定": ", ".join(str(size) for size in CLUSTER_SIZES), "統計/原因": "依使用者指定完整測試"},
    ]
    if best_payload and best:
        param_rows.append(
            {
                "參數": "最佳 min_cluster_size",
                "設定": str(best_payload["best_min_cluster_size"]),
                "統計/原因": f"n_clusters={best['n_clusters']}, noise_ratio={best['noise_ratio']:.4f}, topic -1 count={best['topic_-1_count']}, topic 0 count={best['topic_0_count']}, topic 1 count={best['topic_1_count']}",
            }
        )

    display_rows = []
    for row in rows:
        display_rows.append(
            {
                "min_cluster_size": row["min_cluster_size"],
                "n_clusters": "" if row["n_clusters"] is None else row["n_clusters"],
                "noise_ratio": "" if row["noise_ratio"] is None else f"{row['noise_ratio']:.4f}",
                "主題 -1 count": "" if row["topic_-1_count"] is None else row["topic_-1_count"],
                "主題 0 count": "" if row["topic_0_count"] is None else row["topic_0_count"],
                "主題 1 count": "" if row["topic_1_count"] is None else row["topic_1_count"],
                "狀態": row["status"],
                "備註": row["note"],
            }
        )

    report = [
        f"# BERTopic min_cluster_size 檢測報告 - {RUN_LABEL}",
        "",
        f"- 建立時間：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"- 資料來源：`{meta['dataset_dir']}`",
        f"- 使用欄位：`{meta['text_col']}`",
        f"- 原始筆數：{meta['source_rows']}",
        f"- 可用 documents：{meta['used_rows']}",
        f"- 文本長度：min={meta['min_text_len']}, avg={meta['avg_text_len']:.1f}, max={meta['max_text_len']}",
        f"- word_count：min={meta['min_word_count']}, avg={meta['avg_word_count']:.1f}, max={meta['max_word_count']}",
        "",
        "## BERTopic 參數設定",
        "",
        md_table(param_rows, ["參數", "設定", "統計/原因"]),
        "## min_cluster_size 不同參數測試結果",
        "",
        "> 註：測試表的 topic 0/1 count 依群集大小重編號，最大非離群群集為 topic 0；正式 BERTopic 輸出的 topic id 以 BERTopic model 為準。",
        "",
        md_table(
            display_rows,
            ["min_cluster_size", "n_clusters", "noise_ratio", "主題 -1 count", "主題 0 count", "主題 1 count", "狀態", "備註"],
        ),
    ]
    if best_payload and best:
        report.extend(
            [
                "## 測試結論",
                "",
                f"`min_cluster_size={best_payload['best_min_cluster_size']}` 在本次掃描中離群值最低且保留有效主題。選擇規則為：{best_payload['best_selection_rule']}",
                f"此設定的統計為 n_clusters={best['n_clusters']}、noise_ratio={best['noise_ratio']:.4f}、主題 -1 count={best['topic_-1_count']}、主題 0 count={best['topic_0_count']}、主題 1 count={best['topic_1_count']}。",
                "",
                f"- 最佳參數 topic info CSV：`{BEST_TOPIC_INFO_CSV.relative_to(ROOT)}`" if BEST_TOPIC_INFO_CSV.exists() else "- 最佳參數 topic info CSV：未產生",
                f"- 最佳參數 document-topic CSV：`{BEST_DOC_TOPICS_CSV.relative_to(ROOT)}`" if BEST_DOC_TOPICS_CSV.exists() else "- 最佳參數 document-topic CSV：未產生",
                f"- 完整 min_cluster_size CSV：`{MIN_TEST_CSV.relative_to(ROOT)}`",
                f"- 肘狀圖 PNG：`{CHART_PATH.relative_to(ROOT)}`" if CHART_PATH.exists() else "- 肘狀圖 PNG：未產生",
                "",
            ]
        )
    report.extend(
        [
            "## 錯誤輸出",
            "",
            "### 檢測發現與建議",
            "> 在運行過程中遇到的所有問題，用表格紀錄。",
            "",
            md_table(notices, ["流程", "問題"]),
            "### 整體錯誤輸出",
            "> 最後嘗試還是失敗，需要更改的功能。",
            "",
            "無。BERTopic min_cluster_size 掃描已完成。"
            if not full_failures
            else "\n\n".join(f"```text\n{failure}\n```" for failure in full_failures),
            "",
            "### 可改進",
            "> 不影響流程，但改了可以讓流程更順，或讓結果更好的建議。",
            "",
            "\n".join(f"{idx}. {item}" for idx, item in enumerate(improvements, start=1)) or "無",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")


def run() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    notices: list[dict[str, str]] = [{"流程": "環境開始運行", "問題": "環境套件可載入，開始 BERTopic min_cluster_size 檢測。"}]
    full_failures: list[str] = []
    improvements: list[str] = []
    best_payload: dict[str, Any] | None = None
    final_training_summary: dict[str, Any] | None = None

    try:
        documents, doc_meta, meta, load_notices = load_documents()
        notices.extend(load_notices)
    except Exception:
        REPORT_PATH.write_text(
            f"# BERTopic min_cluster_size 檢測報告 - {RUN_LABEL}\n\n"
            "## 錯誤輸出\n\n"
            "### 檢測發現與建議\n\n"
            + md_table([{"流程": "資料載入", "問題": "無法載入 dataset。"}], ["流程", "問題"])
            + "\n### 整體錯誤輸出\n\n"
            + f"```text\n{traceback.format_exc()}\n```\n\n"
            + "### 可改進\n\n1. 先確認 Hugging Face Dataset 是否完整包含 arrow、dataset_info.json、state.json。\n",
            encoding="utf-8",
        )
        raise

    if not documents:
        raise RuntimeError("Dataset does not contain any usable text documents.")

    embedding_model_name = "all-MiniLM-L6-v2"
    try:
        embedding_model = SentenceTransformer(embedding_model_name)
        embeddings = load_or_create_embeddings(documents, embedding_model, notices)
    except Exception:
        full_failures.append("Embedding model 載入或向量計算失敗。\n" + traceback.format_exc())
        raise

    try:
        reduced_embeddings = load_or_create_umap(embeddings, notices)
    except Exception:
        full_failures.append("UMAP 降維失敗。\n" + traceback.format_exc())
        raise

    rows: list[dict[str, Any]] = []
    for size in CLUSTER_SIZES:
        row: dict[str, Any] = {
            "min_cluster_size": int(size),
            "n_clusters": None,
            "noise_ratio": None,
            "topic_-1_count": None,
            "topic_0_count": None,
            "topic_1_count": None,
            "status": "pending",
            "note": "",
        }
        if size > len(documents):
            row.update(
                {
                    "status": "skipped",
                    "note": f"min_cluster_size={size} 大於可用 documents={len(documents)}，不適用。",
                }
            )
            notices.append({"流程": "BERTopic 參數測試", "問題": row["note"]})
            rows.append(row)
            continue
        try:
            labels = HDBSCAN(
                min_cluster_size=int(size),
                metric="euclidean",
                cluster_selection_method="eom",
                prediction_data=True,
            ).fit_predict(reduced_embeddings)
            row.update(count_labels(labels))
            row.update({"status": "ok", "note": "完成"})
            print(
                f"min_cluster_size={size}: "
                f"n_clusters={row['n_clusters']}, "
                f"noise_ratio={row['noise_ratio']:.4f}, "
                f"topic_-1={row['topic_-1_count']}, "
                f"topic_0={row['topic_0_count']}, "
                f"topic_1={row['topic_1_count']}",
                flush=True,
            )
        except Exception as exc:
            row.update({"status": "failed", "note": str(exc)})
            notices.append({"流程": "BERTopic 參數測試", "問題": f"min_cluster_size={size} 失敗：{exc}"})
            full_failures.append(f"min_cluster_size={size}\n{traceback.format_exc()}")
        rows.append(row)

    best = pick_best(rows)
    if best:
        best_size = int(best["min_cluster_size"])
        best_payload = {
            "best_min_cluster_size": best_size,
            "best_selection_rule": "優先選擇 n_clusters >= 2 且 noise_ratio 最低者；若並列，選 n_clusters 較多者，再選 min_cluster_size 較小者。",
            "best_row": best,
        }
        try:
            final_training_summary = train_best_topic_model(documents, doc_meta, embedding_model, embeddings, best_size)
        except Exception as exc:
            notices.append({"流程": "BERTopic 最佳參數訓練", "問題": f"最佳參數 min_cluster_size={best_size} 的 BERTopic 訓練失敗：{exc}"})
            full_failures.append(f"best min_cluster_size={best_size}\n{traceback.format_exc()}")
    else:
        notices.append({"流程": "BERTopic 結果彙整", "問題": "所有 min_cluster_size 皆未產生有效主題，無法選出最佳參數。"})
        full_failures.append("所有候選參數皆未產生 n_clusters >= 1 的有效主題。")

    pd.DataFrame(rows).to_csv(MIN_TEST_CSV, index=False)
    try:
        plot_elbow_chart()
    except Exception:
        notices.append({"流程": "圖表輸出", "問題": "肘狀圖產生失敗，詳見完整錯誤。"})
        full_failures.append("肘狀圖產生失敗。\n" + traceback.format_exc())

    RUN_LOG_JSON.write_text(
        json.dumps(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "dataset_meta": meta,
                "embedding_model": embedding_model_name,
                "embeddings_shape": list(embeddings.shape),
                "reduced_embeddings_shape": list(reduced_embeddings.shape),
                "rows": rows,
                "notices": notices,
                "best": best_payload,
                "final_training_summary": final_training_summary,
                "full_failures": full_failures,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if meta["short_rows_lt_3_words_count"]:
        improvements.append("短句比例可能影響 HDBSCAN 密度判斷，可測試排除少於 3 或 5 words 的句子後再比較 noise_ratio。")
    improvements.extend(
        [
            "本次參數掃描使用固定 embeddings 與固定 UMAP 結果，比較重點集中在 HDBSCAN min_cluster_size。",
            "最佳參數建議再搭配 topic words 與代表句人工審查，避免只用 noise_ratio 選到語意過寬的主題。",
            "若 noise_ratio 仍偏高，可測試 HDBSCAN min_samples、UMAP n_neighbors，或 BERTopic reduce_outliers。",
        ]
    )
    write_report(meta, rows, notices, full_failures, improvements, best_payload)


if __name__ == "__main__":
    try:
        run()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
