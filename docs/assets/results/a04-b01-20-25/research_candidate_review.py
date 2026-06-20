from __future__ import annotations

import importlib.util
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from bertopic import BERTopic
from bertopic.dimensionality import BaseDimensionalityReduction
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / "Result/06.13_[D]UMAP/[B]01-(orig)_20-25_tok(para12-80)"
RUN_SCRIPT = OUTPUT_DIR / "run_06_13_DUMAP_B01_orig_20_25_tok_para12_80.py"
REVIEW_DIR = OUTPUT_DIR / "research_review"
STAGE2_CSV = OUTPUT_DIR / "stage2_results.csv"


CANDIDATES = [
    {
        "label": "macro_15_high_entropy",
        "reason": "最少主題的宏觀版本之一，topic_entropy 高，適合檢查是否形成較粗的 framing 類別。",
        "umap_n_neighbors": 5,
        "umap_n_components": 10,
        "umap_min_dist": 0.0,
        "hdbscan_min_cluster_size": 225,
        "hdbscan_min_samples": 10,
        "hdbscan_cluster_selection_method": "eom",
        "hdbscan_cluster_selection_epsilon": 0.0,
    },
    {
        "label": "macro_16_less_noise",
        "reason": "比 macro_15 保留略多主題且 noise 稍低，用來檢查宏觀 framing 與資料覆蓋率的折衷。",
        "umap_n_neighbors": 5,
        "umap_n_components": 10,
        "umap_min_dist": 0.0,
        "hdbscan_min_cluster_size": 200,
        "hdbscan_min_samples": 10,
        "hdbscan_cluster_selection_method": "eom",
        "hdbscan_cluster_selection_epsilon": 0.0,
    },
    {
        "label": "mid_22_research",
        "reason": "研究導向分數高，約 22 個主題，平均主題大小較適合人工命名與 framing coding。",
        "umap_n_neighbors": 10,
        "umap_n_components": 5,
        "umap_min_dist": 0.0,
        "hdbscan_min_cluster_size": 125,
        "hdbscan_min_samples": 5,
        "hdbscan_cluster_selection_method": "eom",
        "hdbscan_cluster_selection_epsilon": 0.0,
    },
    {
        "label": "mid_25_research_top",
        "reason": "本次自訂研究分數最高，約 25 個主題，避免 59/70 topics 的過度碎裂。",
        "umap_n_neighbors": 15,
        "umap_n_components": 10,
        "umap_min_dist": 0.0,
        "hdbscan_min_cluster_size": 100,
        "hdbscan_min_samples": 5,
        "hdbscan_cluster_selection_method": "eom",
        "hdbscan_cluster_selection_epsilon": 0.2,
    },
    {
        "label": "mid_30_context",
        "reason": "主題數約 30，noise 較 mid_25 低，適合保留較多產品敘事細節。",
        "umap_n_neighbors": 15,
        "umap_n_components": 10,
        "umap_min_dist": 0.0,
        "hdbscan_min_cluster_size": 75,
        "hdbscan_min_samples": 5,
        "hdbscan_cluster_selection_method": "eom",
        "hdbscan_cluster_selection_epsilon": 0.2,
    },
    {
        "label": "feature_31_lower_noise",
        "reason": "中等主題數中 noise 較低的版本，適合比較是否開始變成產品功能分類。",
        "umap_n_neighbors": 5,
        "umap_n_components": 10,
        "umap_min_dist": 0.0,
        "hdbscan_min_cluster_size": 100,
        "hdbscan_min_samples": 5,
        "hdbscan_cluster_selection_method": "eom",
        "hdbscan_cluster_selection_epsilon": 0.0,
    },
]


FRAME_TERMS = {
    "sustainability",
    "sustainable",
    "environment",
    "emissions",
    "zero",
    "future",
    "innovation",
    "technology",
    "connected",
    "digital",
    "mobility",
    "safety",
    "confidence",
    "performance",
    "power",
    "efficiency",
    "efficient",
    "design",
    "luxury",
    "premium",
    "comfort",
    "experience",
    "customer",
    "customers",
    "freedom",
    "adventure",
    "lifestyle",
    "electric",
    "electrified",
    "electrification",
    "charging",
    "range",
    "battery",
    "hybrid",
}

