from __future__ import annotations

import json
import sys
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from bertopic import BERTopic
from datasets import load_from_disk
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP


ROOT = Path(__file__).resolve().parents[3]
DATASET_DIR = ROOT / "Result/06.03_A02/R06.03_A02-pre_LLM(del)_tok(para12-80)_dataset"
OUTPUT_DIR = ROOT / "Result/06.03_A03_min-test/A03-3(del)_tok(para12-80)"

REPORT_PATH = OUTPUT_DIR / "Result_06.03_A03-3(del)_tok(para12-80).md"
MIN_TEST_CSV = OUTPUT_DIR / "Result_06.03_A03-3(del)_tok(para12-80)-min_cluster_size.csv"
BEST_TOPIC_INFO_CSV = OUTPUT_DIR / "Result_06.03_A03-3(del)_tok(para12-80)-best_topic_info.csv"
BEST_DOC_TOPICS_CSV = OUTPUT_DIR / "Result_06.03_A03-3(del)_tok(para12-80)-best_document_topics.csv"
RUN_LOG_JSON = OUTPUT_DIR / "Result_06.03_A03-3(del)_tok(para12-80)-run_log.json"

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


def load_documents() -> tuple[list[str], list[str], dict[str, Any], list[dict[str, str]]]:
    dataset = load_from_disk(str(DATASET_DIR))
    columns = list(dataset.column_names)
    text_col = "sentence" if "sentence" in columns else columns[0]
    title_col = "title" if "title" in columns else None

    documents: list[str] = []
    titles: list[str] = []
    empty_rows: list[int] = []
    short_rows: list[int] = []
    for idx, item in enumerate(dataset):
        text = "" if item.get(text_col) is None else str(item.get(text_col)).strip()
        if not text:
            empty_rows.append(idx)
            continue
        documents.append(text)
        titles.append("" if title_col is None else str(item.get(title_col, "")))
        if len(text.split()) < 3:
            short_rows.append(idx)

    lengths = [len(doc) for doc in documents]
    word_counts = [len(doc.split()) for doc in documents]
    meta = {
        "dataset_dir": str(DATASET_DIR.relative_to(ROOT)),
        "columns": columns,
        "text_col": text_col,
        "title_col": title_col,
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

    errors: list[dict[str, str]] = []
    if empty_rows:
        errors.append({"流程": "前處理", "問題": f"有 {len(empty_rows)} 筆空白文本已排除。"})
    if short_rows:
        errors.append({"流程": "前處理", "問題": f"有 {len(short_rows)} 筆少於 3 words 的短句保留在測試中，可能增加離群值。"})
    return documents, titles, meta, errors


def count_labels(labels: np.ndarray) -> dict[str, Any]:
    counts = Counter(int(label) for label in labels)
    n_clusters = len([topic for topic in counts if topic != -1])
    return {
        "n_clusters": int(n_clusters),
        "noise_ratio": float(counts.get(-1, 0) / len(labels)),
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
    titles: list[str],
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
    doc_topics = pd.DataFrame(
        {
            "title": titles,
            "document": documents,
            "topic": [int(topic) for topic in topics],
        }
    )
    topic_info.to_csv(BEST_TOPIC_INFO_CSV, index=False)
    doc_topics.to_csv(BEST_DOC_TOPICS_CSV, index=False)
    return {"topic_count": int(len(topic_info)), "topic_info_rows": int(len(topic_info))}


def run() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    errors: list[dict[str, str]] = [{"流程": "環境開始運行", "問題": "環境套件可載入，開始 BERTopic min_cluster_size 檢測。"}]
    full_failures: list[str] = []
    improvements: list[str] = []
    best_payload: dict[str, Any] | None = None
    final_training_summary: dict[str, Any] | None = None

    try:
        documents, titles, meta, load_errors = load_documents()
        errors.extend(load_errors)
    except Exception:
        REPORT_PATH.write_text(
            "# BERTopic min_cluster_size 檢測報告 - 06.03_A03-3(del)_tok(para12-80)\n\n"
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
        embeddings = embedding_model.encode(documents, show_progress_bar=True, batch_size=64)
    except Exception:
        full_failures.append("Embedding model 載入或向量計算失敗。\n" + traceback.format_exc())
        raise

    try:
        reduced_embeddings = UMAP(
            n_neighbors=15,
            n_components=5,
            min_dist=0.0,
            metric="cosine",
            random_state=42,
        ).fit_transform(embeddings)
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
            errors.append({"流程": "BERTopic 參數測試", "問題": row["note"]})
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
        except Exception as exc:
            row.update({"status": "failed", "note": str(exc)})
            errors.append({"流程": "BERTopic 參數測試", "問題": f"min_cluster_size={size} 失敗：{exc}"})
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
            final_training_summary = train_best_topic_model(documents, titles, embedding_model, embeddings, best_size)
        except Exception as exc:
            errors.append({"流程": "BERTopic 最佳參數訓練", "問題": f"最佳參數 min_cluster_size={best_size} 的 BERTopic 訓練失敗：{exc}"})
            full_failures.append(f"best min_cluster_size={best_size}\n{traceback.format_exc()}")
    else:
        errors.append({"流程": "BERTopic 結果彙整", "問題": "所有 min_cluster_size 皆未產生有效主題，無法選出最佳參數。"})
        full_failures.append("所有候選參數皆未產生 n_clusters >= 1 的有效主題。")

    pd.DataFrame(rows).to_csv(MIN_TEST_CSV, index=False)
    RUN_LOG_JSON.write_text(
        json.dumps(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "dataset_meta": meta,
                "rows": rows,
                "errors": errors,
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

    param_rows = [
        {"參數": "Dataset", "設定": meta["dataset_dir"], "統計/原因": f"{meta['used_rows']} usable documents; text_col={meta['text_col']}"},
        {"參數": "Embedding Model", "設定": embedding_model_name, "統計/原因": "通用英文語意向量模型，與既有專案設定一致"},
        {"參數": "UMAP", "設定": "n_neighbors=15, n_components=5, min_dist=0.0, metric=cosine, random_state=42", "統計/原因": "固定降維設定，讓不同 min_cluster_size 可比較"},
        {"參數": "HDBSCAN", "設定": "metric=euclidean, cluster_selection_method=eom, prediction_data=True", "統計/原因": "對固定 UMAP 結果測試 min_cluster_size"},
        {"參數": "CountVectorizer", "設定": "stop_words=english, ngram_range=(1, 2), min_df=2", "統計/原因": "最佳參數 BERTopic 訓練時使用，降低極低頻詞干擾"},
        {"參數": "min_cluster_size 測試範圍", "設定": ", ".join(str(size) for size in CLUSTER_SIZES), "統計/原因": "依使用者指定完整測試"},
    ]
    if best_payload:
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
        "# BERTopic min_cluster_size 檢測報告 - 06.03_A03-3(del)_tok(para12-80)",
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
        md_table(
            display_rows,
            ["min_cluster_size", "n_clusters", "noise_ratio", "主題 -1 count", "主題 0 count", "主題 1 count", "狀態", "備註"],
        ),
    ]
    if best_payload:
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
            md_table(errors, ["流程", "問題"]),
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


if __name__ == "__main__":
    try:
        run()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
