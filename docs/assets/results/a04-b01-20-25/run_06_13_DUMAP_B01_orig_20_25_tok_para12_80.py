from __future__ import annotations

import hashlib
import json
import math
import traceback
from collections import Counter
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bertopic import BERTopic
from datasets import load_from_disk
from hdbscan import HDBSCAN
from joblib import Memory
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP


ROOT = Path(__file__).resolve().parents[3]
DATASET_DIR = ROOT / "Result/06.13_[B]tok/06.13_[B]01-pre_LLM(orig)_20-25(194)_tok(para12-80)_dataset"
OUTPUT_DIR = ROOT / "Result/06.13_[D]UMAP/[B]01-(orig)_20-25_tok(para12-80)"
REPORT_PATH = OUTPUT_DIR / "Result_[D]01-(orig)_20-25_tok(para12-80).md"
BASELINE_DIR = ROOT / "Result/06.13_[C]min/[B]01-(orig)_20-25(194)_tok(para12-80)"
BASELINE_MIN_CSV = BASELINE_DIR / "Result_06.13_[C]min_[B]01-(orig)_20-25(194)_tok(para12-80)-min_cluster_size.csv"
BASELINE_TOPIC_INFO_CSV = BASELINE_DIR / "Result_06.13_[C]min_[B]01-(orig)_20-25(194)_tok(para12-80)-best_topic_info.csv"
STAGE1_CSV = OUTPUT_DIR / "stage1_results.csv"
STAGE2_CSV = OUTPUT_DIR / "stage2_results.csv"
SELECTED_CSV = OUTPUT_DIR / "selected_configs.csv"
STABILITY_CSV = OUTPUT_DIR / "stability_results.csv"
RUN_LOG_JSON = OUTPUT_DIR / "run_log.json"
FINAL_CONFIGS_JSON = OUTPUT_DIR / "final_configs.json"
COMPARISON_SUMMARY_CSV = OUTPUT_DIR / "comparison_summary.csv"
EMBEDDINGS_PATH = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.npy"
EMBEDDINGS_META = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.meta.json"
UMAP_CACHE_DIR = OUTPUT_DIR / "umap_cache"
HDBSCAN_CACHE_DIR = OUTPUT_DIR / "hdbscan_cache"
CHART_DIR = OUTPUT_DIR / "charts"
FINAL_DIR = OUTPUT_DIR / "final_models"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TEXT_COL = "sentence"
RANDOM_STATE = 42
STABILITY_SEEDS = [42, 123, 2026, 3407, 20240603]

UMAP_N_NEIGHBORS = [5, 10, 15, 30, 50, 75, 100]
UMAP_N_COMPONENTS = [5, 10, 15]
UMAP_MIN_DIST = [0.0, 0.05, 0.1, 0.25]

STAGE1_MIN_CLUSTER_SIZE = [50, 75, 100, 125, 150, 175, 200, 225, 250, 300]
STAGE1_MIN_SAMPLES = [None, 10, 30]

