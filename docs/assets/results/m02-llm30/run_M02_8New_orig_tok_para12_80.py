from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
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
OUTPUT_DIR = ROOT / "Result/.m06.05_Main02-single/M02-8New(orig)_tok(para12-80)"
A04_EMBEDDINGS = ROOT / "Result/06.03_A04_min-test/A04-8(orig)_tok(para12-80)/embeddings_all-MiniLM-L6-v2.npy"
A04_EMBEDDINGS_META = ROOT / "Result/06.03_A04_min-test/A04-8(orig)_tok(para12-80)/embeddings_all-MiniLM-L6-v2.meta.json"
EMBEDDINGS_PATH = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.npy"
EMBEDDINGS_META = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.meta.json"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TEXT_COL = "sentence"
LLM_MODEL_KEY = "llm_openai_gpt_5_5"
LLM_MODEL_NAME = "openai/gpt-5.5"
LLM_MODELS = [(LLM_MODEL_KEY, LLM_MODEL_NAME)]
LLM30_RUNS = 30
REPRESENTATIVE_DOCS_PER_TOPIC = 6
OPENROUTER_PREFLIGHT_ERROR = ""


CONFIGS = [
    {
        "selection_label": "M02-8New",
        "report_name": "M02-8New-set.md",
        "selection_reason": "使用者指定單組參數，並以 BERTopic nr_topics='auto' 做 c-TF-IDF topic reduction。",
        "umap": {"n_neighbors": 10, "n_components": 15, "min_dist": 0.0, "metric": "cosine", "random_state": 42},
        "hdbscan": {
            "min_cluster_size": 50,
            "min_samples": 5,
            "metric": "euclidean",
            "cluster_selection_method": "eom",
            "cluster_selection_epsilon": 0.2,
        },
        "nr_topics": "auto",
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
            "X-OpenRouter-Title": "BERTopic M02 Topic Representation",
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
                    max_tokens=64,
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
            return model, np.load(EMBEDDINGS_PATH), "使用 M02-8New 既有 embeddings 快取。"
    if A04_EMBEDDINGS.exists() and A04_EMBEDDINGS_META.exists():
        old_meta = json.loads(A04_EMBEDDINGS_META.read_text(encoding="utf-8"))
        if old_meta == current_meta:
            shutil.copy2(A04_EMBEDDINGS, EMBEDDINGS_PATH)
            EMBEDDINGS_META.write_text(json.dumps(current_meta, ensure_ascii=False, indent=2), encoding="utf-8")
            return model, np.load(EMBEDDINGS_PATH), "重用 A04-8(orig) embeddings 快取並複製到 M02-8New。"
    embeddings = model.encode(docs, show_progress_bar=True, batch_size=64, convert_to_numpy=True)
    np.save(EMBEDDINGS_PATH, embeddings)
    EMBEDDINGS_META.write_text(json.dumps(current_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return model, embeddings, "重新計算 embeddings 並建立 M02-8New 快取。"


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


def representative_docs_df(
    topic_model: BERTopic,
    info: pd.DataFrame,
    docs: list[str],
    topics: list[int],
) -> pd.DataFrame:
    rows = []
    docs_by_topic: dict[int, list[str]] = {}
    for doc, topic in zip(docs, topics, strict=False):
        docs_by_topic.setdefault(int(topic), []).append(str(doc))
    for topic in info["Topic"].tolist():
        topic_id = int(topic)
        reps = [str(rep) for rep in (topic_model.get_representative_docs(topic_id) or [])]
        seen = set(reps)
        for doc in docs_by_topic.get(topic_id, []):
            if len(reps) >= REPRESENTATIVE_DOCS_PER_TOPIC:
                break
            if doc not in seen:
                reps.append(doc)
                seen.add(doc)
        for rank, rep in enumerate(reps[:REPRESENTATIVE_DOCS_PER_TOPIC], start=1):
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


def words_lookup(payload: dict[str, Any]) -> dict[int, str]:
    words = payload.get("words")
    if not isinstance(words, pd.DataFrame) or "topic" not in words.columns or "words" not in words.columns:
        return {}
    return {int(row["topic"]): str(row.get("words", "")) for _, row in words.iterrows()}


def build_combined_representation_table(
    representation_outputs: dict[str, dict[str, Any]],
    representative_docs: pd.DataFrame,
    out_dir: Path,
    llm30_summary: pd.DataFrame | None = None,
) -> pd.DataFrame:
    default_info = representation_outputs.get("default", {}).get("info")
    if not isinstance(default_info, pd.DataFrame):
        return pd.DataFrame(
            columns=["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR", "Original_Sentences"]
        )

    llm_lookup = words_lookup(representation_outputs.get(LLM_MODEL_KEY, {}))
    if isinstance(llm30_summary, pd.DataFrame) and not llm30_summary.empty:
        for _, row in llm30_summary.iterrows():
            if "topic" in row and "mode_label" in row and pd.notna(row["mode_label"]):
                llm_lookup[int(row["topic"])] = str(row["mode_label"])
    keybert_lookup = words_lookup(representation_outputs.get("keybert", {}))
    pos_lookup = words_lookup(representation_outputs.get("pos", {}))
    mmr_lookup = words_lookup(representation_outputs.get("mmr", {}))
    if representative_docs.empty:
        original_lookup: dict[int, str] = {}
    else:
        original_lookup = {
            int(topic): " || ".join(group.sort_values("rank")["representative_text"].astype(str).tolist())
            for topic, group in representative_docs.groupby("topic")
        }

    rows = []
    for _, row in default_info.iterrows():
        topic = int(row["Topic"])
        rows.append(
            {
                "Topic": topic,
                "Count": int(row["Count"]),
                "Name": str(row.get("Name", "")),
                "LLM": "Noise / Outlier" if topic == -1 else llm_lookup.get(topic, ""),
                "KeyBERT": keybert_lookup.get(topic, ""),
                "POS": pos_lookup.get(topic, ""),
                "MMR": mmr_lookup.get(topic, ""),
                "Original_Sentences": original_lookup.get(topic, ""),
            }
        )
    combined = pd.DataFrame(
        rows,
        columns=["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR", "Original_Sentences"],
    )
    combined.to_csv(out_dir / "M02-8New_combined_representations.csv", index=False)
    md = [
        "# M02-8New Combined Topic Representations",
        "",
        md_table(
            combined.to_dict("records"),
            ["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR", "Original_Sentences"],
        ),
        "",
    ]
    (out_dir / "M02-8New_combined_representations.md").write_text("\n".join(md), encoding="utf-8")
    return combined


def build_llm_representations(errors: list[dict[str, str]]) -> dict[str, OpenRouterLLMRepresentation | None]:
    global OPENROUTER_PREFLIGHT_ERROR
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        OPENROUTER_PREFLIGHT_ERROR = "OPENROUTER_API_KEY was not provided."
        for name, model in LLM_MODELS:
            errors.append({"representation_model": name, "model": model, "error": "OPENROUTER_API_KEY was not provided."})
        return {name: None for name, _ in LLM_MODELS}
    preflight_error = openrouter_preflight(api_key)
    if preflight_error:
        OPENROUTER_PREFLIGHT_ERROR = preflight_error
        for name, model in LLM_MODELS:
            errors.append({"representation_model": name, "model": model, "error": preflight_error})
        return {name: None for name, _ in LLM_MODELS}
    OPENROUTER_PREFLIGHT_ERROR = ""
    return {
        name: OpenRouterLLMRepresentation(
            api_key=api_key,
            model=model,
            max_docs=REPRESENTATIVE_DOCS_PER_TOPIC,
            doc_chars=360,
            delay_seconds=float(os.getenv("OPENROUTER_DELAY_SECONDS", "0.15")),
        )
        for name, model in LLM_MODELS
    }


def openrouter_preflight(api_key: str) -> str:
    last_error = ""
    for attempt in range(1, 4):
        try:
            client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
            response = client.chat.completions.create(
                model=LLM_MODEL_NAME,
                messages=[{"role": "user", "content": "Return exactly: ok"}],
                temperature=0.0,
                max_tokens=16,
                extra_headers={
                    "HTTP-Referer": "https://local.bertopic.m02",
                    "X-OpenRouter-Title": "BERTopic M02 OpenRouter Preflight",
                },
            )
            if not getattr(response, "choices", None):
                raise ValueError("OpenRouter preflight returned no choices")
            text = (response.choices[0].message.content or "").strip().lower()
            if "ok" not in text:
                raise ValueError(f"OpenRouter preflight returned unexpected text: {text}")
            return ""
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.75 * attempt)
    return f"OpenRouter preflight failed after retries: {last_error}"


def normalize_label(label: str) -> str:
    text = re.sub(r"^(topic label|topic):\s*", "", str(label), flags=re.I).strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" -")
    return text


def jaccard_similarity(left: str, right: str) -> float:
    left_tokens = set(normalize_label(left).split())
    right_tokens = set(normalize_label(right).split())
    if not left_tokens and not right_tokens:
        return 1.0
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def llm30_prompt(topic_id: int, keywords: str, snippets: list[str]) -> list[dict[str, str]]:
    snippet_text = "\n".join(f"- {snippet[:420]}" for snippet in snippets[:REPRESENTATIVE_DOCS_PER_TOPIC])
    return [
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
                f"Representative snippets:\n{snippet_text}\n\n"
                "Topic label:"
            ),
        },
    ]


