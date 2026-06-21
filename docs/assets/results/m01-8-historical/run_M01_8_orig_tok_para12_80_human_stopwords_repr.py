from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import time
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance, PartOfSpeech
from bertopic.representation._base import BaseRepresentation
from datasets import load_from_disk
from hdbscan import HDBSCAN
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from umap import UMAP


ROOT = Path(__file__).resolve().parents[3]
STOPWORD_MD = ROOT / "Result/06.05_A05_stopword/A05-8(orig)REV_tok(para12-80)/A05-8.4(human)_stopword.md"
DATASET_DIR = ROOT / "Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok(para12-80)_dataset"
OUTPUT_DIR = ROOT / "Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)"
A04_EMBEDDINGS = ROOT / "Result/06.03_A04_min-test/A04-8(orig)_tok(para12-80)/embeddings_all-MiniLM-L6-v2.npy"
A04_EMBEDDINGS_META = ROOT / "Result/06.03_A04_min-test/A04-8(orig)_tok(para12-80)/embeddings_all-MiniLM-L6-v2.meta.json"
EMBEDDINGS_PATH = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.npy"
EMBEDDINGS_META = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.meta.json"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TEXT_COL = "sentence"
LLM_MODELS = [
    ("llm_anthropic_claude_opus_4_7", "anthropic/claude-opus-4.7"),
    ("llm_openai_gpt_5_5", "openai/gpt-5.5"),
    ("llm_google_gemini_3_1_pro_preview", "google/gemini-3.1-pro-preview"),
]


CONFIGS = [
    {
        "selection_label": "lowest_noise",
        "report_name": "A06-8-REV_lowest_noise.md",
        "selection_reason": "最低 noise_ratio，並以較低 largest_topic_ratio 與較高 n_clusters 作為 tie-break。",
        "baseline_metrics": {
            "n_clusters": 2,
            "noise_ratio": 0.0055,
            "topic_-1_count": 61,
            "topic_0_count": 272,
            "topic_1_count": 10803,
            "largest_topic_count": 10803,
            "largest_topic_ratio": 0.9701,
            "top3_topic_ratio": 0.9945,
            "topic_entropy": 0.1663,
            "balance_score": 0.3244,
        },
        "umap": {"n_neighbors": 15, "n_components": 10, "min_dist": 0.05, "metric": "cosine", "random_state": 42},
        "hdbscan": {
            "min_cluster_size": 225,
            "min_samples": 5,
            "metric": "euclidean",
            "cluster_selection_method": "eom",
            "cluster_selection_epsilon": 0.0,
        },
    },
    {
        "selection_label": "most_topics",
        "report_name": "A06-8-REV_most_topics.md",
        "selection_reason": "在可接受 noise_ratio 下保留最多有效主題。",
        "baseline_metrics": {
            "n_clusters": 73,
            "noise_ratio": 0.3337,
            "topic_-1_count": 3716,
            "topic_0_count": 52,
            "topic_1_count": 88,
            "largest_topic_count": 318,
            "largest_topic_ratio": 0.0286,
            "top3_topic_ratio": 0.0663,
            "topic_entropy": 0.9742,
            "balance_score": 0.8781,
        },
        "umap": {"n_neighbors": 5, "n_components": 5, "min_dist": 0.0, "metric": "cosine", "random_state": 42},
        "hdbscan": {
            "min_cluster_size": 50,
            "min_samples": 5,
            "metric": "euclidean",
            "cluster_selection_method": "leaf",
            "cluster_selection_epsilon": 0.0,
        },
    },
    {
        "selection_label": "best_balance",
        "report_name": "A06-8-REV_best_balance.md",
        "selection_reason": "符合指定最佳平衡條件後取最高 balance_score。",
        "baseline_metrics": {
            "n_clusters": 62,
            "noise_ratio": 0.2768,
            "topic_-1_count": 3083,
            "topic_0_count": 251,
            "topic_1_count": 52,
            "largest_topic_count": 453,
            "largest_topic_ratio": 0.0407,
            "top3_topic_ratio": 0.1061,
            "topic_entropy": 0.9524,
            "balance_score": 0.8835,
        },
        "umap": {"n_neighbors": 5, "n_components": 5, "min_dist": 0.0, "metric": "cosine", "random_state": 42},
        "hdbscan": {
            "min_cluster_size": 50,
            "min_samples": 5,
            "metric": "euclidean",
            "cluster_selection_method": "eom",
            "cluster_selection_epsilon": 0.2,
        },
    },
]