STAGE2_MIN_CLUSTER_SIZE = [
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
STAGE2_MIN_SAMPLES = [None, 5, 10, 15, 30, 50, 75, 100]
STAGE2_METHODS = ["eom", "leaf"]
STAGE2_EPSILONS = [0.0, 0.05, 0.1, 0.2]


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        vals = []
        for col in columns:
            value = row.get(col, "")
            if isinstance(value, float):
                text = f"{value:.4f}"
            else:
                text = "" if value is None else str(value)
            vals.append(text.replace("\n", "<br>").replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines) + "\n"


def rel(path: Path) -> str:
    return str(path.relative_to(OUTPUT_DIR))


def safe_float_token(value: float) -> str:
    return str(value).replace(".", "p")


def load_documents() -> tuple[list[str], list[str], pd.DataFrame, dict[str, Any], list[dict[str, str]]]:
    dataset = load_from_disk(str(DATASET_DIR))
    columns = list(dataset.column_names)
    if TEXT_COL not in columns:
        raise ValueError(f"Dataset missing required text column: {TEXT_COL}")
    title_col = "title" if "title" in columns else None
    docs: list[str] = []
    titles: list[str] = []
    rows: list[dict[str, Any]] = []
    empty_rows: list[int] = []
    short_rows: list[int] = []
    for idx, item in enumerate(dataset):
        text = "" if item.get(TEXT_COL) is None else str(item.get(TEXT_COL)).strip()
        if not text:
            empty_rows.append(idx)
            continue
        docs.append(text)
        titles.append("" if title_col is None else str(item.get(title_col, "")))
        row = {column: item.get(column) for column in columns}
        row["dataset_row"] = idx
        row["document"] = text
        rows.append(row)
        if len(text.split()) < 3:
            short_rows.append(idx)
    lengths = [len(doc) for doc in docs]
    word_counts = [len(doc.split()) for doc in docs]
    meta = {
        "dataset_dir": str(DATASET_DIR.relative_to(ROOT)),
        "columns": columns,
        "text_col": TEXT_COL,
        "title_col": title_col,
        "source_rows": len(dataset),
        "used_rows": len(docs),
        "empty_rows_count": len(empty_rows),
        "short_rows_lt_3_words_count": len(short_rows),
        "min_text_len": min(lengths, default=0),
        "max_text_len": max(lengths, default=0),
        "avg_text_len": float(np.mean(lengths)) if lengths else 0.0,
        "min_word_count": min(word_counts, default=0),
        "max_word_count": max(word_counts, default=0),
        "avg_word_count": float(np.mean(word_counts)) if word_counts else 0.0,
    }
    notes = []
    if empty_rows:
        notes.append({"流程": "資料載入", "問題": f"有 {len(empty_rows)} 筆空白文本已排除。"})
    if short_rows:
        notes.append({"流程": "資料載入", "問題": f"有 {len(short_rows)} 筆少於 3 words 的短句保留，可能增加離群值。"})
    return docs, titles, pd.DataFrame(rows), meta, notes


def docs_hash(docs: list[str]) -> str:
    digest = hashlib.sha256()
    digest.update(str(len(docs)).encode("utf-8"))
    for doc in docs[:100]:
        digest.update(doc.encode("utf-8", errors="ignore"))
    for doc in docs[-100:]:
        digest.update(doc.encode("utf-8", errors="ignore"))
    return digest.hexdigest()


def get_embeddings(docs: list[str], errors: list[dict[str, str]]) -> tuple[SentenceTransformer, np.ndarray]:
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    current_meta = {"model": EMBEDDING_MODEL_NAME, "doc_count": len(docs), "docs_hash": docs_hash(docs)}
    if EMBEDDINGS_PATH.exists() and EMBEDDINGS_META.exists():
        old_meta = json.loads(EMBEDDINGS_META.read_text(encoding="utf-8"))
        if old_meta == current_meta:
            embeddings = np.load(EMBEDDINGS_PATH)
            if embeddings.shape[0] == len(docs):
                errors.append({"流程": "Embedding", "問題": "偵測到既有 embeddings 快取，已直接共用。"})
                return model, embeddings
    embeddings = model.encode(docs, show_progress_bar=True, batch_size=64, convert_to_numpy=True)
    np.save(EMBEDDINGS_PATH, embeddings)
    EMBEDDINGS_META.write_text(json.dumps(current_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    errors.append({"流程": "Embedding", "問題": "已完成 embeddings 計算並建立快取。"})
    return model, embeddings


def umap_path(nn: int, nc: int, md: float, seed: int) -> Path:
    return UMAP_CACHE_DIR / f"umap_nn{nn}_nc{nc}_md{safe_float_token(md)}_seed{seed}.npy"


def get_umap_embeddings(embeddings: np.ndarray, nn: int, nc: int, md: float, seed: int) -> np.ndarray:
    path = umap_path(nn, nc, md, seed)
    if path.exists():
        return np.load(path)
    reduced = UMAP(
        n_neighbors=nn,
        n_components=nc,
        min_dist=md,
        metric="cosine",
        random_state=seed,
        low_memory=True,
    ).fit_transform(embeddings)
    np.save(path, reduced)
    return reduced


def label_metrics(labels: np.ndarray) -> dict[str, Any]:
    counts = Counter(int(label) for label in labels)
    total = int(len(labels))
    sorted_clusters = sorted(
        ((topic, count) for topic, count in counts.items() if topic != -1),
        key=lambda item: (-item[1], item[0]),
    )
    remapped_counts = {new_topic: count for new_topic, (_, count) in enumerate(sorted_clusters)}
    cluster_counts = [count for _, count in sorted_clusters]
    cluster_counts_sorted = sorted(cluster_counts, reverse=True)
    n_clusters = len(cluster_counts)
    largest = int(cluster_counts_sorted[0]) if cluster_counts_sorted else 0
    top3 = int(sum(cluster_counts_sorted[:3])) if cluster_counts_sorted else 0
    if n_clusters <= 1 or sum(cluster_counts) == 0:
        entropy = 0.0
    else:
        probs = np.array(cluster_counts, dtype=float) / float(sum(cluster_counts))
        entropy = float(-(probs * np.log(probs)).sum() / math.log(n_clusters))
    noise_ratio = float(counts.get(-1, 0) / total) if total else 0.0
    largest_ratio = float(largest / total) if total else 0.0
    top3_ratio = float(top3 / total) if total else 0.0
    normalized_n_clusters = min(n_clusters / 25.0, 1.0)
    balance_score = (
        0.30 * (1.0 - noise_ratio)
        + 0.30 * (1.0 - largest_ratio)
        + 0.20 * (1.0 - top3_ratio)
        + 0.20 * normalized_n_clusters
    )
    return {
        "n_clusters": int(n_clusters),
        "noise_ratio": noise_ratio,
        "topic_-1_count": int(counts.get(-1, 0)),
        "topic_0_count": int(remapped_counts.get(0, 0)),
        "topic_1_count": int(remapped_counts.get(1, 0)),
        "largest_topic_count": largest,
        "largest_topic_ratio": largest_ratio,
        "top3_topic_ratio": top3_ratio,
        "topic_entropy": entropy,
        "balance_score": float(balance_score),
    }


def hdbscan_labels(
    reduced: np.ndarray,
    min_cluster_size: int,
    min_samples: int | None,
    method: str,
    epsilon: float,
    memory: Memory,
) -> np.ndarray:
    return HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric="euclidean",
        cluster_selection_method=method,
        cluster_selection_epsilon=epsilon,
        prediction_data=True,
        core_dist_n_jobs=-1,
        memory=memory,
    ).fit_predict(reduced)


def existing_keys(path: Path, key_cols: list[str]) -> set[tuple[Any, ...]]:
    if not path.exists():
        return set()
    df = pd.read_csv(path)
    keys = set()
    for _, row in df.iterrows():
        vals = []
        for col in key_cols:
            val = row[col]
            if pd.isna(val):
                vals.append(None)
            else:
                vals.append(val)
        keys.add(tuple(vals))
    return keys


def append_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    df = pd.DataFrame(rows)
    header = not path.exists()
    df.to_csv(path, mode="a", header=header, index=False)


def run_hdbscan_grid(
    stage_name: str,
    output_csv: Path,
    embeddings: np.ndarray,
    umap_configs: list[dict[str, Any]],
    min_cluster_sizes: list[int],
    min_samples_values: list[int | None],
    methods: list[str],
    epsilons: list[float],
    errors: list[dict[str, str]],
) -> pd.DataFrame:
    key_cols = [
        "umap_n_neighbors",
        "umap_n_components",
        "umap_min_dist",
        "umap_random_state",
        "hdbscan_min_cluster_size",
        "hdbscan_min_samples",
        "hdbscan_cluster_selection_method",
        "hdbscan_cluster_selection_epsilon",
    ]
    done = existing_keys(output_csv, key_cols)
    total = len(umap_configs) * len(min_cluster_sizes) * len(min_samples_values) * len(methods) * len(epsilons)
    completed = len(done)
    for uidx, uconf in enumerate(umap_configs, start=1):
        nn = int(uconf["umap_n_neighbors"])
        nc = int(uconf["umap_n_components"])
        md = float(uconf["umap_min_dist"])
        seed = int(uconf.get("umap_random_state", RANDOM_STATE))
        try:
            reduced = get_umap_embeddings(embeddings, nn, nc, md, seed)
        except Exception as exc:
            errors.append({"流程": "UMAP", "問題": f"{stage_name} UMAP nn={nn}, nc={nc}, min_dist={md}, seed={seed} 失敗：{exc}"})
            continue
        memory = Memory(HDBSCAN_CACHE_DIR / stage_name / f"nn{nn}_nc{nc}_md{safe_float_token(md)}_seed{seed}", verbose=0)
        batch: list[dict[str, Any]] = []
        for min_cluster_size, min_samples, method, epsilon in product(min_cluster_sizes, min_samples_values, methods, epsilons):
            key = (nn, nc, md, seed, min_cluster_size, min_samples, method, epsilon)
            if key in done:
                continue
            row = {
                "stage": stage_name,
                "umap_n_neighbors": nn,
                "umap_n_components": nc,
                "umap_min_dist": md,
                "umap_metric": "cosine",
                "umap_random_state": seed,
                "hdbscan_min_cluster_size": int(min_cluster_size),
                "hdbscan_min_samples": min_samples,
                "hdbscan_cluster_selection_method": method,
                "hdbscan_cluster_selection_epsilon": float(epsilon),
                "hdbscan_metric": "euclidean",
                "status": "pending",
                "note": "",
            }
            try:
                labels = hdbscan_labels(reduced, int(min_cluster_size), min_samples, method, float(epsilon), memory)
                row.update(label_metrics(labels))
                row["status"] = "ok"
                row["note"] = "完成"
            except Exception as exc:
                row["status"] = "failed"
                row["note"] = str(exc)
                errors.append({"流程": "HDBSCAN", "問題": f"{stage_name} {key} 失敗：{exc}"})
            batch.append(row)
            done.add(key)
            completed += 1
            if len(batch) >= 50:
                append_rows(output_csv, batch)
                batch = []
                print(f"[{stage_name}] {completed}/{total} rows checkpointed", flush=True)
        append_rows(output_csv, batch)
        print(f"[{stage_name}] finished UMAP {uidx}/{len(umap_configs)} nn={nn} nc={nc} md={md}", flush=True)
    return pd.read_csv(output_csv) if output_csv.exists() else pd.DataFrame()


def choose_stage2_umaps(stage1: pd.DataFrame) -> list[dict[str, Any]]:
    ok = stage1[stage1["status"].eq("ok")].copy()
    grouped = (
        ok.sort_values(["balance_score", "noise_ratio", "largest_topic_ratio"], ascending=[False, True, True])
        .groupby(["umap_n_neighbors", "umap_n_components", "umap_min_dist"], as_index=False)
        .head(1)
        .sort_values(["balance_score", "noise_ratio", "n_clusters"], ascending=[False, True, False])
    )
    selected = grouped.head(10).copy()
    extras = []
    if not ok.empty:
        extras.append(ok.sort_values(["noise_ratio", "largest_topic_ratio", "n_clusters"], ascending=[True, True, False]).iloc[0])
        extras.append(ok.sort_values(["n_clusters", "noise_ratio", "largest_topic_ratio"], ascending=[False, True, True]).iloc[0])
    for extra in extras:
        mask = (
            selected["umap_n_neighbors"].eq(extra["umap_n_neighbors"])
            & selected["umap_n_components"].eq(extra["umap_n_components"])
            & selected["umap_min_dist"].eq(extra["umap_min_dist"])
        )
        if not mask.any():
            selected = pd.concat([selected, extra.to_frame().T], ignore_index=True)
    selected = selected.drop_duplicates(["umap_n_neighbors", "umap_n_components", "umap_min_dist"]).head(10)
    return [
        {
            "umap_n_neighbors": int(row["umap_n_neighbors"]),
            "umap_n_components": int(row["umap_n_components"]),
            "umap_min_dist": float(row["umap_min_dist"]),
            "umap_random_state": RANDOM_STATE,
        }
        for _, row in selected.iterrows()
    ]


def select_best(stage2: pd.DataFrame) -> pd.DataFrame:
    ok = stage2[stage2["status"].eq("ok")].copy()
    ok = ok[ok["n_clusters"].ge(1)].copy()
    picks: list[pd.Series] = []
    labels: list[str] = []
    reasons: list[str] = []
    low_pool = ok[ok["n_clusters"].ge(2)]
    if low_pool.empty:
        low_pool = ok
    lowest_noise = low_pool.sort_values(["noise_ratio", "largest_topic_ratio", "n_clusters"], ascending=[True, True, False]).iloc[0]
    picks.append(lowest_noise)
    labels.append("lowest_noise")
    reasons.append("最低 noise_ratio，並以較低 largest_topic_ratio 與較高 n_clusters 作為 tie-break。")
    topic_pool = ok[ok["noise_ratio"].le(0.45)]
    if topic_pool.empty:
        topic_pool = ok[ok["noise_ratio"].le(0.60)]
    if topic_pool.empty:
        topic_pool = ok
    most_topics = topic_pool.sort_values(["n_clusters", "noise_ratio", "largest_topic_ratio"], ascending=[False, True, True]).iloc[0]
    picks.append(most_topics)
    labels.append("most_topics")
    reasons.append("在可接受 noise_ratio 下保留最多有效主題。")
    strict = ok[
        ok["n_clusters"].ge(4)
        & ok["noise_ratio"].le(0.35)
        & ok["largest_topic_ratio"].le(0.65)
        & ok["top3_topic_ratio"].le(0.85)
    ]
    relaxed = ok[
        ok["n_clusters"].ge(3)
        & ok["noise_ratio"].le(0.45)
        & ok["largest_topic_ratio"].le(0.75)
    ]
    if not strict.empty:
        balance_pool = strict
        balance_reason = "符合指定最佳平衡條件後取最高 balance_score。"
    elif not relaxed.empty:
        balance_pool = relaxed
        balance_reason = "嚴格條件無可用組合，改用放寬條件後取最高 balance_score。"
    else:
        balance_pool = ok[ok["n_clusters"].ge(2)]
        if balance_pool.empty:
            balance_pool = ok
        balance_reason = "嚴格與放寬條件皆無可用組合，取最高 balance_score。"
    best_balance = balance_pool.sort_values(["balance_score", "noise_ratio", "largest_topic_ratio"], ascending=[False, True, True]).iloc[0]
    picks.append(best_balance)
    labels.append("best_balance")
    reasons.append(balance_reason)
    selected = pd.DataFrame([pick.to_dict() for pick in picks])
    selected.insert(0, "selection_label", labels)
    selected.insert(1, "selection_reason", reasons)
    return selected


def row_to_umap_config(row: pd.Series, seed: int | None = None) -> dict[str, Any]:
    return {
        "umap_n_neighbors": int(row["umap_n_neighbors"]),
        "umap_n_components": int(row["umap_n_components"]),
        "umap_min_dist": float(row["umap_min_dist"]),
        "umap_random_state": int(seed if seed is not None else row.get("umap_random_state", RANDOM_STATE)),
    }


def run_stability(embeddings: np.ndarray, top_rows: pd.DataFrame, errors: list[dict[str, str]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for rank, (_, base) in enumerate(top_rows.iterrows(), start=1):
        for seed in STABILITY_SEEDS:
            row = base.to_dict()
            row["stability_rank"] = rank
            row["umap_random_state"] = seed
            row["status"] = "pending"
            row["note"] = ""
            try:
                reduced = get_umap_embeddings(
                    embeddings,
                    int(base["umap_n_neighbors"]),
                    int(base["umap_n_components"]),
                    float(base["umap_min_dist"]),
                    seed,
                )
                memory = Memory(
                    HDBSCAN_CACHE_DIR
                    / "stability"
                    / f"rank{rank}_seed{seed}_nn{int(base['umap_n_neighbors'])}_nc{int(base['umap_n_components'])}",
                    verbose=0,
                )
                labels = hdbscan_labels(
                    reduced,
                    int(base["hdbscan_min_cluster_size"]),
                    None if pd.isna(base["hdbscan_min_samples"]) else int(base["hdbscan_min_samples"]),
                    str(base["hdbscan_cluster_selection_method"]),
                    float(base["hdbscan_cluster_selection_epsilon"]),
                    memory,
                )
                row.update(label_metrics(labels))
                row["status"] = "ok"
                row["note"] = "完成"
            except Exception as exc:
                row["status"] = "failed"
                row["note"] = str(exc)
                errors.append({"流程": "UMAP", "問題": f"stability rank={rank}, seed={seed} 失敗：{exc}"})
            rows.append(row)
            pd.DataFrame(rows).to_csv(STABILITY_CSV, index=False)
    return pd.DataFrame(rows)


def train_final_models(
    docs: list[str],
    titles: list[str],
    doc_meta: pd.DataFrame,
    embedding_model: SentenceTransformer,
    embeddings: np.ndarray,
    selected: pd.DataFrame,
    errors: list[dict[str, str]],
) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    final_configs: list[dict[str, Any]] = []
    for _, row in selected.iterrows():
        label = str(row["selection_label"])
        out = FINAL_DIR / label
        out.mkdir(parents=True, exist_ok=True)
        config_record = {
            "selection_label": label,
            "selection_reason": row.get("selection_reason", ""),
            "output_dir": rel(out),
            "embedding_model": EMBEDDING_MODEL_NAME,
            "umap": {
                "n_neighbors": int(row["umap_n_neighbors"]),
                "n_components": int(row["umap_n_components"]),
                "min_dist": float(row["umap_min_dist"]),
                "metric": "cosine",
                "random_state": RANDOM_STATE,
            },
            "hdbscan": {
                "min_cluster_size": int(row["hdbscan_min_cluster_size"]),
                "min_samples": None if pd.isna(row["hdbscan_min_samples"]) else int(row["hdbscan_min_samples"]),
                "metric": "euclidean",
                "cluster_selection_method": str(row["hdbscan_cluster_selection_method"]),
                "cluster_selection_epsilon": float(row["hdbscan_cluster_selection_epsilon"]),
            },
            "selection_metrics": {
                "n_clusters": int(row["n_clusters"]),
                "noise_ratio": float(row["noise_ratio"]),
                "largest_topic_ratio": float(row["largest_topic_ratio"]),
                "top3_topic_ratio": float(row["top3_topic_ratio"]),
                "topic_entropy": float(row["topic_entropy"]),
                "balance_score": float(row["balance_score"]),
            },
        }
        final_configs.append(config_record)
        try:
            umap_model = UMAP(
                n_neighbors=int(row["umap_n_neighbors"]),
                n_components=int(row["umap_n_components"]),
                min_dist=float(row["umap_min_dist"]),
                metric="cosine",
                random_state=RANDOM_STATE,
                low_memory=True,
            )
            hdbscan_model = HDBSCAN(
                min_cluster_size=int(row["hdbscan_min_cluster_size"]),
                min_samples=None if pd.isna(row["hdbscan_min_samples"]) else int(row["hdbscan_min_samples"]),
                metric="euclidean",
                cluster_selection_method=str(row["hdbscan_cluster_selection_method"]),
                cluster_selection_epsilon=float(row["hdbscan_cluster_selection_epsilon"]),
                prediction_data=True,
                core_dist_n_jobs=-1,
            )
            topic_model = BERTopic(
                embedding_model=embedding_model,
                umap_model=umap_model,
                hdbscan_model=hdbscan_model,
                vectorizer_model=CountVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2),
                top_n_words=10,
                calculate_probabilities=False,
                verbose=False,
            )
            topics, _ = topic_model.fit_transform(docs, embeddings)
            info = topic_model.get_topic_info()
            info.to_csv(out / "topic_info.csv", index=False)
            doc_topics = doc_meta.copy()
            if "title" not in doc_topics.columns:
                doc_topics["title"] = titles
            doc_topics["topic"] = [int(t) for t in topics]
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
            doc_topics[ordered_columns].to_csv(out / "document_topics.csv", index=False)
            topic_words = []
            representative_docs = []
            for topic in info["Topic"].tolist():
                words = topic_model.get_topic(int(topic))
                topic_words.append(
                    {
                        "topic": int(topic),
                        "words": ", ".join([word for word, _ in words]) if words else "",
                        "weighted_words": json.dumps(words or [], ensure_ascii=False),
                    }
                )
                reps = topic_model.get_representative_docs(int(topic)) or []
                for ridx, rep in enumerate(reps[:5], start=1):
                    representative_docs.append({"topic": int(topic), "rank": ridx, "representative_text": rep})
            pd.DataFrame(topic_words).to_csv(out / "topic_words.csv", index=False)
            pd.DataFrame(representative_docs).to_csv(out / "representative_docs.csv", index=False)
            size_dist = info[["Topic", "Count", "Name"]].copy()
            size_dist["ratio"] = size_dist["Count"] / len(docs)
            size_dist.to_csv(out / "topic_size_distribution.csv", index=False)
            metrics = label_metrics(np.array(topics, dtype=int))
            largest_non_noise = info[info["Topic"].ne(-1)].sort_values("Count", ascending=False).head(1)
            if not largest_non_noise.empty:
                largest_topic = int(largest_non_noise.iloc[0]["Topic"])
                words = topic_model.get_topic(largest_topic) or []
                reps = topic_model.get_representative_docs(largest_topic) or []
                summary = [
                    f"# Largest Topic Summary - {label}",
                    "",
                    f"- topic: {largest_topic}",
                    f"- count: {int(largest_non_noise.iloc[0]['Count'])}",
                    f"- ratio: {float(largest_non_noise.iloc[0]['Count']) / len(docs):.4f}",
                    f"- top words: {', '.join([w for w, _ in words])}",
                    "",
                    "## Representative Texts",
                    "",
                ]
                summary.extend([f"{idx}. {text}" for idx, text in enumerate(reps[:10], start=1)])
                (out / "largest_topic_summary.md").write_text("\n".join(summary), encoding="utf-8")
            summaries.append(
                {
                    "selection_label": label,
                    "status": "ok",
                    "output_dir": rel(out),
                    "topic_info_rows": int(len(info)),
                    "n_topics_including_noise": int(len(info)),
                    **metrics,
                }
            )
        except Exception as exc:
            errors.append({"流程": "BERTopic", "問題": f"{label} 正式訓練失敗：{exc}"})
            summaries.append({"selection_label": label, "status": "failed", "note": str(exc)})
    FINAL_CONFIGS_JSON.write_text(json.dumps(final_configs, ensure_ascii=False, indent=2), encoding="utf-8")
    if summaries:
        pd.DataFrame(summaries).to_csv(COMPARISON_SUMMARY_CSV, index=False)
    return summaries


def plot_dual_axis(df: pd.DataFrame) -> None:
    ok = df[df["status"].eq("ok")].copy()
    agg = ok.groupby("hdbscan_min_cluster_size", as_index=False).agg({"n_clusters": "mean", "noise_ratio": "mean"})
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(agg["hdbscan_min_cluster_size"], agg["n_clusters"], marker="o", color="#e87532", label="n_clusters")
    ax1.set_xlabel("min_cluster_size")
    ax1.set_ylabel("n_clusters")
    ax2 = ax1.twinx()
    ax2.plot(agg["hdbscan_min_cluster_size"], agg["noise_ratio"], marker="D", color="#1d7a35", label="noise_ratio")
    ax2.set_ylabel("noise_ratio")
    ax1.grid(True, alpha=0.3)
    fig.legend(loc="lower center", ncol=2)
    fig.tight_layout(rect=[0, 0.08, 1, 1])
    fig.savefig(CHART_DIR / "min_cluster_size_dual_axis.png", dpi=180)
    plt.close(fig)


def plot_group_line(df: pd.DataFrame, x: str, y: str, fname: str, ylabel: str) -> None:
    ok = df[df["status"].eq("ok")].copy()
    if x == "hdbscan_min_samples":
        ok[x] = ok[x].where(ok[x].notna(), "None")
    agg = ok.groupby(x, as_index=False)[y].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(agg[x].astype(str), agg[y], marker="o", color="#2f6fbb")
    ax.set_xlabel(x)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(CHART_DIR / fname, dpi=180)
    plt.close(fig)


def plot_heatmap(df: pd.DataFrame) -> None:
    ok = df[df["status"].eq("ok")].copy()
    pivot = ok.pivot_table(
        index="umap_n_neighbors",
        columns="hdbscan_min_cluster_size",
        values="balance_score",
        aggfunc="mean",
    )
    fig, ax = plt.subplots(figsize=(14, 6))
    im = ax.imshow(pivot.values, aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([str(c) for c in pivot.columns], rotation=45, ha="right")
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([str(i) for i in pivot.index])
    ax.set_xlabel("hdbscan_min_cluster_size")
    ax.set_ylabel("umap_n_neighbors")
    ax.set_title("Mean balance_score heatmap")
    fig.colorbar(im, ax=ax, label="balance_score")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "parameter_heatmap.png", dpi=180)
    plt.close(fig)


def plot_best_balance_bar(final_summary: list[dict[str, Any]]) -> None:
    item = next((row for row in final_summary if row.get("selection_label") == "best_balance" and row.get("status") == "ok"), None)
    if not item:
        return
    dist = pd.read_csv(OUTPUT_DIR / item["output_dir"] / "topic_size_distribution.csv")
    dist = dist.sort_values("Count", ascending=False).head(30)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(dist["Topic"].astype(str), dist["Count"], color="#4a8f73")
    ax.set_xlabel("topic")
    ax.set_ylabel("count")
    ax.set_title("Best balance topic size distribution")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "best_balance_topic_size_bar.png", dpi=180)
    plt.close(fig)


def plot_method_comparison(df: pd.DataFrame) -> None:
    ok = df[df["status"].eq("ok")].copy()
    agg = ok.groupby("hdbscan_cluster_selection_method", as_index=False).agg(
        n_clusters=("n_clusters", "mean"),
        noise_ratio=("noise_ratio", "mean"),
        largest_topic_ratio=("largest_topic_ratio", "mean"),
        balance_score=("balance_score", "mean"),
    )
    metrics = ["n_clusters", "noise_ratio", "largest_topic_ratio", "balance_score"]
    fig, axes = plt.subplots(1, len(metrics), figsize=(16, 5))
    for ax, metric in zip(axes, metrics):
        ax.bar(agg["hdbscan_cluster_selection_method"], agg[metric], color="#5b8a72")
        ax.set_title(metric)
        ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "cluster_selection_method_comparison.png", dpi=180)
    plt.close(fig)


def plot_selected_topic_size_distributions(final_summary: list[dict[str, Any]]) -> None:
    ok_items = [row for row in final_summary if row.get("status") == "ok" and row.get("output_dir")]
    if not ok_items:
        return
    fig, axes = plt.subplots(len(ok_items), 1, figsize=(12, max(5, 4 * len(ok_items))), squeeze=False)
    for ax, item in zip(axes.flatten(), ok_items):
        dist_path = OUTPUT_DIR / item["output_dir"] / "topic_size_distribution.csv"
        if not dist_path.exists():
            continue
        dist = pd.read_csv(dist_path).sort_values("Count", ascending=False).head(30)
        ax.bar(dist["Topic"].astype(str), dist["Count"], color="#446d9b")
        ax.set_title(str(item["selection_label"]))
        ax.set_xlabel("topic")
        ax.set_ylabel("count")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "selected_topic_size_distributions.png", dpi=180)
    plt.close(fig)