FEATURE_TERMS = {
    "seat",
    "seats",
    "rear",
    "grille",
    "led",
    "wheel",
    "wheels",
    "inch",
    "alloy",
    "screen",
    "display",
    "camera",
    "monitor",
    "key",
    "sound",
    "cargo",
    "trunk",
    "leather",
    "horsepower",
    "torque",
    "engine",
    "motor",
    "warranty",
    "carplay",
    "android",
}


def load_run_module():
    spec = importlib.util.spec_from_file_location("d_umap_run", RUN_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_terms(path: Path) -> set[str]:
    if not path.exists():
        return set()
    terms = set()
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        text = line.strip().lower()
        if text and not text.startswith("#"):
            terms.add(text)
    return terms


def label_metrics(labels: np.ndarray) -> dict[str, Any]:
    counts = Counter(int(label) for label in labels)
    total = len(labels)
    cluster_counts = sorted([count for topic, count in counts.items() if topic != -1], reverse=True)
    n_clusters = len(cluster_counts)
    largest = cluster_counts[0] if cluster_counts else 0
    top3 = sum(cluster_counts[:3])
    if n_clusters <= 1 or sum(cluster_counts) == 0:
        entropy = 0.0
    else:
        probs = np.array(cluster_counts, dtype=float) / float(sum(cluster_counts))
        entropy = float(-(probs * np.log(probs)).sum() / math.log(n_clusters))
    return {
        "n_clusters": n_clusters,
        "noise_ratio": counts.get(-1, 0) / total,
        "topic_-1_count": counts.get(-1, 0),
        "largest_topic_count": largest,
        "largest_topic_ratio": largest / total,
        "top3_topic_ratio": top3 / total,
        "topic_entropy": entropy,
        "mean_non_noise_topic_size": (total - counts.get(-1, 0)) / n_clusters if n_clusters else 0.0,
    }


def word_metrics(topic_words: pd.DataFrame, brand_model_terms: set[str]) -> dict[str, Any]:
    rows = []
    for _, row in topic_words.iterrows():
        words = [part.strip().lower() for part in str(row.get("words", "")).split(",") if part.strip()]
        if int(row["topic"]) == -1:
            continue
        brand_hits = [word for word in words if word in brand_model_terms]
        frame_hits = [word for word in words if word in FRAME_TERMS]
        feature_hits = [word for word in words if word in FEATURE_TERMS]
        rows.append(
            {
                "topic": int(row["topic"]),
                "top_word_count": len(words),
                "brand_model_hit_count": len(brand_hits),
                "frame_hit_count": len(frame_hits),
                "feature_hit_count": len(feature_hits),
                "brand_model_hit_ratio": len(brand_hits) / len(words) if words else 0.0,
                "frame_hit_ratio": len(frame_hits) / len(words) if words else 0.0,
                "feature_hit_ratio": len(feature_hits) / len(words) if words else 0.0,
                "words": ", ".join(words),
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return {
            "topics_checked": 0,
            "topics_with_brand_model_hits": 0,
            "mean_brand_model_hit_ratio": 0.0,
            "mean_frame_hit_ratio": 0.0,
            "mean_feature_hit_ratio": 0.0,
        }
    return {
        "topics_checked": int(len(out)),
        "topics_with_brand_model_hits": int((out["brand_model_hit_count"] > 0).sum()),
        "mean_brand_model_hit_ratio": float(out["brand_model_hit_ratio"].mean()),
        "mean_frame_hit_ratio": float(out["frame_hit_ratio"].mean()),
        "mean_feature_hit_ratio": float(out["feature_hit_ratio"].mean()),
    }


def md_table(df: pd.DataFrame, columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in df.iterrows():
        vals = []
        for col in columns:
            value = row.get(col, "")
            if isinstance(value, float):
                text = f"{value:.4f}"
            else:
                text = "" if pd.isna(value) else str(value)
            vals.append(text.replace("|", "\\|").replace("\n", "<br>"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    run_mod = load_run_module()
    docs, titles, doc_meta, meta, _ = run_mod.load_documents()
    embeddings = np.load(OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.npy")
    stage2 = pd.read_csv(STAGE2_CSV)
    brand_model_terms = load_terms(ROOT / "brands.txt") | load_terms(ROOT / "models.txt")

    summaries = []
    topic_word_summaries = []
    for conf in CANDIDATES:
        out = REVIEW_DIR / conf["label"]
        out.mkdir(parents=True, exist_ok=True)
        key_mask = (
            stage2["umap_n_neighbors"].eq(conf["umap_n_neighbors"])
            & stage2["umap_n_components"].eq(conf["umap_n_components"])
            & stage2["umap_min_dist"].eq(conf["umap_min_dist"])
            & stage2["hdbscan_min_cluster_size"].eq(conf["hdbscan_min_cluster_size"])
            & stage2["hdbscan_cluster_selection_method"].eq(conf["hdbscan_cluster_selection_method"])
            & stage2["hdbscan_cluster_selection_epsilon"].eq(conf["hdbscan_cluster_selection_epsilon"])
        )
        ms = conf["hdbscan_min_samples"]
        key_mask &= stage2["hdbscan_min_samples"].isna() if ms is None else stage2["hdbscan_min_samples"].eq(ms)
        stage_row = stage2[key_mask].head(1)
        reduced = run_mod.get_umap_embeddings(
            embeddings,
            conf["umap_n_neighbors"],
            conf["umap_n_components"],
            conf["umap_min_dist"],
            42,
        )
        topic_model = BERTopic(
            embedding_model=None,
            umap_model=BaseDimensionalityReduction(),
            hdbscan_model=HDBSCAN(
                min_cluster_size=conf["hdbscan_min_cluster_size"],
                min_samples=conf["hdbscan_min_samples"],
                metric="euclidean",
                cluster_selection_method=conf["hdbscan_cluster_selection_method"],
                cluster_selection_epsilon=conf["hdbscan_cluster_selection_epsilon"],
                prediction_data=True,
                core_dist_n_jobs=-1,
            ),
            vectorizer_model=CountVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2),
            top_n_words=10,
            calculate_probabilities=False,
            verbose=False,
        )
        topics, _ = topic_model.fit_transform(docs, reduced)
        info = topic_model.get_topic_info()
        info.to_csv(out / "topic_info.csv", index=False)

        doc_topics = doc_meta.copy()
        doc_topics["topic"] = [int(topic) for topic in topics]
        doc_topics.to_csv(out / "document_topics.csv", index=False)

        topic_words = []
        representative_docs = []
        for topic in info["Topic"].tolist():
            words = topic_model.get_topic(int(topic)) or []
            topic_words.append(
                {
                    "topic": int(topic),
                    "count": int(info.loc[info["Topic"].eq(topic), "Count"].iloc[0]),
                    "words": ", ".join([word for word, _ in words]),
                    "weighted_words": json.dumps(words, ensure_ascii=False),
                }
            )
            for rank, text in enumerate((topic_model.get_representative_docs(int(topic)) or [])[:5], start=1):
                representative_docs.append({"topic": int(topic), "rank": rank, "representative_text": text})
        topic_words_df = pd.DataFrame(topic_words)
        topic_words_df.to_csv(out / "topic_words.csv", index=False)
        pd.DataFrame(representative_docs).to_csv(out / "representative_docs.csv", index=False)

        per_topic_word_metrics = []
        for _, row in topic_words_df.iterrows():
            words = [part.strip().lower() for part in str(row.get("words", "")).split(",") if part.strip()]
            brand_hits = [word for word in words if word in brand_model_terms]
            frame_hits = [word for word in words if word in FRAME_TERMS]
            feature_hits = [word for word in words if word in FEATURE_TERMS]
            per_topic_word_metrics.append(
                {
                    "label": conf["label"],
                    "topic": int(row["topic"]),
                    "count": int(row["count"]),
                    "brand_model_hits": ", ".join(brand_hits),
                    "frame_hits": ", ".join(frame_hits),
                    "feature_hits": ", ".join(feature_hits),
                    "words": row["words"],
                }
            )
        pd.DataFrame(per_topic_word_metrics).to_csv(out / "topic_word_diagnostics.csv", index=False)
        topic_word_summaries.extend(per_topic_word_metrics)

        metrics = label_metrics(np.array(topics, dtype=int))
        wm = word_metrics(topic_words_df, brand_model_terms)
        stage_metrics = stage_row.iloc[0].to_dict() if not stage_row.empty else {}
        summary = {
            "label": conf["label"],
            "reason": conf["reason"],
            **{k: conf[k] for k in conf if k not in {"label", "reason"}},
            **metrics,
            **wm,
            "stage2_balance_score": stage_metrics.get("balance_score", np.nan),
            "topic_info_rows": int(len(info)),
        }
        # Heuristic: prefer 18-30 topics, manageable noise, low brand/model absorption,
        # and enough frame/value proposition terms for qualitative coding.
        topic_score = 1.0 - min(abs(summary["n_clusters"] - 24) / 24, 1.0)
        noise_score = 1.0 - min(abs(summary["noise_ratio"] - 0.28) / 0.28, 1.0)
        size_score = 1.0 - min(abs(summary["mean_non_noise_topic_size"] - 320) / 320, 1.0)
        brand_penalty = min(summary["mean_brand_model_hit_ratio"] / 0.20, 1.0)
        frame_score = min(summary["mean_frame_hit_ratio"] / 0.22, 1.0)
        summary["research_fit_score"] = (
            0.28 * topic_score
            + 0.22 * noise_score
            + 0.16 * size_score
            + 0.14 * summary["topic_entropy"]
            + 0.12 * frame_score
            + 0.08 * (1.0 - brand_penalty)
        )
        summaries.append(summary)

    summary_df = pd.DataFrame(summaries).sort_values("research_fit_score", ascending=False)
    summary_df.to_csv(REVIEW_DIR / "candidate_summary.csv", index=False)
    pd.DataFrame(topic_word_summaries).to_csv(REVIEW_DIR / "all_topic_word_diagnostics.csv", index=False)

    report = [
        "# Research-Oriented BERTopic Candidate Review",
        "",
        "這份補充檢查不是用最低 noise、最多 topic 或最高 balance_score 選模型，而是用 EV manufacturer framing 研究可解釋性來看：主題數不能太少也不能太碎，noise 可以接受但不能犧牲全部資料，並檢查 topic words 是否過度被品牌/車款吸走。",
        "",
        "## Candidate Summary",
        "",
        md_table(
            summary_df,
            [
                "label",
                "n_clusters",
                "noise_ratio",
                "largest_topic_ratio",
                "top3_topic_ratio",
                "topic_entropy",
                "mean_non_noise_topic_size",
                "topics_with_brand_model_hits",
                "mean_brand_model_hit_ratio",
                "mean_frame_hit_ratio",
                "mean_feature_hit_ratio",
                "research_fit_score",
                "reason",
            ],
        ),
        "## Top Topic Words By Candidate",
        "",
    ]
    for _, summary in summary_df.iterrows():
        label = summary["label"]
        tw = pd.read_csv(REVIEW_DIR / label / "topic_words.csv")
        head = tw[tw["topic"].ne(-1)].head(12)[["topic", "count", "words"]]
        report.extend([f"### {label}", "", md_table(head, ["topic", "count", "words"]), ""])
    (REVIEW_DIR / "research_candidate_review.md").write_text("\n".join(report), encoding="utf-8")


if __name__ == "__main__":
    main()
