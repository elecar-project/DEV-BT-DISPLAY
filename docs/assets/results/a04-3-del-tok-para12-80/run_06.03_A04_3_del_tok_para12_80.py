from __future__ import annotations

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
DATASET_DIR = ROOT / "Result/06.03_A02/R06.03_A02-pre_LLM(del)_tok(para12-80)_dataset"
OUTPUT_DIR = ROOT / "Result/06.03_A04_min-test/A04-3(del)_tok(para12-80)"
CACHE_DIR = OUTPUT_DIR / "cache"
HDBSCAN_CACHE_DIR = CACHE_DIR / "hdbscan_memory"
FINAL_DIR = OUTPUT_DIR / "final_models"
CHART_DIR = OUTPUT_DIR / "charts"

REPORT_PATH = OUTPUT_DIR / "Result_06.03_A04-3(del)_tok(para12-80).md"
STAGE1_CSV = OUTPUT_DIR / "Result_06.03_A04-3(del)_tok(para12-80)-stage1_umap_hdbscan.csv"
STAGE2_CSV = OUTPUT_DIR / "Result_06.03_A04-3(del)_tok(para12-80)-stage2_hdbscan_deep.csv"
STABILITY_CSV = OUTPUT_DIR / "Result_06.03_A04-3(del)_tok(para12-80)-top10_stability.csv"
ALL_RESULTS_CSV = OUTPUT_DIR / "Result_06.03_A04-3(del)_tok(para12-80)-all_results.csv"
RUN_LOG_JSON = OUTPUT_DIR / "Result_06.03_A04-3(del)_tok(para12-80)-run_log.json"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TEXT_COLUMN = "sentence"
UMAP_RANDOM_STATE = 42
STABILITY_RANDOM_STATES = [42, 123, 2026, 3407, 20240603]
HDBSCAN_CORE_DIST_N_JOBS = 2

STAGE1_UMAP_GRID = {
    "n_neighbors": [5, 10, 15, 30, 50, 75, 100],
    "n_components": [5, 10, 15],
    "min_dist": [0.0, 0.05, 0.1, 0.25],
}
STAGE1_HDBSCAN_GRID = {
    "min_cluster_size": [50, 75, 100, 125, 150, 175, 200, 225, 250, 300],
    "min_samples": [None, 10, 30],
    "cluster_selection_method": ["eom"],
    "cluster_selection_epsilon": [0.0],
}
STAGE2_HDBSCAN_GRID = {
    "min_cluster_size": [
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
    ],
    "min_samples": [None, 5, 10, 15, 30, 50, 75, 100],
    "cluster_selection_method": ["eom", "leaf"],
    "cluster_selection_epsilon": [0.0, 0.05, 0.1, 0.2],
}