def call_openrouter_label(
    client: OpenAI,
    topic_id: int,
    keywords: str,
    snippets: list[str],
    temperature: float = 0.0,
) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL_NAME,
        messages=llm30_prompt(topic_id, keywords, snippets),
        temperature=temperature,
        max_tokens=64,
        extra_headers={
            "HTTP-Referer": "https://local.bertopic.m02",
            "X-OpenRouter-Title": "BERTopic M02 LLM30 Validation",
        },
    )
    if not getattr(response, "choices", None):
        raise ValueError("OpenRouter returned no choices")
    label = (response.choices[0].message.content or "").strip()
    label = re.sub(r"^(topic label|topic):\s*", "", label, flags=re.I).strip()
    label = label.replace("\n", " ").strip(" .:-")
    if not label:
        raise ValueError("OpenRouter returned an empty label")
    return label


def load_llm30_cache(cache_path: Path) -> dict[tuple[int, int], dict[str, Any]]:
    cached: dict[tuple[int, int], dict[str, Any]] = {}
    if not cache_path.exists():
        return cached
    for line in cache_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if item.get("normalized_label") and not item.get("error"):
            cached[(int(item["topic"]), int(item["run"]))] = item
    return cached


def llm30_request_task(
    api_key: str,
    topic_id: int,
    run_idx: int,
    keywords: str,
    snippets: list[str],
) -> dict[str, Any]:
    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    last_error = ""
    for attempt in range(1, 4):
        try:
            label = call_openrouter_label(client, topic_id, keywords, snippets, temperature=0.0)
            return {
                "topic": topic_id,
                "run": run_idx,
                "model": LLM_MODEL_NAME,
                "keywords": keywords,
                "label": label,
                "normalized_label": normalize_label(label),
                "error": "",
            }
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.75 * attempt)
    return {
        "topic": topic_id,
        "run": run_idx,
        "model": LLM_MODEL_NAME,
        "keywords": keywords,
        "label": "",
        "normalized_label": "",
        "error": last_error,
    }