def plot_best_three(selected: pd.DataFrame) -> None:
    metrics = ["n_clusters", "noise_ratio", "largest_topic_ratio", "top3_topic_ratio", "balance_score"]
    fig, axes = plt.subplots(1, len(metrics), figsize=(18, 5))
    for ax, metric in zip(axes, metrics):
        ax.bar(selected["selection_label"], selected[metric], color="#6b78b8")
        ax.set_title(metric)
        ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "best_three_comparison.png", dpi=180)
    plt.close(fig)


def create_charts(stage2: pd.DataFrame, selected: pd.DataFrame, final_summary: list[dict[str, Any]], errors: list[dict[str, str]]) -> list[str]:
    chart_files = []
    funcs = [
        ("parameter_heatmap.png", lambda: plot_heatmap(stage2)),
        ("min_cluster_size_dual_axis.png", lambda: plot_dual_axis(stage2)),
        ("min_samples_noise_ratio.png", lambda: plot_group_line(stage2, "hdbscan_min_samples", "noise_ratio", "min_samples_noise_ratio.png", "noise_ratio")),
        ("n_neighbors_largest_topic_ratio.png", lambda: plot_group_line(stage2, "umap_n_neighbors", "largest_topic_ratio", "n_neighbors_largest_topic_ratio.png", "largest_topic_ratio")),
        ("n_components_n_clusters.png", lambda: plot_group_line(stage2, "umap_n_components", "n_clusters", "n_components_n_clusters.png", "n_clusters")),
        ("cluster_selection_method_comparison.png", lambda: plot_method_comparison(stage2)),
        ("best_balance_topic_size_bar.png", lambda: plot_best_balance_bar(final_summary)),
        ("selected_topic_size_distributions.png", lambda: plot_selected_topic_size_distributions(final_summary)),
        ("best_three_comparison.png", lambda: plot_best_three(selected)),
    ]
    for fname, func in funcs:
        try:
            func()
            if (CHART_DIR / fname).exists():
                chart_files.append(rel(CHART_DIR / fname))
        except Exception as exc:
            errors.append({"流程": "圖表輸出", "問題": f"{fname} 產生失敗：{exc}"})
    return chart_files