RESULT_COLUMNS = [
    "stage",
    "umap_n_neighbors",
    "umap_n_components",
    "umap_min_dist",
    "umap_metric",
    "umap_random_state",
    "hdbscan_min_cluster_size",
    "hdbscan_min_samples",
    "hdbscan_cluster_selection_method",
    "hdbscan_cluster_selection_epsilon",
    "hdbscan_metric",
    "n_clusters",
    "noise_ratio",
    "topic_-1_count",
    "topic_0_count",
    "topic_1_count",
    "largest_topic_count",
    "largest_topic_ratio",
    "top3_topic_ratio",
    "topic_entropy",
    "balance_score",
    "status",
    "note",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


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


def load_documents() -> tuple[list[str], list[str], dict[str, Any], list[dict[str, str]]]:
    dataset = load_from_disk(str(DATASET_DIR))
    columns = list(dataset.column_names)
    if TEXT_COLUMN not in columns:
        raise ValueError(f"Dataset missing required text column: {TEXT_COLUMN}")

    documents: list[str] = []
    titles: list[str] = []
    row_ids: list[int] = []
    empty_rows: list[int] = []
    short_rows: list[int] = []
    for idx, item in enumerate(dataset):
        text = "" if item.get(TEXT_COLUMN) is None else str(item.get(TEXT_COLUMN)).strip()
        if not text:
            empty_rows.append(idx)
            continue
        documents.append(text)
        titles.append(str(item.get("title", "")))
        row_ids.append(idx)
        if len(text.split()) < 3:
            short_rows.append(idx)

    text_lens = [len(doc) for doc in documents]
    word_counts = [len(doc.split()) for doc in documents]
    meta = {
        "dataset_dir": str(DATASET_DIR.relative_to(ROOT)),
        "columns": columns,
        "text_col": TEXT_COLUMN,
        "source_rows": len(dataset),
        "used_rows": len(documents),
        "row_ids": row_ids,
        "empty_rows_count": len(empty_rows),
        "empty_rows_sample": empty_rows[:20],
        "short_rows_lt_3_words_count": len(short_rows),
        "short_rows_lt_3_words_sample": short_rows[:20],
        "min_text_len": min(text_lens, default=0),
        "avg_text_len": float(np.mean(text_lens)) if text_lens else 0.0,
        "max_text_len": max(text_lens, default=0),
        "min_word_count": min(word_counts, default=0),
        "avg_word_count": float(np.mean(word_counts)) if word_counts else 0.0,
        "max_word_count": max(word_counts, default=0),
    }
    errors: list[dict[str, str]] = []
    if empty_rows:
        errors.append({"流程": "資料載入", "問題": f"有 {len(empty_rows)} 筆空白文本已排除。"})
    if short_rows:
        errors.append({"流程": "資料載入", "問題": f"有 {len(short_rows)} 筆少於 3 words 的短文本保留，可能影響密度分群。"})
    return documents, titles, meta, errors


def get_embeddings(documents: list[str]) -> tuple[SentenceTransformer, np.ndarray, list[dict[str, str]]]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    errors = [{"流程": "Embedding", "問題": f"使用 {EMBEDDING_MODEL_NAME}；embeddings 只計算一次並快取。"}]
    cache_path = CACHE_DIR / "embeddings_all-MiniLM-L6-v2.npy"
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    if cache_path.exists():
        embeddings = np.load(cache_path)
        if len(embeddings) == len(documents):
            errors.append({"流程": "Embedding", "問題": f"載入既有快取：{cache_path.relative_to(ROOT)}。"})
            return model, embeddings, errors
        errors.append({"流程": "Embedding", "問題": "既有 embedding 快取筆數不符，已重新計算。"})
    embeddings = model.encode(documents, show_progress_bar=True, batch_size=64, convert_to_numpy=True)
    np.save(cache_path, embeddings)
    errors.append({"流程": "Embedding", "問題": f"已寫入快取：{cache_path.relative_to(ROOT)}。"})
    return model, embeddings, errors


def umap_cache_name(n_neighbors: int, n_components: int, min_dist: float, random_state: int) -> Path:
    dist = str(min_dist).replace(".", "p")
    return CACHE_DIR / f"umap_nn{n_neighbors}_nc{n_components}_md{dist}_rs{random_state}.npy"


def get_umap_embeddings(
    embeddings: np.ndarray,
    n_neighbors: int,
    n_components: int,
    min_dist: float,
    random_state: int,
) -> np.ndarray:
    path = umap_cache_name(n_neighbors, n_components, min_dist, random_state)
    if path.exists():
        return np.load(path)
    reduced = UMAP(
        n_neighbors=n_neighbors,
        n_components=n_components,
        min_dist=min_dist,
        metric="cosine",
        random_state=random_state,
    ).fit_transform(embeddings)
    np.save(path, reduced)
    return reduced


def hdbscan_grid(grid: dict[str, list[Any]]) -> list[dict[str, Any]]:
    return [
        {
            "min_cluster_size": min_cluster_size,
            "min_samples": min_samples,
            "cluster_selection_method": method,
            "cluster_selection_epsilon": epsilon,
        }
        for min_cluster_size, min_samples, method, epsilon in product(
            grid["min_cluster_size"],
            grid["min_samples"],
            grid["cluster_selection_method"],
            grid["cluster_selection_epsilon"],
        )
    ]


def base_result(
    stage: str,
    umap_cfg: dict[str, Any],
    hdbscan_cfg: dict[str, Any],
    status: str = "pending",
    note: str = "",
) -> dict[str, Any]:
    return {
        "stage": stage,
        "umap_n_neighbors": int(umap_cfg["n_neighbors"]),
        "umap_n_components": int(umap_cfg["n_components"]),
        "umap_min_dist": float(umap_cfg["min_dist"]),
        "umap_metric": "cosine",
        "umap_random_state": int(umap_cfg.get("random_state", UMAP_RANDOM_STATE)),
        "hdbscan_min_cluster_size": int(hdbscan_cfg["min_cluster_size"]),
        "hdbscan_min_samples": hdbscan_cfg["min_samples"],
        "hdbscan_cluster_selection_method": hdbscan_cfg["cluster_selection_method"],
        "hdbscan_cluster_selection_epsilon": float(hdbscan_cfg["cluster_selection_epsilon"]),
        "hdbscan_metric": "euclidean",
        "n_clusters": np.nan,
        "noise_ratio": np.nan,
        "topic_-1_count": np.nan,
        "topic_0_count": np.nan,
        "topic_1_count": np.nan,
        "largest_topic_count": np.nan,
        "largest_topic_ratio": np.nan,
        "top3_topic_ratio": np.nan,
        "topic_entropy": np.nan,
        "balance_score": np.nan,
        "status": status,
        "note": note,
    }


def label_metrics(labels: np.ndarray) -> dict[str, Any]:
    counts = Counter(int(label) for label in labels)
    total = len(labels)
    topic_counts = sorted([count for topic, count in counts.items() if topic != -1], reverse=True)
    n_clusters = len(topic_counts)
    largest = topic_counts[0] if topic_counts else 0
    top3 = sum(topic_counts[:3])
    noise_ratio = counts.get(-1, 0) / total if total else 0.0
    largest_topic_ratio = largest / total if total else 0.0
    top3_topic_ratio = top3 / total if total else 0.0
    if n_clusters > 1 and sum(topic_counts) > 0:
        probs = np.array(topic_counts, dtype=float) / float(sum(topic_counts))
        entropy = float(-(probs * np.log(probs)).sum() / math.log(n_clusters))
    else:
        entropy = 0.0
    balance_score = (
        0.30 * (1 - noise_ratio)
        + 0.30 * (1 - largest_topic_ratio)
        + 0.20 * (1 - top3_topic_ratio)
        + 0.20 * min(n_clusters / 25, 1)
    )
    return {
        "n_clusters": int(n_clusters),
        "noise_ratio": float(noise_ratio),
        "topic_-1_count": int(counts.get(-1, 0)),
        "topic_0_count": int(counts.get(0, 0)),
        "topic_1_count": int(counts.get(1, 0)),
        "largest_topic_count": int(largest),
        "largest_topic_ratio": float(largest_topic_ratio),
        "top3_topic_ratio": float(top3_topic_ratio),
        "topic_entropy": float(entropy),
        "balance_score": float(balance_score),
    }


def run_hdbscan(
    reduced_embeddings: np.ndarray,
    umap_cfg: dict[str, Any],
    hdbscan_cfg: dict[str, Any],
    stage: str,
) -> dict[str, Any]:
    row = base_result(stage, umap_cfg, hdbscan_cfg)
    try:
        labels = HDBSCAN(
            min_cluster_size=int(hdbscan_cfg["min_cluster_size"]),
            min_samples=hdbscan_cfg["min_samples"],
            metric="euclidean",
            cluster_selection_method=hdbscan_cfg["cluster_selection_method"],
            cluster_selection_epsilon=float(hdbscan_cfg["cluster_selection_epsilon"]),
            prediction_data=False,
            core_dist_n_jobs=HDBSCAN_CORE_DIST_N_JOBS,
            memory=Memory(location=str(HDBSCAN_CACHE_DIR), verbose=0),
        ).fit_predict(reduced_embeddings)
        row.update(label_metrics(labels))
        row["status"] = "ok"
        row["note"] = "完成"
    except Exception as exc:
        row["status"] = "failed"
        row["note"] = f"{type(exc).__name__}: {exc}"
    return row


def read_existing(path: Path) -> pd.DataFrame:
    if path.exists() and path.stat().st_size > 0:
        return pd.read_csv(path)
    return pd.DataFrame(columns=RESULT_COLUMNS)


def result_key(row: dict[str, Any]) -> tuple[Any, ...]:
    min_samples = row["hdbscan_min_samples"]
    if pd.isna(min_samples) or str(min_samples).lower() in {"none", "nan", ""}:
        min_samples_key = "None"
    else:
        min_samples_key = str(int(float(min_samples)))
    return (
        row["stage"],
        int(row["umap_n_neighbors"]),
        int(row["umap_n_components"]),
        float(row["umap_min_dist"]),
        int(row["umap_random_state"]),
        int(row["hdbscan_min_cluster_size"]),
        min_samples_key,
        row["hdbscan_cluster_selection_method"],
        float(row["hdbscan_cluster_selection_epsilon"]),
    )


def append_row(path: Path, row: dict[str, Any]) -> None:
    df = pd.DataFrame([{col: row.get(col) for col in RESULT_COLUMNS}])
    df.to_csv(path, mode="a", header=not path.exists(), index=False)


def run_search(
    embeddings: np.ndarray,
    stage: str,
    umap_configs: list[dict[str, Any]],
    hdbscan_configs: list[dict[str, Any]],
    out_csv: Path,
) -> pd.DataFrame:
    existing = read_existing(out_csv)
    done = set()
    if not existing.empty:
        for item in existing.to_dict("records"):
            done.add(result_key(item))

    total = len(umap_configs) * len(hdbscan_configs)
    completed = len(done)
    for umap_cfg in umap_configs:
        reduced = get_umap_embeddings(
            embeddings,
            int(umap_cfg["n_neighbors"]),
            int(umap_cfg["n_components"]),
            float(umap_cfg["min_dist"]),
            int(umap_cfg.get("random_state", UMAP_RANDOM_STATE)),
        )
        for hdbscan_cfg in hdbscan_configs:
            probe = base_result(stage, umap_cfg, hdbscan_cfg)
            key = result_key(probe)
            if key in done:
                continue
            row = run_hdbscan(reduced, umap_cfg, hdbscan_cfg, stage)
            append_row(out_csv, row)
            done.add(key)
            completed += 1
            if completed % 100 == 0 or row["status"] != "ok":
                print(f"[{now_utc()}] {stage}: {completed}/{total} last_status={row['status']}", flush=True)
    return read_existing(out_csv)


def stage1_umap_configs() -> list[dict[str, Any]]:
    return [
        {
            "n_neighbors": n_neighbors,
            "n_components": n_components,
            "min_dist": min_dist,
            "random_state": UMAP_RANDOM_STATE,
        }
        for n_neighbors, n_components, min_dist in product(
            STAGE1_UMAP_GRID["n_neighbors"],
            STAGE1_UMAP_GRID["n_components"],
            STAGE1_UMAP_GRID["min_dist"],
        )
    ]


def choose_top10_umap(stage1: pd.DataFrame) -> pd.DataFrame:
    ok = stage1[stage1["status"].eq("ok")].copy()
    grouped = (
        ok.groupby(["umap_n_neighbors", "umap_n_components", "umap_min_dist"], dropna=False)
        .agg(
            best_balance_score=("balance_score", "max"),
            best_noise_ratio=("noise_ratio", "min"),
            best_n_clusters=("n_clusters", "max"),
            best_largest_topic_ratio=("largest_topic_ratio", "min"),
            mean_balance_score=("balance_score", "mean"),
        )
        .reset_index()
    )
    grouped = grouped.sort_values(
        by=["best_balance_score", "best_noise_ratio", "best_n_clusters", "best_largest_topic_ratio"],
        ascending=[False, True, False, True],
    )
    return grouped.head(10).reset_index(drop=True)


def select_best_rows(results: pd.DataFrame) -> dict[str, dict[str, Any]]:
    ok = results[results["status"].eq("ok") & (results["n_clusters"] >= 1)].copy()
    if ok.empty:
        return {}
    lowest_noise = ok.sort_values(
        by=["noise_ratio", "largest_topic_ratio", "top3_topic_ratio", "n_clusters"],
        ascending=[True, True, True, False],
    ).iloc[0]
    most_topics = ok.sort_values(
        by=["n_clusters", "noise_ratio", "largest_topic_ratio"],
        ascending=[False, True, True],
    ).iloc[0]
    strict = ok[
        (ok["n_clusters"] >= 4)
        & (ok["noise_ratio"] <= 0.35)
        & (ok["largest_topic_ratio"] <= 0.65)
        & (ok["top3_topic_ratio"] <= 0.85)
    ]
    relaxed_used = False
    if strict.empty:
        strict = ok[
            (ok["n_clusters"] >= 3)
            & (ok["noise_ratio"] <= 0.45)
            & (ok["largest_topic_ratio"] <= 0.75)
        ]
        relaxed_used = True
    pool = strict if not strict.empty else ok
    best_balance = pool.sort_values(
        by=["balance_score", "topic_entropy", "noise_ratio"],
        ascending=[False, False, True],
    ).iloc[0]
    payload = {
        "lowest_noise": lowest_noise.to_dict(),
        "most_topics": most_topics.to_dict(),
        "best_balance": best_balance.to_dict(),
    }
    payload["best_balance"]["selection_note"] = "使用放寬條件" if relaxed_used else "使用原始最佳平衡條件"
    return payload


def make_umap_model(row: dict[str, Any], random_state: int | None = None) -> UMAP:
    return UMAP(
        n_neighbors=int(row["umap_n_neighbors"]),
        n_components=int(row["umap_n_components"]),
        min_dist=float(row["umap_min_dist"]),
        metric="cosine",
        random_state=int(random_state if random_state is not None else row["umap_random_state"]),
    )


def make_hdbscan_model(row: dict[str, Any], prediction_data: bool = True) -> HDBSCAN:
    min_samples = row["hdbscan_min_samples"]
    if pd.isna(min_samples) or str(min_samples) == "None":
        min_samples = None
    else:
        min_samples = int(min_samples)
    return HDBSCAN(
        min_cluster_size=int(row["hdbscan_min_cluster_size"]),
        min_samples=min_samples,
        metric="euclidean",
        cluster_selection_method=str(row["hdbscan_cluster_selection_method"]),
        cluster_selection_epsilon=float(row["hdbscan_cluster_selection_epsilon"]),
        prediction_data=prediction_data,
        core_dist_n_jobs=HDBSCAN_CORE_DIST_N_JOBS,
        memory=Memory(location=str(HDBSCAN_CACHE_DIR), verbose=0),
    )


def safe_name(name: str) -> str:
    return name.replace(" ", "_").replace("/", "_")


def train_final_model(
    label: str,
    row: dict[str, Any],
    documents: list[str],
    titles: list[str],
    row_ids: list[int],
    embedding_model: SentenceTransformer,
    embeddings: np.ndarray,
) -> dict[str, Any]:
    out_dir = FINAL_DIR / safe_name(label)
    out_dir.mkdir(parents=True, exist_ok=True)
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=make_umap_model(row),
        hdbscan_model=make_hdbscan_model(row, prediction_data=True),
        vectorizer_model=CountVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2),
        top_n_words=12,
        calculate_probabilities=False,
        verbose=False,
    )
    topics, _ = topic_model.fit_transform(documents, embeddings)
    topic_info = topic_model.get_topic_info()
    doc_topics = pd.DataFrame(
        {
            "source_dataset_row": row_ids,
            "title": titles,
            "sentence": documents,
            "topic": [int(topic) for topic in topics],
        }
    )

    topic_words_rows: list[dict[str, Any]] = []
    representative_rows: list[dict[str, Any]] = []
    for topic_id in topic_info["Topic"].tolist():
        words = topic_model.get_topic(int(topic_id)) or []
        topic_words_rows.append(
            {
                "topic": int(topic_id),
                "words": ", ".join([word for word, _ in words]),
                "weighted_words": ", ".join([f"{word}:{weight:.4f}" for word, weight in words]),
            }
        )
        reps = topic_model.get_representative_docs(int(topic_id)) or []
        for rank, doc in enumerate(reps[:10], start=1):
            representative_rows.append({"topic": int(topic_id), "rank": rank, "representative_doc": doc})

    topic_info_path = out_dir / "topic_info.csv"
    doc_topics_path = out_dir / "document_topics.csv"
    topic_words_path = out_dir / "topic_words.csv"
    representative_path = out_dir / "topic_representative_docs.csv"
    config_path = out_dir / "final_config.json"
    chart_path = out_dir / "topic_distribution.png"

    topic_info.to_csv(topic_info_path, index=False)
    doc_topics.to_csv(doc_topics_path, index=False)
    pd.DataFrame(topic_words_rows).to_csv(topic_words_path, index=False)
    pd.DataFrame(representative_rows).to_csv(representative_path, index=False)

    counts = doc_topics["topic"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar([str(idx) for idx in counts.index], counts.values, color="#4C78A8")
    ax.set_title(f"Topic distribution - {label}")
    ax.set_xlabel("Topic")
    ax.set_ylabel("Document count")
    ax.tick_params(axis="x", rotation=60)
    fig.tight_layout()
    fig.savefig(chart_path, dpi=160)
    plt.close(fig)

    config = {
        "label": label,
        "created_at": now_utc(),
        "dataset": str(DATASET_DIR.relative_to(ROOT)),
        "embedding_model": EMBEDDING_MODEL_NAME,
        "umap": {
            "n_neighbors": int(row["umap_n_neighbors"]),
            "n_components": int(row["umap_n_components"]),
            "min_dist": float(row["umap_min_dist"]),
            "metric": "cosine",
            "random_state": int(row["umap_random_state"]),
        },
        "hdbscan": {
            "min_cluster_size": int(row["hdbscan_min_cluster_size"]),
            "min_samples": None
            if pd.isna(row["hdbscan_min_samples"]) or str(row["hdbscan_min_samples"]) == "None"
            else int(row["hdbscan_min_samples"]),
            "cluster_selection_method": str(row["hdbscan_cluster_selection_method"]),
            "cluster_selection_epsilon": float(row["hdbscan_cluster_selection_epsilon"]),
            "metric": "euclidean",
        },
        "metrics_from_search": {
            key: row.get(key)
            for key in [
                "n_clusters",
                "noise_ratio",
                "largest_topic_ratio",
                "top3_topic_ratio",
                "topic_entropy",
                "balance_score",
            ]
        },
        "outputs": {
            "topic_info": str(topic_info_path.relative_to(ROOT)),
            "document_topics": str(doc_topics_path.relative_to(ROOT)),
            "topic_words": str(topic_words_path.relative_to(ROOT)),
            "representative_docs": str(representative_path.relative_to(ROOT)),
            "topic_distribution_chart": str(chart_path.relative_to(ROOT)),
        },
    }
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "label": label,
        "topic_info": str(topic_info_path.relative_to(ROOT)),
        "document_topics": str(doc_topics_path.relative_to(ROOT)),
        "topic_words": str(topic_words_path.relative_to(ROOT)),
        "representative_docs": str(representative_path.relative_to(ROOT)),
        "topic_distribution_chart": str(chart_path.relative_to(ROOT)),
        "final_config": str(config_path.relative_to(ROOT)),
        "n_topic_info_rows": int(len(topic_info)),
    }