def run_llm30_validation(
    docs: list[str],
    topics: list[int],
    topic_words: pd.DataFrame,
    out_dir: Path,
    errors: list[dict[str, str]],
) -> dict[str, Any]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        errors.append({"representation_model": "llm30", "error": "OPENROUTER_API_KEY was not provided."})
        return {"status": "skipped", "topics": 0, "calls": 0, "stable_topics": 0}
    preflight_error = openrouter_preflight(api_key)
    if preflight_error:
        errors.append({"representation_model": "llm30", "model": LLM_MODEL_NAME, "error": preflight_error})
        skipped_df = pd.DataFrame(
            [
                {
                    "topic": "",
                    "model": LLM_MODEL_NAME,
                    "runs_requested": LLM30_RUNS,
                    "successful_runs": 0,
                    "error_runs": 0,
                    "unique_normalized_labels": 0,
                    "mode_label": "",
                    "mode_normalized_label": "",
                    "mode_count": 0,
                    "mode_ratio": 0.0,
                    "avg_jaccard_to_mode": 0.0,
                    "stable": False,
                    "keywords": "",
                    "all_labels": "",
                    "status": "skipped",
                    "error": preflight_error,
                }
            ]
        )
        skipped_df.to_csv(out_dir / "M02-8New_LLM30.csv", index=False)
        pd.DataFrame(columns=["topic", "run", "model", "keywords", "label", "normalized_label", "error"]).to_csv(
            out_dir / "M02-8New_LLM30_detail.csv",
            index=False,
        )
        (out_dir / "M02-8New_LLM30.md").write_text(
            "\n".join(
                [
                    "# M02-8New LLM30 Validation",
                    "",
                    f"- model: `{LLM_MODEL_NAME}` via OpenRouter",
                    "- status: `skipped`",
                    f"- reason: {preflight_error}",
                    "",
                    "BERTopic clustering and non-LLM representation outputs were still generated.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return {"status": "skipped", "topics": 0, "calls": 0, "stable_topics": 0, "error": preflight_error}

    doc_df = pd.DataFrame({"Document": docs, "Topic": topics})
    topic_ids = [int(topic) for topic in topic_words["topic"].tolist() if int(topic) != -1]
    cache_path = out_dir / "M02-8New_LLM30_cache.jsonl"
    cached = load_llm30_cache(cache_path)
    records: list[dict[str, Any]] = []
    max_workers = max(1, int(os.getenv("OPENROUTER_LLM30_WORKERS", "6")))
    pending: list[tuple[int, int, str, list[str]]] = []

    for topic_id in topic_ids:
        row = topic_words.loc[topic_words["topic"] == topic_id].iloc[0]
        keywords = str(row.get("words", ""))
        snippets = (
            doc_df.loc[doc_df["Topic"] == topic_id, "Document"]
            .dropna()
            .astype(str)
            .head(REPRESENTATIVE_DOCS_PER_TOPIC)
            .tolist()
        )
        for run_idx in range(1, LLM30_RUNS + 1):
            cache_key = (topic_id, run_idx)
            if cache_key in cached:
                records.append(cached[cache_key])
            else:
                pending.append((topic_id, run_idx, keywords, snippets))

    print(
        f"  LLM30 cache: {len(records)} done, {len(pending)} pending, workers={max_workers}",
        flush=True,
    )
    completed = 0
    with cache_path.open("a", encoding="utf-8") as cache_file:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(llm30_request_task, api_key, topic_id, run_idx, keywords, snippets)
                for topic_id, run_idx, keywords, snippets in pending
            ]
            for future in as_completed(futures):
                item = future.result()
                cache_file.write(json.dumps(item, ensure_ascii=False) + "\n")
                cache_file.flush()
                cached[(int(item["topic"]), int(item["run"]))] = item
                records.append(item)
                completed += 1
                if item.get("error"):
                    errors.append(
                        {
                            "representation_model": "llm30",
                            "topic": str(item["topic"]),
                            "run": str(item["run"]),
                            "model": LLM_MODEL_NAME,
                            "error": str(item["error"]),
                        }
                    )
                if completed % 25 == 0 or completed == len(pending):
                    print(f"  LLM30 completed {completed}/{len(pending)} pending calls", flush=True)

    detail_df = pd.DataFrame(records)
    summary_rows: list[dict[str, Any]] = []
    for topic_id, group in detail_df.groupby("topic", sort=True):
        labels = [label for label in group["normalized_label"].tolist() if label]
        counts = Counter(labels)
        mode_label, mode_count = counts.most_common(1)[0] if counts else ("", 0)
        raw_mode_labels = group.loc[group["normalized_label"] == mode_label, "label"].tolist()
        display_mode = raw_mode_labels[0] if raw_mode_labels else ""
        successful = len(labels)
        exact_ratio = mode_count / successful if successful else 0.0
        avg_jaccard = float(np.mean([jaccard_similarity(label, mode_label) for label in labels])) if labels else 0.0
        is_stable = bool(exact_ratio >= 0.70 or avg_jaccard >= 0.65)
        keyword_text = str(group["keywords"].iloc[0])
        summary_rows.append(
            {
                "topic": int(topic_id),
                "model": LLM_MODEL_NAME,
                "runs_requested": LLM30_RUNS,
                "successful_runs": successful,
                "error_runs": int(group["error"].astype(bool).sum()),
                "unique_normalized_labels": len(counts),
                "mode_label": display_mode,
                "mode_normalized_label": mode_label,
                "mode_count": mode_count,
                "mode_ratio": exact_ratio,
                "avg_jaccard_to_mode": avg_jaccard,
                "stable": is_stable,
                "keywords": keyword_text,
                "all_labels": " || ".join(str(label) for label in group["label"].tolist() if label),
            }
        )
    summary_df = pd.DataFrame(summary_rows)
    detail_df.to_csv(out_dir / "M02-8New_LLM30_detail.csv", index=False)
    summary_df.to_csv(out_dir / "M02-8New_LLM30.csv", index=False)

    md_rows = summary_df[
        [
            "topic",
            "successful_runs",
            "unique_normalized_labels",
            "mode_label",
            "mode_ratio",
            "avg_jaccard_to_mode",
            "stable",
            "keywords",
        ]
    ].to_dict("records")
    report = [
        "# M02-8New LLM30 Validation",
        "",
        f"- model: `{LLM_MODEL_NAME}` via OpenRouter",
        f"- runs per non-noise topic: {LLM30_RUNS}",
        f"- input per topic: same default c-TF-IDF keywords and same first {REPRESENTATIVE_DOCS_PER_TOPIC} representative topic documents",
        "- stable rule: `mode_ratio >= 0.70` or `avg_jaccard_to_mode >= 0.65`",
        f"- stable topics: {int(summary_df['stable'].sum()) if not summary_df.empty else 0} / {len(summary_df)}",
        "",
        md_table(md_rows, list(md_rows[0].keys()) if md_rows else ["topic"]),
        "",
        "## Interpretation",
        "",
        "若 `stable=True`，代表同一組 keywords 與文本重跑時，模型給出的主題名稱在字面或詞彙組成上大致一致；若為 `False`，建議人工檢查該 topic 的 keywords 是否過於混雜。",
        "",
    ]
    (out_dir / "M02-8New_LLM30.md").write_text("\n".join(report), encoding="utf-8")
    return {
        "status": "ok",
        "topics": len(summary_df),
        "calls": len(detail_df),
        "stable_topics": int(summary_df["stable"].sum()) if not summary_df.empty else 0,
        "csv": "M02-8New_LLM30.csv",
        "md": "M02-8New_LLM30.md",
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
    combined_representations: pd.DataFrame,
    csv_paths: dict[str, str],
    errors: list[dict[str, str]],
    started_at: str,
    finished_at: str,
) -> None:
    label = config["selection_label"]
    parameter_row = {
        "selection_label": label,
        "selection_reason": config["selection_reason"],
        "bertopic_nr_topics": config.get("nr_topics"),
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
        "llm_model": LLM_MODEL_NAME,
        "llm30_runs_per_topic": LLM30_RUNS,
        "representative_docs_per_topic": REPRESENTATIVE_DOCS_PER_TOPIC,
    }
    report = [
        f"# M02-8New BERTopic + A05-8.4(human) stopwords + c-TF-IDF reduction - {label}",
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
        f"- {LLM_MODEL_KEY}: OpenRouter `{LLM_MODEL_NAME}` topic labels",
        "",
        "## LLM30 Validation",
        "",
        f"- 每個非 noise topic 使用 `{LLM_MODEL_NAME}` 對相同 keywords 與 {REPRESENTATIVE_DOCS_PER_TOPIC} 個代表原句重跑 {LLM30_RUNS} 次。",
        "- 穩定判定：normalized label 眾數比例 >= 0.70，或平均 token Jaccard similarity >= 0.65。",
        "- 詳細輸出：`M02-8New_LLM30.md`、`M02-8New_LLM30.csv`。",
        "",
        "## Combined Topic Representations",
        "",
        md_table(
            combined_representations.to_dict("records"),
            ["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR", "Original_Sentences"],
        )
        if not combined_representations.empty
        else "無",
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
            "BERTopic `nr_topics='auto'` 會在初始 HDBSCAN 分群後使用 c-TF-IDF 相似度自動合併主題；本報告 metrics 為 reduction 後的 topic labels。",
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
        nr_topics=config.get("nr_topics"),
        calculate_probabilities=False,
        verbose=False,
    )
    topics, _ = topic_model.fit_transform(docs, embeddings)
    topics = [int(topic) for topic in getattr(topic_model, "topics_", topics)]
    metrics = label_metrics(topics)
    pd.DataFrame({"title": titles, "sentence": docs, "topic": topics}).to_csv(out_dir / "document_topics.csv", index=False)
    base_info = topic_model.get_topic_info()
    representative_docs = representative_docs_df(topic_model, base_info, docs, topics)
    representative_docs.to_csv(out_dir / "representative_docs.csv", index=False)
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
            errors.append(
                {
                    "representation_model": name,
                    "model": LLM_MODEL_NAME,
                    "error": OPENROUTER_PREFLIGHT_ERROR or "OpenRouter LLM representation was skipped.",
                }
            )
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

    default_words = representation_outputs.get("default", {}).get("words")
    llm30_summary = {"status": "not_run", "topics": 0, "calls": 0, "stable_topics": 0}
    if isinstance(default_words, pd.DataFrame):
        print("  LLM30 validation: openai/gpt-5.5", flush=True)
        llm30_summary = run_llm30_validation(docs, topics, default_words, OUTPUT_DIR, errors)
    llm30_df_path = OUTPUT_DIR / "M02-8New_LLM30.csv"
    llm30_df = pd.read_csv(llm30_df_path) if llm30_df_path.exists() else None
    combined_representations = build_combined_representation_table(
        representation_outputs,
        representative_docs,
        OUTPUT_DIR,
        llm30_df,
    )

    (out_dir / "representation_errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
    config_record = {
        **config,
        "m02_metrics": metrics,
        "dataset": str(DATASET_DIR.relative_to(ROOT)),
        "embedding_model": EMBEDDING_MODEL_NAME,
        "custom_stopwords_count": len(custom_stopwords),
        "stopword_source": str(STOPWORD_MD.relative_to(ROOT)),
        "nr_topics": config.get("nr_topics"),
        "representation_models": list(representations.keys()),
        "llm_provider": "OpenRouter",
        "llm_model": LLM_MODEL_NAME,
        "llm30_summary": llm30_summary,
        "representative_docs_per_topic": REPRESENTATIVE_DOCS_PER_TOPIC,
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
        "combined_representations_csv": "M02-8New_combined_representations.csv",
        "combined_representations_md": "M02-8New_combined_representations.md",
        "final_config": str((out_dir / "final_config.json").relative_to(OUTPUT_DIR)),
        "representation_errors": str((out_dir / "representation_errors.json").relative_to(OUTPUT_DIR)),
        "llm30_summary": "M02-8New_LLM30.csv",
        "llm30_report": "M02-8New_LLM30.md",
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
        combined_representations,
        csv_paths,
        errors,
        started_at,
        datetime.now(timezone.utc).isoformat(),
    )
    return {
        "selection_label": label,
        "report": config["report_name"],
        **metrics,
        "llm30_status": llm30_summary.get("status"),
        "llm30_topics": llm30_summary.get("topics"),
        "llm30_stable_topics": llm30_summary.get("stable_topics"),
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
    (OUTPUT_DIR / "M02-8New_custom_stopwords_used.txt").write_text(
        "\n".join(custom_stopwords) + "\n", encoding="utf-8"
    )
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
    pd.DataFrame(summaries).to_csv(OUTPUT_DIR / "M02-8New_summary.csv", index=False)
    (OUTPUT_DIR / "M02-8New_run_summary.json").write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "M02-8New_run_log.json").write_text(
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
                "llm_model": LLM_MODEL_NAME,
                "llm30_runs_per_topic": LLM30_RUNS,
                "representative_docs_per_topic": REPRESENTATIVE_DOCS_PER_TOPIC,
                "global_errors": global_errors,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