class OpenRouterLLMRepresentation(BaseRepresentation):
    def __init__(
        self,
        api_key: str,
        model: str = "openai/gpt-4o-mini",
        max_docs: int = 3,
        doc_chars: int = 360,
        delay_seconds: float = 0.15,
    ) -> None:
        self.client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        self.model = model
        self.max_docs = max_docs
        self.doc_chars = doc_chars
        self.delay_seconds = delay_seconds
        self.errors_: list[dict[str, str]] = []
        self.headers = {
            "HTTP-Referer": "https://local.bertopic.a06",
            "X-OpenRouter-Title": "BERTopic A06 Topic Representation",
        }

    def extract_topics(
        self,
        topic_model,
        documents: pd.DataFrame,
        c_tf_idf,
        topics: Mapping[str, list[tuple[str, float]]],
    ) -> Mapping[str, list[tuple[str, float]]]:
        updated_topics: dict[int, list[tuple[str, float]]] = {}
        for topic, words in topics.items():
            topic_id = int(topic)
            keywords = ", ".join(str(word) for word, _ in words[:10])
            docs = (
                documents.loc[documents["Topic"] == topic_id, "Document"]
                .dropna()
                .astype(str)
                .head(self.max_docs)
                .tolist()
            )
            doc_text = "\n".join(f"- {doc[: self.doc_chars]}" for doc in docs)
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You label BERTopic topics for an electric vehicle research corpus. "
                        "Return one concise English topic label, 2 to 6 words. "
                        "Prefer EV meaning when present. Do not explain."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Topic ID: {topic_id}\n"
                        f"Keywords: {keywords}\n"
                        f"Representative snippets:\n{doc_text}\n\n"
                        "Topic label:"
                    ),
                },
            ]
            try:
                if self.delay_seconds:
                    time.sleep(self.delay_seconds)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.0,
                    max_tokens=24,
                    extra_headers=self.headers,
                )
                label = (response.choices[0].message.content or "").strip()
                label = re.sub(r"^(topic label|topic):\s*", "", label, flags=re.I).strip()
                label = label.replace("\n", " ").strip(" .:-")
                if not label:
                    label = f"LLM label unavailable: {keywords}"
            except Exception as exc:
                label = f"LLM fallback: {', '.join(str(word) for word, _ in words[:4])}"
                self.errors_.append(
                    {
                        "topic": str(topic_id),
                        "error": str(exc),
                        "traceback": traceback.format_exc(limit=2),
                    }
                )
            updated_topics[topic_id] = [(label, 1.0)]
        return updated_topics


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        values = []
        for col in columns:
            value = row.get(col, "")
            text = f"{value:.4f}" if isinstance(value, float) else ("" if value is None else str(value))
            values.append(text.replace("\n", "<br>").replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def docs_hash(docs: list[str]) -> str:
    digest = hashlib.sha256()
    digest.update(str(len(docs)).encode("utf-8"))
    for doc in docs[:100]:
        digest.update(doc.encode("utf-8", errors="ignore"))
    for doc in docs[-100:]:
        digest.update(doc.encode("utf-8", errors="ignore"))
    return digest.hexdigest()


def load_documents() -> tuple[list[str], list[str], dict[str, Any]]:
    dataset = load_from_disk(str(DATASET_DIR))
    if TEXT_COL not in dataset.column_names:
        raise ValueError(f"Missing text column: {TEXT_COL}")
    docs: list[str] = []
    titles: list[str] = []
    for item in dataset:
        text = "" if item.get(TEXT_COL) is None else str(item.get(TEXT_COL)).strip()
        if text:
            docs.append(text)
            titles.append(str(item.get("title", "")))
    lengths = [len(doc) for doc in docs]
    word_counts = [len(doc.split()) for doc in docs]
    meta = {
        "dataset": str(DATASET_DIR.relative_to(ROOT)),
        "source_rows": len(dataset),
        "used_rows": len(docs),
        "text_col": TEXT_COL,
        "embedding_model": EMBEDDING_MODEL_NAME,
        "stopword_source": str(STOPWORD_MD.relative_to(ROOT)),
        "min_text_len": min(lengths),
        "max_text_len": max(lengths),
        "avg_text_len": float(np.mean(lengths)),
        "min_word_count": min(word_counts),
        "max_word_count": max(word_counts),
        "avg_word_count": float(np.mean(word_counts)),
    }
    return docs, titles, meta


def extract_recommended_stopwords(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    words: set[str] = set()
    for line in text.splitlines():
        if not line.startswith("| ") or " | " not in line:
            continue
        if line.startswith("| ---") or "停用詞類型" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        for item in cells[2].split(","):
            term = item.strip().lower().strip("`")
            if term:
                words.add(term)
                for token in re.findall(r"(?u)\b\w\w+\b", term):
                    words.add(token.lower())
    match = re.search(
        r"## 建議給 CountVectorizer 的單字停用詞清單.*?```text\n(?P<words>.*?)\n```",
        text,
        flags=re.S,
    )
    if match:
        for line in match.group("words").splitlines():
            word = line.strip().lower()
            if word:
                words.add(word)
    if not words:
        raise ValueError(f"Could not find table stopwords or CountVectorizer stopword block in {path}")
    return sorted(words)


def get_embeddings(docs: list[str]) -> tuple[SentenceTransformer, np.ndarray, str]:
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    current_meta = {"model": EMBEDDING_MODEL_NAME, "doc_count": len(docs), "docs_hash": docs_hash(docs)}
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if EMBEDDINGS_PATH.exists() and EMBEDDINGS_META.exists():
        old_meta = json.loads(EMBEDDINGS_META.read_text(encoding="utf-8"))
        if old_meta == current_meta:
            return model, np.load(EMBEDDINGS_PATH), "使用 M01-8 既有 embeddings 快取。"
    if A04_EMBEDDINGS.exists() and A04_EMBEDDINGS_META.exists():
        old_meta = json.loads(A04_EMBEDDINGS_META.read_text(encoding="utf-8"))
        if old_meta == current_meta:
            shutil.copy2(A04_EMBEDDINGS, EMBEDDINGS_PATH)
            EMBEDDINGS_META.write_text(json.dumps(current_meta, ensure_ascii=False, indent=2), encoding="utf-8")
            return model, np.load(EMBEDDINGS_PATH), "重用 A04-8(orig) embeddings 快取並複製到 M01-8。"
    embeddings = model.encode(docs, show_progress_bar=True, batch_size=64, convert_to_numpy=True)
    np.save(EMBEDDINGS_PATH, embeddings)
    EMBEDDINGS_META.write_text(json.dumps(current_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return model, embeddings, "重新計算 embeddings 並建立 M01-8 快取。"


def label_metrics(labels: list[int] | np.ndarray) -> dict[str, Any]:
    counts = Counter(int(label) for label in labels)
    total = int(sum(counts.values()))
    cluster_counts = [count for topic, count in counts.items() if topic != -1]
    sorted_counts = sorted(cluster_counts, reverse=True)
    n_clusters = len(cluster_counts)
    largest = int(sorted_counts[0]) if sorted_counts else 0
    top3 = int(sum(sorted_counts[:3])) if sorted_counts else 0
    if n_clusters <= 1 or not cluster_counts:
        entropy = 0.0
    else:
        probs = np.array(cluster_counts, dtype=float) / sum(cluster_counts)
        entropy = float(-(probs * np.log(probs)).sum() / math.log(n_clusters))
    noise_ratio = counts.get(-1, 0) / total if total else 0.0
    largest_ratio = largest / total if total else 0.0
    top3_ratio = top3 / total if total else 0.0
    balance_score = (
        0.30 * (1.0 - noise_ratio)
        + 0.30 * (1.0 - largest_ratio)
        + 0.20 * (1.0 - top3_ratio)
        + 0.20 * min(n_clusters / 25.0, 1.0)
    )
    return {
        "n_clusters": int(n_clusters),
        "noise_ratio": float(noise_ratio),
        "topic_-1_count": int(counts.get(-1, 0)),
        "topic_0_count": int(counts.get(0, 0)),
        "topic_1_count": int(counts.get(1, 0)),
        "largest_topic_count": largest,
        "largest_topic_ratio": float(largest_ratio),
        "top3_topic_ratio": float(top3_ratio),
        "topic_entropy": entropy,
        "balance_score": float(balance_score),
    }


def topic_words_df(topic_model: BERTopic, info: pd.DataFrame, representation_name: str) -> pd.DataFrame:
    rows = []
    for topic in info["Topic"].tolist():
        words = topic_model.get_topic(int(topic)) or []
        clean_words = [(str(word), float(weight)) for word, weight in words]
        rows.append(
            {
                "representation_model": representation_name,
                "topic": int(topic),
                "words": ", ".join(word for word, _ in clean_words),
                "weighted_words": json.dumps(clean_words, ensure_ascii=False),
            }
        )
    return pd.DataFrame(rows)


def representative_docs_df(topic_model: BERTopic, info: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for topic in info["Topic"].tolist():
        reps = topic_model.get_representative_docs(int(topic)) or []
        for rank, rep in enumerate(reps[:5], start=1):
            rows.append({"topic": int(topic), "rank": rank, "representative_text": rep})
    return pd.DataFrame(rows)


def stopword_hit_summary(topic_words: pd.DataFrame, custom_stopwords: list[str]) -> dict[str, Any]:
    stopword_set = set(custom_stopwords)
    rows = []
    for _, row in topic_words.iterrows():
        words = [word.strip().lower() for word in str(row.get("words", "")).split(",") if word.strip()]
        hits = [word for word in words if word in stopword_set]
        if hits:
            rows.append({"topic": int(row["topic"]), "hits": ", ".join(hits), "hit_count": len(hits)})
    return {"topics_with_custom_stopword_hits": len(rows), "custom_stopword_hits": rows}


def filter_topic_representations(topic_model: BERTopic, custom_stopwords: list[str]) -> None:
    stopword_set = set(custom_stopwords)
    for topic, words in list(topic_model.topic_representations_.items()):
        filtered = []
        for word, weight in words:
            if str(word).strip().lower() in stopword_set:
                continue
            filtered.append((str(word), float(weight)))
        if not filtered:
            filtered = [("filtered_topic_terms_unavailable", 0.0)]
        topic_model.topic_representations_[topic] = filtered


def export_representation(
    topic_model: BERTopic,
    docs: list[str],
    topics: list[int],
    out_dir: Path,
    name: str,
    representation_model: Any | None,
    custom_stopwords: list[str],
    errors: list[dict[str, str]],
) -> dict[str, Any]:
    try:
        if representation_model is not None:
            topic_model.update_topics(docs, topics=topics, representation_model=representation_model, top_n_words=10)
        filter_topic_representations(topic_model, custom_stopwords)
        info = topic_model.get_topic_info()
        words = topic_words_df(topic_model, info, name)
        info.to_csv(out_dir / f"topic_info_{name}.csv", index=False)
        words.to_csv(out_dir / f"topic_words_{name}.csv", index=False)
        if name == "default":
            info.to_csv(out_dir / "topic_info.csv", index=False)
            words.to_csv(out_dir / "topic_words.csv", index=False)
        hit_summary = stopword_hit_summary(words, custom_stopwords)
        return {
            "status": "ok",
            "info": info,
            "words": words,
            "topics_with_custom_stopword_hits": hit_summary["topics_with_custom_stopword_hits"],
            "custom_stopword_hits": hit_summary["custom_stopword_hits"],
        }
    except Exception as exc:
        errors.append({"representation_model": name, "error": str(exc), "traceback": traceback.format_exc()})
        return {"status": "failed", "info": None, "words": None, "topics_with_custom_stopword_hits": None}


def build_llm_representations(errors: list[dict[str, str]]) -> dict[str, OpenRouterLLMRepresentation | None]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        for name, model in LLM_MODELS:
            errors.append({"representation_model": name, "model": model, "error": "OPENROUTER_API_KEY was not provided."})
        return {name: None for name, _ in LLM_MODELS}
    return {
        name: OpenRouterLLMRepresentation(
            api_key=api_key,
            model=model,
            max_docs=3,
            doc_chars=360,
            delay_seconds=float(os.getenv("OPENROUTER_DELAY_SECONDS", "0.15")),
        )
        for name, model in LLM_MODELS
    }


def info_preview_rows(info: pd.DataFrame, n: int = 20) -> tuple[list[dict[str, Any]], list[str]]:
    preferred = ["Topic", "Count", "Name", "Representation"]
    columns = [col for col in preferred if col in info.columns]
    return info.head(n)[columns].to_dict("records"), columns


def write_report(
    config: dict[str, Any],
    meta: dict[str, Any],
    embedding_note: str,
    custom_stopwords: list[str],
    metrics: dict[str, Any],
    representation_outputs: dict[str, dict[str, Any]],
    csv_paths: dict[str, str],
    errors: list[dict[str, str]],
    started_at: str,
    finished_at: str,
) -> None:
    label = config["selection_label"]
    baseline = config["baseline_metrics"]
    comparison = {
        "selection_label": label,
        "baseline_noise_ratio": baseline["noise_ratio"],
        "a06_noise_ratio": metrics["noise_ratio"],
        "baseline_n_clusters": baseline["n_clusters"],
        "a06_n_clusters": metrics["n_clusters"],
        "baseline_largest_topic_ratio": baseline["largest_topic_ratio"],
        "a06_largest_topic_ratio": metrics["largest_topic_ratio"],
        "baseline_top3_topic_ratio": baseline["top3_topic_ratio"],
        "a06_top3_topic_ratio": metrics["top3_topic_ratio"],
        "baseline_balance_score": baseline["balance_score"],
        "a06_balance_score": metrics["balance_score"],
    }
    parameter_row = {
        "selection_label": label,
        "selection_reason": config["selection_reason"],
        "umap_n_neighbors": config["umap"]["n_neighbors"],
        "umap_n_components": config["umap"]["n_components"],
        "umap_min_dist": config["umap"]["min_dist"],
        "umap_metric": config["umap"]["metric"],
        "umap_random_state": config["umap"]["random_state"],
        "hdbscan_min_cluster_size": config["hdbscan"]["min_cluster_size"],
        "hdbscan_min_samples": config["hdbscan"]["min_samples"],
        "hdbscan_cluster_selection_method": config["hdbscan"]["cluster_selection_method"],
        "hdbscan_cluster_selection_epsilon": config["hdbscan"]["cluster_selection_epsilon"],
        "hdbscan_metric": config["hdbscan"]["metric"],
    }
    run_row = {
        "started_at": started_at,
        "finished_at": finished_at,
        "dataset": meta["dataset"],
        "embedding_model": EMBEDDING_MODEL_NAME,
        "embedding_note": embedding_note,
        "custom_stopword_count": len(custom_stopwords),
        "llm_provider": "OpenRouter",
        "llm_models": ", ".join(model for _, model in LLM_MODELS),
    }
    report = [
        f"# A06-8-REV BERTopic + A05-8.4(human) stopwords + representation models - {label}",
        "",
        "## Run Info",
        "",
        md_table([run_row], list(run_row.keys())),
        "",
        "## Parameters",
        "",
        md_table([parameter_row], list(parameter_row.keys())),
        "",
        "## Metrics",
        "",
        md_table([{**metrics}], list(metrics.keys())),
        "",
        "## Compared With Provided Baseline",
        "",
        md_table([comparison], list(comparison.keys())),
        "",
        "## Stopword Setting",
        "",
        f"- stopword source: `{STOPWORD_MD.relative_to(ROOT)}`",
        "- 使用 A05-8.4(human) 報告表格第三欄建議停用詞，並加上 sklearn English stop words。",
        "- stopwords 只作用於 BERTopic c-TF-IDF / topic words 表示；embedding 與 HDBSCAN 分群仍使用原始 orig 文本向量。",
        "",
        "## Representation Models",
        "",
        "- default: BERTopic c-TF-IDF",
        "- keybert: KeyBERT-Inspired",
        "- pos: Part-of-Speech",
        "- mmr: Maximal Marginal Relevance",
        "- llm_anthropic_claude_opus_4_7: OpenRouter LLM topic labels",
        "- llm_openai_gpt_5_5: OpenRouter LLM topic labels",
        "- llm_google_gemini_3_1_pro_preview: OpenRouter LLM topic labels",
        "",
    ]
    for name, payload in representation_outputs.items():
        status = payload.get("status", "unknown")
        report.extend([f"### {name}", "", f"- status: `{status}`"])
        if payload.get("topics_with_custom_stopword_hits") is not None:
            report.append(f"- topics_with_custom_stopword_hits: {payload['topics_with_custom_stopword_hits']}")
        info = payload.get("info")
        words = payload.get("words")
        if isinstance(info, pd.DataFrame) and isinstance(words, pd.DataFrame):
            rows, columns = info_preview_rows(info, 20)
            report.extend(
                [
                    "",
                    "#### Topic Info Top 20",
                    "",
                    md_table(rows, columns),
                    "",
                    "#### Topic Words Top 20",
                    "",
                    md_table(words.head(20).to_dict("records"), ["topic", "words"]),
                ]
            )
    report.extend(
        [
            "",
            "## Output Files",
            "",
            md_table([csv_paths], list(csv_paths.keys())),
            "",
            "## Representation Errors",
            "",
            "無" if not errors else "```json\n" + json.dumps(errors, ensure_ascii=False, indent=2) + "\n```",
            "",
            "## Notes",
            "",
            "KeyBERT-Inspired、POS、MMR 與 LLM 只更新 topic representation，不改變 UMAP/HDBSCAN topic labels，因此三者的 clustering metrics 會相同。",
            "",
        ]
    )
    (OUTPUT_DIR / config["report_name"]).write_text("\n".join(report), encoding="utf-8")


def run_one(
    config: dict[str, Any],
    docs: list[str],
    titles: list[str],
    embedding_model: SentenceTransformer,
    embeddings: np.ndarray,
    vectorizer_model: CountVectorizer,
    custom_stopwords: list[str],
    meta: dict[str, Any],
    embedding_note: str,
    llm_representations: dict[str, OpenRouterLLMRepresentation | None],
) -> dict[str, Any]:
    started_at = datetime.now(timezone.utc).isoformat()
    label = config["selection_label"]
    out_dir = OUTPUT_DIR / label
    out_dir.mkdir(parents=True, exist_ok=True)
    umap_conf = config["umap"]
    hdbscan_conf = config["hdbscan"]
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=UMAP(
            n_neighbors=umap_conf["n_neighbors"],
            n_components=umap_conf["n_components"],
            min_dist=umap_conf["min_dist"],
            metric=umap_conf["metric"],
            random_state=umap_conf["random_state"],
            low_memory=True,
        ),
        hdbscan_model=HDBSCAN(
            min_cluster_size=hdbscan_conf["min_cluster_size"],
            min_samples=hdbscan_conf["min_samples"],
            metric=hdbscan_conf["metric"],
            cluster_selection_method=hdbscan_conf["cluster_selection_method"],
            cluster_selection_epsilon=hdbscan_conf["cluster_selection_epsilon"],
            prediction_data=True,
            core_dist_n_jobs=-1,
        ),
        vectorizer_model=vectorizer_model,
        top_n_words=10,
        calculate_probabilities=False,
        verbose=False,
    )
    topics, _ = topic_model.fit_transform(docs, embeddings)
    topics = [int(topic) for topic in topics]
    metrics = label_metrics(topics)
    pd.DataFrame({"title": titles, "sentence": docs, "topic": topics}).to_csv(out_dir / "document_topics.csv", index=False)
    base_info = topic_model.get_topic_info()
    representative_docs_df(topic_model, base_info).to_csv(out_dir / "representative_docs.csv", index=False)
    topic_size = base_info[["Topic", "Count", "Name"]].copy()
    topic_size["ratio"] = topic_size["Count"] / len(docs)
    topic_size.to_csv(out_dir / "topic_size_distribution.csv", index=False)

    errors: list[dict[str, str]] = []
    representations: dict[str, Any | None] = {
        "default": None,
        "keybert": KeyBERTInspired(top_n_words=10, random_state=42),
        "pos": PartOfSpeech("en_core_web_sm", top_n_words=10),
        "mmr": MaximalMarginalRelevance(diversity=0.35, top_n_words=10),
    }
    representations.update(llm_representations)
    representation_outputs: dict[str, dict[str, Any]] = {}
    for name, representation_model in representations.items():
        if name.startswith("llm_") and representation_model is None:
            representation_outputs[name] = {"status": "skipped", "info": None, "words": None}
            errors.append({"representation_model": name, "error": "OPENROUTER_API_KEY was not provided."})
            continue
        print(f"  representation: {name}", flush=True)
        representation_outputs[name] = export_representation(
            topic_model,
            docs,
            topics,
            out_dir,
            name,
            representation_model,
            custom_stopwords,
            errors,
        )
        if name.startswith("llm_") and isinstance(representation_model, OpenRouterLLMRepresentation):
            for item in representation_model.errors_:
                errors.append({"representation_model": name, "model": representation_model.model, **item})

    (out_dir / "representation_errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
    config_record = {
        **config,
        "a06_metrics": metrics,
        "dataset": str(DATASET_DIR.relative_to(ROOT)),
        "embedding_model": EMBEDDING_MODEL_NAME,
        "custom_stopwords_count": len(custom_stopwords),
        "stopword_source": str(STOPWORD_MD.relative_to(ROOT)),
        "representation_models": list(representations.keys()),
        "llm_provider": "OpenRouter",
        "llm_models": [model for _, model in LLM_MODELS],
    }
    (out_dir / "final_config.json").write_text(json.dumps(config_record, ensure_ascii=False, indent=2), encoding="utf-8")
    csv_paths = {
        "topic_info_default": str((out_dir / "topic_info_default.csv").relative_to(OUTPUT_DIR)),
        "topic_words_default": str((out_dir / "topic_words_default.csv").relative_to(OUTPUT_DIR)),
        "topic_info_keybert": str((out_dir / "topic_info_keybert.csv").relative_to(OUTPUT_DIR)),
        "topic_words_keybert": str((out_dir / "topic_words_keybert.csv").relative_to(OUTPUT_DIR)),
        "topic_info_pos": str((out_dir / "topic_info_pos.csv").relative_to(OUTPUT_DIR)),
        "topic_words_pos": str((out_dir / "topic_words_pos.csv").relative_to(OUTPUT_DIR)),
        "topic_info_mmr": str((out_dir / "topic_info_mmr.csv").relative_to(OUTPUT_DIR)),
        "topic_words_mmr": str((out_dir / "topic_words_mmr.csv").relative_to(OUTPUT_DIR)),
        "document_topics": str((out_dir / "document_topics.csv").relative_to(OUTPUT_DIR)),
        "representative_docs": str((out_dir / "representative_docs.csv").relative_to(OUTPUT_DIR)),
        "topic_size_distribution": str((out_dir / "topic_size_distribution.csv").relative_to(OUTPUT_DIR)),
        "final_config": str((out_dir / "final_config.json").relative_to(OUTPUT_DIR)),
        "representation_errors": str((out_dir / "representation_errors.json").relative_to(OUTPUT_DIR)),
    }
    for name, _ in LLM_MODELS:
        csv_paths[f"topic_info_{name}"] = str((out_dir / f"topic_info_{name}.csv").relative_to(OUTPUT_DIR))
        csv_paths[f"topic_words_{name}"] = str((out_dir / f"topic_words_{name}.csv").relative_to(OUTPUT_DIR))
    write_report(
        config,
        meta,
        embedding_note,
        custom_stopwords,
        metrics,
        representation_outputs,
        csv_paths,
        errors,
        started_at,
        datetime.now(timezone.utc).isoformat(),
    )
    return {
        "selection_label": label,
        "report": config["report_name"],
        **metrics,
        "representation_errors": len(errors),
        "llm_topic_label_errors": sum(
            len(rep.errors_) for rep in llm_representations.values() if isinstance(rep, OpenRouterLLMRepresentation)
        ),
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    docs, titles, meta = load_documents()
    custom_stopwords = extract_recommended_stopwords(STOPWORD_MD)
    stopwords = sorted(set(ENGLISH_STOP_WORDS).union(custom_stopwords))
    (OUTPUT_DIR / "M01-8_custom_stopwords_used.txt").write_text("\n".join(custom_stopwords) + "\n", encoding="utf-8")
    embedding_model, embeddings, embedding_note = get_embeddings(docs)
    vectorizer_model = CountVectorizer(stop_words=stopwords, ngram_range=(1, 2), min_df=2)
    global_errors: list[dict[str, str]] = []
    summaries = []
    for config in CONFIGS:
        print(f"Training {config['selection_label']}...", flush=True)
        llm_representations = build_llm_representations(global_errors)
        summaries.append(
            run_one(
                config,
                docs,
                titles,
                embedding_model,
                embeddings,
                vectorizer_model,
                custom_stopwords,
                meta,
                embedding_note,
                llm_representations,
            )
        )
    pd.DataFrame(summaries).to_csv(OUTPUT_DIR / "M01-8_comparison_summary.csv", index=False)
    (OUTPUT_DIR / "M01-8_run_summary.json").write_text(json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "M01-8_run_log.json").write_text(
        json.dumps(
            {
                "finished_at": datetime.now(timezone.utc).isoformat(),
                "dataset": str(DATASET_DIR.relative_to(ROOT)),
                "output_dir": str(OUTPUT_DIR.relative_to(ROOT)),
                "stopword_md": str(STOPWORD_MD.relative_to(ROOT)),
                "custom_stopword_count": len(custom_stopwords),
                "total_stopword_count_with_english": len(stopwords),
                "embedding_note": embedding_note,
                "rows": len(docs),
                "configs": [config["selection_label"] for config in CONFIGS],
                "representation_models": ["default", "keybert", "pos", "mmr", *[name for name, _ in LLM_MODELS]],
                "llm_provider": "OpenRouter",
                "llm_models": [model for _, model in LLM_MODELS],
                "global_errors": global_errors,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