def save_line_chart_dual(df: pd.DataFrame) -> str:
    path = CHART_DIR / "01_min_cluster_size_vs_n_clusters_noise_ratio.png"
    grouped = (
        df[df["status"].eq("ok")]
        .groupby("hdbscan_min_cluster_size")
        .agg(n_clusters=("n_clusters", "mean"), noise_ratio=("noise_ratio", "mean"))
        .reset_index()
    )
    fig, ax1 = plt.subplots(figsize=(11, 5))
    ax1.plot(grouped["hdbscan_min_cluster_size"], grouped["n_clusters"], marker="o", color="#4C78A8")
    ax1.set_xlabel("min_cluster_size")
    ax1.set_ylabel("mean n_clusters", color="#4C78A8")
    ax2 = ax1.twinx()
    ax2.plot(grouped["hdbscan_min_cluster_size"], grouped["noise_ratio"], marker="s", color="#F58518")
    ax2.set_ylabel("mean noise_ratio", color="#F58518")
    ax1.set_title("min_cluster_size vs n_clusters / noise_ratio")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return str(path.relative_to(ROOT))


def save_box_or_bar(df: pd.DataFrame, x_col: str, y_col: str, title: str, filename: str) -> str:
    path = CHART_DIR / filename
    ok = df[df["status"].eq("ok")].copy()
    ok[x_col] = ok[x_col].astype(object).where(ok[x_col].notna(), "None")
    groups = [group[y_col].dropna().values for _, group in ok.groupby(x_col, dropna=False)]
    labels = [str(name) for name, _ in ok.groupby(x_col, dropna=False)]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.boxplot(groups, labels=labels, showfliers=False)
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return str(path.relative_to(ROOT))