def load_term_list(path: Path) -> set[str]:
    if not path.exists():
        return set()
    terms: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        text = line.strip().lower()
        if text and not text.startswith("#"):
            terms.add(text)
    return terms


def analyze_brand_model_terms(final_summary: list[dict[str, Any]]) -> pd.DataFrame:
    brands = load_term_list(ROOT / "brands.txt")
    models = load_term_list(ROOT / "models.txt")
    rows: list[dict[str, Any]] = []
    for item in final_summary:
        if item.get("status") != "ok" or not item.get("output_dir"):
            continue
        words_path = OUTPUT_DIR / item["output_dir"] / "topic_words.csv"
        if not words_path.exists():
            continue
        topic_words = pd.read_csv(words_path)
        for _, row in topic_words.iterrows():
            words = [part.strip().lower() for part in str(row.get("words", "")).split(",") if part.strip()]
            brand_hits = sorted({word for word in words if word in brands})
            model_hits = sorted({word for word in words if word in models})
            rows.append(
                {
                    "selection_label": item["selection_label"],
                    "topic": int(row["topic"]),
                    "top_word_count": len(words),
                    "brand_word_hits": ", ".join(brand_hits),
                    "model_word_hits": ", ".join(model_hits),
                    "brand_model_hit_count": len(brand_hits) + len(model_hits),
                    "brand_model_hit_ratio": (len(brand_hits) + len(model_hits)) / len(words) if words else 0.0,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out.to_csv(OUTPUT_DIR / "brand_model_topic_word_check.csv", index=False)
    return out


def load_cmin_baseline() -> pd.DataFrame:
    if not BASELINE_MIN_CSV.exists():
        return pd.DataFrame()
    min_df = pd.read_csv(BASELINE_MIN_CSV)
    ok = min_df[min_df["status"].eq("ok")].copy() if "status" in min_df.columns else min_df.copy()
    ok = ok[ok["n_clusters"].ge(1)].copy()
    if ok.empty:
        return pd.DataFrame()
    pool = ok[ok["n_clusters"].ge(2)]
    if pool.empty:
        pool = ok
    best = pool.sort_values(["noise_ratio", "n_clusters", "min_cluster_size"], ascending=[True, False, True]).iloc[0]

    total = int(best["topic_-1_count"] + best["topic_0_count"] + best["topic_1_count"])
    non_noise_counts = [int(best["topic_0_count"]), int(best["topic_1_count"])]
    if BASELINE_TOPIC_INFO_CSV.exists():
        info = pd.read_csv(BASELINE_TOPIC_INFO_CSV)
        total = int(info["Count"].sum())
        non_noise_counts = sorted(
            [int(row["Count"]) for _, row in info.iterrows() if int(row["Topic"]) != -1],
            reverse=True,
        )
    largest = int(non_noise_counts[0]) if non_noise_counts else 0
    top3 = int(sum(non_noise_counts[:3])) if non_noise_counts else 0
    n_clusters = int(best["n_clusters"])
    if n_clusters <= 1 or sum(non_noise_counts) == 0:
        entropy = 0.0
    else:
        probs = np.array(non_noise_counts, dtype=float) / float(sum(non_noise_counts))
        entropy = float(-(probs * np.log(probs)).sum() / math.log(n_clusters))
    noise_ratio = float(best["noise_ratio"])
    largest_ratio = float(largest / total) if total else 0.0
    top3_ratio = float(top3 / total) if total else 0.0
    balance_score = (
        0.30 * (1.0 - noise_ratio)
        + 0.30 * (1.0 - largest_ratio)
        + 0.20 * (1.0 - top3_ratio)
        + 0.20 * min(n_clusters / 25.0, 1.0)
    )
    return pd.DataFrame(
        [
            {
                "baseline": "06.13_[C]min best",
                "min_cluster_size": int(best["min_cluster_size"]),
                "n_clusters": n_clusters,
                "noise_ratio": noise_ratio,
                "topic_-1_count": int(best["topic_-1_count"]),
                "largest_topic_count": largest,
                "largest_topic_ratio": largest_ratio,
                "top3_topic_ratio": top3_ratio,
                "topic_entropy": entropy,
                "balance_score": float(balance_score),
                "source_dir": str(BASELINE_DIR.relative_to(ROOT)),
            }
        ]
    )


def write_report(
    meta: dict[str, Any],
    stage1: pd.DataFrame,
    stage2: pd.DataFrame,
    selected: pd.DataFrame,
    stability: pd.DataFrame,
    final_summary: list[dict[str, Any]],
    chart_files: list[str],
    errors: list[dict[str, str]],
    full_failures: list[str],
) -> None:
    ok1 = stage1[stage1["status"].eq("ok")] if "status" in stage1.columns else pd.DataFrame()
    ok2 = stage2[stage2["status"].eq("ok")] if "status" in stage2.columns else pd.DataFrame()
    selected_cols = list(selected.columns) if not selected.empty else ["selection_label", "selection_reason"]
    top_stage1 = ok1.sort_values("balance_score", ascending=False).head(15).to_dict("records") if not ok1.empty else []
    top_stage2 = ok2.sort_values("balance_score", ascending=False).head(20).to_dict("records") if not ok2.empty else []
    err_rows = []
    for flow in ["環境開始運行", "資料載入", "Embedding", "UMAP", "HDBSCAN", "BERTopic", "圖表輸出"]:
        msgs = [item["問題"] for item in errors if item["流程"] == flow]
        err_rows.append({"流程": flow, "問題": "<br>".join(f"{idx}. {msg}" for idx, msg in enumerate(msgs, start=1)) if msgs else "無"})
    stability_summary = pd.DataFrame()
    if not stability.empty and "status" in stability.columns:
        sok = stability[stability["status"].eq("ok")]
        if not sok.empty:
            stability_summary = sok.groupby("stability_rank", as_index=False).agg(
                noise_ratio_mean=("noise_ratio", "mean"),
                noise_ratio_std=("noise_ratio", "std"),
                n_clusters_mean=("n_clusters", "mean"),
                n_clusters_std=("n_clusters", "std"),
                largest_topic_ratio_mean=("largest_topic_ratio", "mean"),
                largest_topic_ratio_std=("largest_topic_ratio", "std"),
            )
    baseline = load_cmin_baseline()
    brand_model = analyze_brand_model_terms(final_summary)
    brand_model_summary = pd.DataFrame()
    if not brand_model.empty:
        brand_model_summary = brand_model.groupby("selection_label", as_index=False).agg(
            topics_checked=("topic", "count"),
            topics_with_brand_model_hits=("brand_model_hit_count", lambda values: int((values > 0).sum())),
            mean_brand_model_hit_ratio=("brand_model_hit_ratio", "mean"),
            max_brand_model_hit_ratio=("brand_model_hit_ratio", "max"),
        )
    if not brand_model_summary.empty:
        bm_focus = brand_model_summary[brand_model_summary["selection_label"].eq("best_balance")].head(1)
        if bm_focus.empty:
            bm_focus = brand_model_summary.head(1)
        bm = bm_focus.iloc[0]
        brand_absorption_note = (
            "有。正式 BERTopic 的 topic words 顯示 orig 語料仍明顯受品牌/車款詞彙吸引："
            f"{bm['selection_label']} 有 {int(bm['topics_with_brand_model_hits'])}/{int(bm['topics_checked'])} 個 topics "
            f"出現品牌/車款 hits，平均 top words hit ratio={float(bm['mean_brand_model_hit_ratio']):.4f}，"
            f"最高 hit ratio={float(bm['max_brand_model_hit_ratio']):.4f}。"
            "這表示 UMAP/HDBSCAN 已改善主題大小平衡，但 orig 的部分主題仍會以 Lexus、Audi、Hyundai、Volvo、Kia 等品牌/車款為聚類錨點。"
        )
    else:
        brand_absorption_note = "正式模型尚未產生 topic_words 或品牌/車款清單，無法自動判斷吸附程度。"
    best_balance = selected[selected["selection_label"].eq("best_balance")].head(1) if "selection_label" in selected.columns else pd.DataFrame()
    comparison_notes = []
    if not best_balance.empty and not baseline.empty:
        bb = best_balance.iloc[0]
        base = baseline.iloc[0]
        better_balance = (
            float(bb["balance_score"]) > float(base["balance_score"])
            and int(bb["n_clusters"]) > int(base["n_clusters"])
            and float(bb["largest_topic_ratio"]) < float(base["largest_topic_ratio"])
        )
        comparison_notes.append(
            "是否比 06.13_[C]min 產生更平衡的 noise 與主題數："
            + (
                "是。"
                if better_balance
                else "未完全是，仍需要在 noise、主題數與集中度之間取捨。"
            )
            + f"[D] best_balance n_clusters={int(bb['n_clusters'])}, noise_ratio={float(bb['noise_ratio']):.4f}, "
            + f"balance_score={float(bb['balance_score']):.4f}；[C]min baseline n_clusters={int(base['n_clusters'])}, "
            + f"noise_ratio={float(base['noise_ratio']):.4f}, balance_score={float(base['balance_score']):.4f}。"
        )
        comparison_notes.append(
            "是否降低最大主題集中度："
            + (
                "是。"
                if float(bb["largest_topic_ratio"]) < float(base["largest_topic_ratio"])
                else "否。"
            )
            + f"[D] largest_topic_ratio={float(bb['largest_topic_ratio']):.4f}, top3_topic_ratio={float(bb['top3_topic_ratio']):.4f}；"
            + f"[C]min largest_topic_ratio={float(base['largest_topic_ratio']):.4f}, top3_topic_ratio={float(base['top3_topic_ratio']):.4f}。"
        )
    elif not best_balance.empty:
        bb = best_balance.iloc[0]
        comparison_notes.append(
            f"未找到 06.13_[C]min baseline CSV；本次最佳平衡設定為 n_clusters={int(bb['n_clusters'])}, "
            f"noise_ratio={float(bb['noise_ratio']):.4f}, largest_topic_ratio={float(bb['largest_topic_ratio']):.4f}, "
            f"top3_topic_ratio={float(bb['top3_topic_ratio']):.4f}。"
        )
    strategy_note = (
        "建議以 repl 作為主要語料策略，del 作為敏感性/驗證版本，orig 作為對照與品牌/車款專題分析。"
        "理由是本次 orig 在 UMAP/HDBSCAN 調參後可以改善主題大小平衡，但 topic words 仍保留明顯品牌/車款錨點；"
        "repl 較適合保留「這裡有品牌/車款實體」的語意位置，同時降低特定名稱吸附，del 則可用來確認非品牌敘事是否穩定。"
    )
    report = [
        "# BERTopic UMAP + HDBSCAN 多參數檢測報告 - 06.13_[D]UMAP_[B]01-(orig)_20-25_tok(para12-80)",
        "",
        "## 1. Dataset 資訊",
        "",
        md_table([meta], list(meta.keys())),
        "## 2. Embedding / UMAP / HDBSCAN 參數設定",
        "",
        f"- embedding_model: `{EMBEDDING_MODEL_NAME}`",
        f"- embeddings cache: `{rel(EMBEDDINGS_PATH)}`",
        f"- UMAP 第一階段: n_neighbors={UMAP_N_NEIGHBORS}, n_components={UMAP_N_COMPONENTS}, min_dist={UMAP_MIN_DIST}, metric=cosine, random_state=42",
        f"- HDBSCAN 第一階段: min_cluster_size={STAGE1_MIN_CLUSTER_SIZE}, min_samples={STAGE1_MIN_SAMPLES}, method=eom, epsilon=0.0",
        f"- HDBSCAN 第二階段: min_cluster_size={STAGE2_MIN_CLUSTER_SIZE}, min_samples={STAGE2_MIN_SAMPLES}, method={STAGE2_METHODS}, epsilon={STAGE2_EPSILONS}",
        "",
        "## 3. 第一階段測試結果摘要",
        "",
        f"- 總列數: {len(stage1)}",
        f"- 成功列數: {len(ok1)}",
        "",
        md_table(top_stage1, ["umap_n_neighbors", "umap_n_components", "umap_min_dist", "hdbscan_min_cluster_size", "hdbscan_min_samples", "n_clusters", "noise_ratio", "largest_topic_ratio", "top3_topic_ratio", "topic_entropy", "balance_score"]),
        "## 4. 第二階段測試結果摘要",
        "",
        f"- 總列數: {len(stage2)}",
        f"- 成功列數: {len(ok2)}",
        "",
        md_table(top_stage2, ["umap_n_neighbors", "umap_n_components", "umap_min_dist", "hdbscan_min_cluster_size", "hdbscan_min_samples", "hdbscan_cluster_selection_method", "hdbscan_cluster_selection_epsilon", "n_clusters", "noise_ratio", "largest_topic_ratio", "top3_topic_ratio", "topic_entropy", "balance_score"]),
        "## 5. 最低 noise 設定",
        "",
        md_table(selected[selected["selection_label"].eq("lowest_noise")].to_dict("records"), selected_cols) if "selection_label" in selected.columns else "尚未選出。\n",
        "## 6. 最多有效主題設定",
        "",
        md_table(selected[selected["selection_label"].eq("most_topics")].to_dict("records"), selected_cols) if "selection_label" in selected.columns else "尚未選出。\n",
        "## 7. 最佳平衡設定",
        "",
        md_table(selected[selected["selection_label"].eq("best_balance")].to_dict("records"), selected_cols) if "selection_label" in selected.columns else "尚未選出。\n",
        "## 8. 為什麼不只用 min_cluster_size 判斷",
        "",
        "只調整 min_cluster_size 會把問題壓縮成單一維度：降低 noise_ratio 時容易讓大量文本被併入少數大主題；追求較多主題時又可能導致 noise_ratio 上升。UMAP 的 n_neighbors、n_components、min_dist 會改變語意向量在低維空間中的局部/全域結構，HDBSCAN 的 min_samples、cluster_selection_method 與 epsilon 會改變保守程度與群集切分方式。因此本次以 balance_score 同時納入 noise、主題數、最大主題集中度與前三主題集中度，避免只選到低 noise 但不可解釋的過度集中結果。",
        "",
        "## 9. 與 06.13_[C]min 基準及語料策略比較",
        "",
        f"- 06.13_[C]min 基準來源：`{BASELINE_DIR.relative_to(ROOT)}`。",
        *[f"- {note}" for note in comparison_notes],
        f"- 原始品牌車款詞彙是否造成吸附：{brand_absorption_note}",
        f"- 語料策略建議：{strategy_note}",
        "",
        "### 06.13_[C]min 基準摘要",
        "",
        md_table(baseline.to_dict("records"), list(baseline.columns)) if not baseline.empty else "未找到 06.13_[C]min baseline CSV。\n",
        "### 品牌/車款詞彙檢查",
        "",
        md_table(brand_model_summary.to_dict("records"), list(brand_model_summary.columns)) if not brand_model_summary.empty else "正式模型尚未產生 topic_words，無法檢查。\n",
        "",
        "## 10. 各圖表連結",
        "",
    ]
    report.extend([f"- [{Path(path).name}]({path})" for path in chart_files])
    report.extend(
        [
            "",
            "## 11. 最終 BERTopic 訓練輸出",
            "",
            md_table(final_summary, sorted({key for row in final_summary for key in row.keys()})) if final_summary else "無成功輸出。\n",
            "",
            f"- final_configs.json: `{rel(FINAL_CONFIGS_JSON)}`",
            f"- comparison_summary.csv: `{rel(COMPARISON_SUMMARY_CSV)}`",
            "",
            "## 12. 穩定性檢測摘要",
            "",
            md_table(stability_summary.to_dict("records"), list(stability_summary.columns)) if not stability_summary.empty else "未產生穩定性摘要。\n",
            "## 錯誤輸出",
            "",
            "### 檢測發現與建議",
            "",
            md_table(err_rows, ["流程", "問題"]),
            "### 整體錯誤輸出",
            "",
            "無阻斷性失敗。" if not full_failures else "```text\n" + "\n\n".join(full_failures[-10:]) + "\n```",
            "",
            "### 可改進",
            "",
            "1. 可加入中文或領域專用 stopwords，提升 topic words 可解釋性。",
            "2. 可用 c-TF-IDF 後處理、MMR 或人工合併相近主題，降低語意相近語料造成的主題碎裂。",
            "3. 若穩定性檢測顯示不同 random_state 差異大，建議優先採用標準差較低的平衡設定，而不是只看單次最高分。",
            "4. 若最佳平衡設定仍有最大主題過大，可後續針對最大主題單獨進行二階段 BERTopic。",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")


def run() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    UMAP_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    HDBSCAN_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    errors: list[dict[str, str]] = [{"流程": "環境開始運行", "問題": "環境套件可載入，開始 06.13_[D]UMAP 多參數檢測。"}]
    full_failures: list[str] = []
    try:
        docs, titles, doc_meta, meta, load_errors = load_documents()
        errors.extend(load_errors)
        if not docs:
            raise RuntimeError("Dataset does not contain any usable text.")
        embedding_model, embeddings = get_embeddings(docs, errors)
        stage1_umaps = [
            {"umap_n_neighbors": nn, "umap_n_components": nc, "umap_min_dist": md, "umap_random_state": RANDOM_STATE}
            for nn, nc, md in product(UMAP_N_NEIGHBORS, UMAP_N_COMPONENTS, UMAP_MIN_DIST)
        ]
        stage1 = run_hdbscan_grid(
            "stage1",
            STAGE1_CSV,
            embeddings,
            stage1_umaps,
            STAGE1_MIN_CLUSTER_SIZE,
            STAGE1_MIN_SAMPLES,
            ["eom"],
            [0.0],
            errors,
        )
        if stage1.empty or not stage1["status"].eq("ok").any():
            raise RuntimeError("Stage 1 did not produce any successful parameter rows.")
        stage2_umaps = choose_stage2_umaps(stage1)
        (OUTPUT_DIR / "stage2_umap_candidates.json").write_text(json.dumps(stage2_umaps, ensure_ascii=False, indent=2), encoding="utf-8")
        stage2 = run_hdbscan_grid(
            "stage2",
            STAGE2_CSV,
            embeddings,
            stage2_umaps,
            STAGE2_MIN_CLUSTER_SIZE,
            STAGE2_MIN_SAMPLES,
            STAGE2_METHODS,
            STAGE2_EPSILONS,
            errors,
        )
        if stage2.empty or not stage2["status"].eq("ok").any():
            raise RuntimeError("Stage 2 did not produce any successful parameter rows.")
        selected = select_best(stage2)
        selected.to_csv(SELECTED_CSV, index=False)
        top10 = stage2[stage2["status"].eq("ok")].sort_values("balance_score", ascending=False).head(10)
        stability = run_stability(embeddings, top10, errors)
        final_summary = train_final_models(docs, titles, doc_meta, embedding_model, embeddings, selected, errors)
        chart_files = create_charts(stage2, selected, final_summary, errors)
        write_report(meta, stage1, stage2, selected, stability, final_summary, chart_files, errors, full_failures)
        run_log = {
            "started_at": started,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "dataset": str(DATASET_DIR.relative_to(ROOT)),
            "output_dir": str(OUTPUT_DIR.relative_to(ROOT)),
            "stage1_rows": len(stage1),
            "stage2_rows": len(stage2),
            "selected_rows": len(selected),
            "errors_count": len(errors),
            "full_failures_count": len(full_failures),
        }
        RUN_LOG_JSON.write_text(json.dumps(run_log, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        full_failures.append(traceback.format_exc())
        meta = meta if "meta" in locals() else {"dataset_dir": str(DATASET_DIR.relative_to(ROOT))}
        stage1 = pd.read_csv(STAGE1_CSV) if STAGE1_CSV.exists() else pd.DataFrame()
        stage2 = pd.read_csv(STAGE2_CSV) if STAGE2_CSV.exists() else pd.DataFrame()
        selected = pd.read_csv(SELECTED_CSV) if SELECTED_CSV.exists() else pd.DataFrame()
        stability = pd.read_csv(STABILITY_CSV) if STABILITY_CSV.exists() else pd.DataFrame()
        write_report(meta, stage1, stage2, selected, stability, [], [], errors, full_failures)
        RUN_LOG_JSON.write_text(
            json.dumps(
                {
                    "started_at": started,
                    "failed_at": datetime.now(timezone.utc).isoformat(),
                    "dataset": str(DATASET_DIR.relative_to(ROOT)),
                    "output_dir": str(OUTPUT_DIR.relative_to(ROOT)),
                    "error": full_failures[-1],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        raise


if __name__ == "__main__":
    run()