def save_method_chart(df: pd.DataFrame) -> str:
    path = CHART_DIR / "05_cluster_selection_method_comparison.png"
    ok = df[df["status"].eq("ok")].copy()
    grouped = (
        ok.groupby("hdbscan_cluster_selection_method")
        .agg(noise_ratio=("noise_ratio", "mean"), n_clusters=("n_clusters", "mean"), balance_score=("balance_score", "mean"))
        .reset_index()
    )
    x = np.arange(len(grouped))
    width = 0.25
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - width, grouped["noise_ratio"], width, label="noise_ratio")
    ax.bar(x, grouped["n_clusters"] / max(grouped["n_clusters"].max(), 1), width, label="n_clusters scaled")
    ax.bar(x + width, grouped["balance_score"], width, label="balance_score")
    ax.set_xticks(x)
    ax.set_xticklabels(grouped["hdbscan_cluster_selection_method"].tolist())
    ax.set_title("cluster_selection_method comparison")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return str(path.relative_to(ROOT))


def save_best_compare(best: dict[str, dict[str, Any]]) -> str:
    path = CHART_DIR / "06_best_three_settings_comparison.png"
    rows = []
    for label, row in best.items():
        rows.append(
            {
                "label": label,
                "noise_ratio": float(row["noise_ratio"]),
                "largest_topic_ratio": float(row["largest_topic_ratio"]),
                "top3_topic_ratio": float(row["top3_topic_ratio"]),
                "balance_score": float(row["balance_score"]),
            }
        )
    data = pd.DataFrame(rows)
    metrics = ["noise_ratio", "largest_topic_ratio", "top3_topic_ratio", "balance_score"]
    x = np.arange(len(data))
    width = 0.18
    fig, ax = plt.subplots(figsize=(11, 5))
    for i, metric in enumerate(metrics):
        ax.bar(x + (i - 1.5) * width, data[metric], width, label=metric)
    ax.set_xticks(x)
    ax.set_xticklabels(data["label"].tolist())
    ax.set_ylim(0, max(1.0, float(data[metrics].max().max()) * 1.1))
    ax.set_title("Lowest noise / most topics / best balance comparison")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return str(path.relative_to(ROOT))


def make_charts(all_results: pd.DataFrame, best: dict[str, dict[str, Any]]) -> list[str]:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    paths = [
        save_line_chart_dual(all_results),
        save_box_or_bar(
            all_results,
            "umap_n_neighbors",
            "largest_topic_ratio",
            "UMAP n_neighbors vs largest_topic_ratio",
            "02_umap_n_neighbors_vs_largest_topic_ratio.png",
        ),
        save_box_or_bar(
            all_results,
            "umap_n_components",
            "n_clusters",
            "UMAP n_components vs n_clusters",
            "03_umap_n_components_vs_n_clusters.png",
        ),
        save_box_or_bar(
            all_results,
            "hdbscan_min_samples",
            "noise_ratio",
            "HDBSCAN min_samples vs noise_ratio",
            "04_hdbscan_min_samples_vs_noise_ratio.png",
        ),
        save_method_chart(all_results),
    ]
    if best:
        paths.append(save_best_compare(best))
    return paths


def format_config_short(row: dict[str, Any]) -> str:
    return (
        f"UMAP(nn={int(row['umap_n_neighbors'])}, nc={int(row['umap_n_components'])}, "
        f"min_dist={float(row['umap_min_dist'])}, rs={int(row['umap_random_state'])}); "
        f"HDBSCAN(mcs={int(row['hdbscan_min_cluster_size'])}, "
        f"min_samples={row['hdbscan_min_samples']}, "
        f"method={row['hdbscan_cluster_selection_method']}, "
        f"eps={float(row['hdbscan_cluster_selection_epsilon'])})"
    )


def write_report(
    meta: dict[str, Any],
    errors: list[dict[str, str]],
    failures: list[str],
    improvements: list[str],
    stage1: pd.DataFrame,
    top10_umap: pd.DataFrame,
    stage2: pd.DataFrame,
    stability: pd.DataFrame,
    all_results: pd.DataFrame,
    best: dict[str, dict[str, Any]],
    final_outputs: list[dict[str, Any]],
    chart_paths: list[str],
) -> None:
    best_rows = []
    for label, row in best.items():
        best_rows.append(
            {
                "選擇": label,
                "設定": format_config_short(row),
                "n_clusters": row["n_clusters"],
                "noise_ratio": row["noise_ratio"],
                "largest_topic_ratio": row["largest_topic_ratio"],
                "top3_topic_ratio": row["top3_topic_ratio"],
                "topic_entropy": row["topic_entropy"],
                "balance_score": row["balance_score"],
                "理由": "最低 noise"
                if label == "lowest_noise"
                else "最多有效主題"
                if label == "most_topics"
                else row.get("selection_note", "最佳平衡"),
            }
        )

    top10_rows = top10_umap.to_dict("records")
    final_rows = final_outputs
    chart_rows = [{"圖表": path} for path in chart_paths]

    full_table_cols = [
        "stage",
        "umap_n_neighbors",
        "umap_n_components",
        "umap_min_dist",
        "umap_random_state",
        "hdbscan_min_cluster_size",
        "hdbscan_min_samples",
        "hdbscan_cluster_selection_method",
        "hdbscan_cluster_selection_epsilon",
        "n_clusters",
        "noise_ratio",
        "topic_-1_count",
        "topic_0_count",
        "topic_1_count",
        "largest_topic_count",
        "largest_topic_ratio",
        "top3_topic_ratio",
        "topic_entropy",
        "balance_score",
        "status",
        "note",
    ]
    ok_for_report = all_results.copy()
    ok_for_report = ok_for_report.sort_values(
        by=["stage", "balance_score", "noise_ratio"], ascending=[True, False, True]
    )
    full_rows = ok_for_report[full_table_cols].to_dict("records")

    if not errors:
        errors = [{"流程": "環境開始運行", "問題": "無重大錯誤。"}]
    required_error_rows = []
    required_flows = ["環境開始運行", "資料載入", "Embedding", "UMAP", "HDBSCAN", "BERTopic", "圖表輸出"]
    for flow in required_flows:
        matches = [item["問題"] for item in errors if item["流程"] == flow]
        required_error_rows.append({"流程": flow, "問題": "<br>".join(matches) if matches else ""})

    report = [
        "# BERTopic UMAP + HDBSCAN 多參數組合測試報告 - 06.03_A04-3(del)_tok(para12-80)",
        "",
        f"- 建立時間：{now_utc()}",
        f"- 資料來源：`{meta['dataset_dir']}`",
        f"- 文本欄位：`{meta['text_col']}`",
        f"- 原始筆數：{meta['source_rows']}",
        f"- 可用 documents：{meta['used_rows']}",
        f"- 文本長度：min={meta['min_text_len']}, avg={meta['avg_text_len']:.1f}, max={meta['max_text_len']}",
        f"- word_count：min={meta['min_word_count']}, avg={meta['avg_word_count']:.1f}, max={meta['max_word_count']}",
        "",
        "## 搜尋設定",
        "",
        md_table(
            [
                {"項目": "Embedding", "設定": f"{EMBEDDING_MODEL_NAME}; embeddings 快取於 `cache/embeddings_all-MiniLM-L6-v2.npy`"},
                {"項目": "UMAP 第一階段", "設定": "n_neighbors=5,10,15,30,50,75,100; n_components=5,10,15; min_dist=0.0,0.05,0.1,0.25; metric=cosine; random_state=42"},
                {"項目": "HDBSCAN 第一階段", "設定": "min_cluster_size=50..300 指定清單; min_samples=None,10,30; method=eom; epsilon=0.0"},
                {"項目": "HDBSCAN 第二階段", "設定": "前 10 組 UMAP 設定；min_cluster_size=50..1000 指定清單; min_samples=None,5,10,15,30,50,75,100; method=eom/leaf; epsilon=0.0,0.05,0.1,0.2"},
                {"項目": "穩定性檢測", "設定": "最佳前 10 組參數以 random_state=42,123,2026,3407,20240603 重跑"},
            ],
            ["項目", "設定"],
        ),
        "## 第一階段挑出的前 10 組 UMAP 設定",
        "",
        md_table(
            top10_rows,
            [
                "umap_n_neighbors",
                "umap_n_components",
                "umap_min_dist",
                "best_balance_score",
                "best_noise_ratio",
                "best_n_clusters",
                "best_largest_topic_ratio",
                "mean_balance_score",
            ],
        ),
        "## 最佳設定選擇",
        "",
        md_table(
            best_rows,
            [
                "選擇",
                "設定",
                "n_clusters",
                "noise_ratio",
                "largest_topic_ratio",
                "top3_topic_ratio",
                "topic_entropy",
                "balance_score",
                "理由",
            ],
        ),
        "## 圖表連結",
        "",
        md_table(chart_rows, ["圖表"]),
        "## 最終 BERTopic 訓練輸出",
        "",
        md_table(
            final_rows,
            [
                "label",
                "topic_info",
                "document_topics",
                "topic_words",
                "representative_docs",
                "topic_distribution_chart",
                "final_config",
                "n_topic_info_rows",
            ],
        ),
        "## 完整參數表",
        "",
        f"- 第一階段 CSV：`{STAGE1_CSV.relative_to(ROOT)}`",
        f"- 第二階段 CSV：`{STAGE2_CSV.relative_to(ROOT)}`",
        f"- 穩定性檢測 CSV：`{STABILITY_CSV.relative_to(ROOT)}`",
        f"- 合併完整 CSV：`{ALL_RESULTS_CSV.relative_to(ROOT)}`",
        "",
        md_table(full_rows, full_table_cols),
        "## 錯誤輸出",
        "",
        "### 檢測發現與建議",
        "",
        md_table(required_error_rows, ["流程", "問題"]),
        "### 整體錯誤輸出",
        "",
        "無。所有必要流程已完成。" if not failures else "\n".join([f"```text\n{failure}\n```" for failure in failures]),
        "",
        "### 可改進",
        "",
    ]
    for item in improvements:
        report.append(f"1. {item}")
    report.extend(
        [
            "",
            "## 附註",
            "",
            f"- 第一階段完成列數：{len(stage1)}",
            f"- 第二階段完成列數：{len(stage2)}",
            f"- 穩定性檢測完成列數：{len(stability)}",
            f"- 合併結果列數：{len(all_results)}",
        ]
    )
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    errors: list[dict[str, str]] = [{"流程": "環境開始運行", "問題": "核心套件可載入，開始 UMAP + HDBSCAN 多參數搜尋。"}]
    failures: list[str] = []
    improvements = [
        "目前 best balance 使用分群統計選擇，仍建議人工檢查 topic words 與 representative docs，避免低 noise 但語意過寬。",
        "若要讓主題更可解釋，可在 CountVectorizer 加入 domain stopwords，移除 reveal、today、look、vehicle 等過度泛用詞。",
        "若主題仍被大主題吸收，可測試更高 n_components、leaf method 搭配較低 min_samples，或在 BERTopic 後續使用 topic reduction/merge 做人工整理。",
        "短文本少數但存在，後續可比較排除少於 3 或 5 words 的文件對 HDBSCAN 密度估計的影響。",
    ]

    try:
        documents, titles, meta, load_errors = load_documents()
        errors.extend(load_errors)
        if not documents:
            raise RuntimeError("Dataset does not contain usable documents.")
    except Exception:
        failures.append("資料載入失敗。\n" + traceback.format_exc())
        raise

    try:
        embedding_model, embeddings, embedding_errors = get_embeddings(documents)
        errors.extend(embedding_errors)
    except Exception:
        failures.append("Embedding 失敗。\n" + traceback.format_exc())
        raise

    try:
        stage1 = run_search(
            embeddings,
            "stage1",
            stage1_umap_configs(),
            hdbscan_grid(STAGE1_HDBSCAN_GRID),
            STAGE1_CSV,
        )
        errors.append({"流程": "UMAP", "問題": f"第一階段 UMAP grid 完成，組合數：{len(stage1_umap_configs())}。"})
        errors.append({"流程": "HDBSCAN", "問題": f"第一階段 HDBSCAN 完成列數：{len(stage1)}。"})
    except Exception:
        failures.append("第一階段 UMAP/HDBSCAN 搜尋失敗。\n" + traceback.format_exc())
        raise

    top10_umap = choose_top10_umap(stage1)
    top10_umap.to_csv(OUTPUT_DIR / "Result_06.03_A04-3(del)_tok(para12-80)-top10_umap_settings.csv", index=False)
    stage2_umap_configs = [
        {
            "n_neighbors": int(row["umap_n_neighbors"]),
            "n_components": int(row["umap_n_components"]),
            "min_dist": float(row["umap_min_dist"]),
            "random_state": UMAP_RANDOM_STATE,
        }
        for row in top10_umap.to_dict("records")
    ]

    try:
        stage2 = run_search(
            embeddings,
            "stage2",
            stage2_umap_configs,
            hdbscan_grid(STAGE2_HDBSCAN_GRID),
            STAGE2_CSV,
        )
        errors.append({"流程": "HDBSCAN", "問題": f"第二階段深入測試完成列數：{len(stage2)}。"})
    except Exception:
        failures.append("第二階段 HDBSCAN 深入測試失敗。\n" + traceback.format_exc())
        raise

    combined_for_best = pd.concat([stage1, stage2], ignore_index=True)
    best = select_best_rows(combined_for_best)

    stability_targets = []
    if best:
        ranked = combined_for_best[combined_for_best["status"].eq("ok")].sort_values(
            by=["balance_score", "noise_ratio"], ascending=[False, True]
        )
        stability_targets = ranked.head(10).to_dict("records")
    stability_umap_configs: list[dict[str, Any]] = []
    stability_hdbscan_configs: list[dict[str, Any]] = []
    for row in stability_targets:
        for random_state in STABILITY_RANDOM_STATES:
            stability_umap_configs.append(
                {
                    "n_neighbors": int(row["umap_n_neighbors"]),
                    "n_components": int(row["umap_n_components"]),
                    "min_dist": float(row["umap_min_dist"]),
                    "random_state": int(random_state),
                }
            )
            stability_hdbscan_configs.append(
                {
                    "min_cluster_size": int(row["hdbscan_min_cluster_size"]),
                    "min_samples": None
                    if pd.isna(row["hdbscan_min_samples"]) or str(row["hdbscan_min_samples"]) == "None"
                    else int(row["hdbscan_min_samples"]),
                    "cluster_selection_method": str(row["hdbscan_cluster_selection_method"]),
                    "cluster_selection_epsilon": float(row["hdbscan_cluster_selection_epsilon"]),
                }
            )

    try:
        stability_rows = []
        existing = read_existing(STABILITY_CSV)
        done = set(result_key(item) for item in existing.to_dict("records")) if not existing.empty else set()
        for umap_cfg, hdbscan_cfg in zip(stability_umap_configs, stability_hdbscan_configs):
            probe = base_result("stability", umap_cfg, hdbscan_cfg)
            key = result_key(probe)
            if key in done:
                continue
            reduced = get_umap_embeddings(
                embeddings,
                int(umap_cfg["n_neighbors"]),
                int(umap_cfg["n_components"]),
                float(umap_cfg["min_dist"]),
                int(umap_cfg["random_state"]),
            )
            row = run_hdbscan(reduced, umap_cfg, hdbscan_cfg, "stability")
            append_row(STABILITY_CSV, row)
            stability_rows.append(row)
        stability = read_existing(STABILITY_CSV)
        errors.append({"流程": "UMAP", "問題": f"前 10 組參數完成 {len(STABILITY_RANDOM_STATES)} 個 random_state 穩定性檢測。"})
    except Exception:
        failures.append("穩定性檢測失敗。\n" + traceback.format_exc())
        raise

    all_results = pd.concat([stage1, stage2, stability], ignore_index=True)
    all_results.to_csv(ALL_RESULTS_CSV, index=False)

    try:
        chart_paths = make_charts(all_results, best)
        errors.append({"流程": "圖表輸出", "問題": f"已輸出 {len(chart_paths)} 張圖表。"})
    except Exception:
        chart_paths = []
        failures.append("圖表輸出失敗。\n" + traceback.format_exc())
        errors.append({"流程": "圖表輸出", "問題": "圖表輸出失敗，詳見整體錯誤輸出。"})

    final_outputs: list[dict[str, Any]] = []
    try:
        row_ids = meta["row_ids"]
        used_signatures: set[tuple[Any, ...]] = set()
        for label, row in best.items():
            signature = result_key({**row, "stage": "final"})
            final_label = label if signature not in used_signatures else f"{label}_duplicate_config"
            used_signatures.add(signature)
            final_outputs.append(
                train_final_model(final_label, row, documents, titles, row_ids, embedding_model, embeddings)
            )
        errors.append({"流程": "BERTopic", "問題": f"三種最佳設定正式訓練完成，輸出模型組數：{len(final_outputs)}。"})
    except Exception:
        failures.append("最終 BERTopic 訓練失敗。\n" + traceback.format_exc())
        errors.append({"流程": "BERTopic", "問題": "最終 BERTopic 訓練失敗，詳見整體錯誤輸出。"})
        raise
    finally:
        RUN_LOG_JSON.write_text(
            json.dumps(
                {
                    "created_at": now_utc(),
                    "dataset": str(DATASET_DIR.relative_to(ROOT)),
                    "output_dir": str(OUTPUT_DIR.relative_to(ROOT)),
                    "meta": {k: v for k, v in meta.items() if k != "row_ids"},
                    "errors": errors,
                    "failures": failures,
                    "best": best,
                    "final_outputs": final_outputs,
                },
                ensure_ascii=False,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )
        write_report(
            meta,
            errors,
            failures,
            improvements,
            read_existing(STAGE1_CSV),
            top10_umap if "top10_umap" in locals() else pd.DataFrame(),
            read_existing(STAGE2_CSV),
            read_existing(STABILITY_CSV),
            pd.read_csv(ALL_RESULTS_CSV) if ALL_RESULTS_CSV.exists() else pd.DataFrame(),
            best if "best" in locals() else {},
            final_outputs,
            chart_paths if "chart_paths" in locals() else [],
        )


if __name__ == "__main__":
    main()
