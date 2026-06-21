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
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance, PartOfSpeech
from datasets import load_from_disk
from hdbscan import HDBSCAN
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from umap import UMAP


ROOT = Path(__file__).resolve().parents[3]
DATASET_DIR = ROOT / "Result/06.13_[B]tok/06.13_[B]01-pre_LLM(orig)_20-25(194)_tok(para12-80)_dataset"
STOPWORD_MD = ROOT / "Result/06.05_A05_stopword/A05-8(orig)REV_tok(para12-80)/A05-8.4(human)_stopword.md"
OUTPUT_DIR = ROOT / "Result/06.17_M03_split/06.17_M03-2(orig_20-25_tp-50)"
RUN_BASENAME = OUTPUT_DIR.name

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDINGS_PATH = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.npy"
EMBEDDINGS_META = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.meta.json"
EMBEDDING_SOURCES = [
    (
        ROOT / "Result/06.13_[D]UMAP/[B]01-(orig)_20-25_tok(para12-80)/embeddings_all-MiniLM-L6-v2.npy",
        ROOT / "Result/06.13_[D]UMAP/[B]01-(orig)_20-25_tok(para12-80)/embeddings_all-MiniLM-L6-v2.meta.json",
        "重用 06.13_[D]UMAP/[B]01-(orig)_20-25 embeddings 快取。",
    ),
    (
        ROOT / "Result/06.13_[C]min/[B]01-(orig)_20-25(194)_tok(para12-80)/cache/embeddings_all-MiniLM-L6-v2.npy",
        None,
        "重用 06.13_[C]min/[B]01-(orig)_20-25 cache embeddings 快取。",
    ),
]

TEXT_COL = "sentence"
RANDOM_STATE = 42
REPRESENTATIVE_DOCS_PER_TOPIC = 6
LLM_MODEL_NAME = "openai/gpt-5.5"
LLM50_RUNS = 50
LLM_TEMPERATURE = 0.0
LLM_MAX_TOKENS = 64

CONFIG = {
    "selection_label": RUN_BASENAME,
    "report_name": f"{RUN_BASENAME}.md",
    "selection_reason": "使用者指定單組參數，並以 BERTopic nr_topics='auto' 做 c-TF-IDF topic reduction。",
    "nr_topics": "auto",
    "umap": {
        "n_neighbors": 10,
        "n_components": 5,
        "min_dist": 0.0,
        "metric": "cosine",
        "random_state": RANDOM_STATE,
    },
    "hdbscan": {
        "min_cluster_size": 125,
        "min_samples": 5,
        "metric": "euclidean",
        "cluster_selection_method": "eom",
        "cluster_selection_epsilon": 0.0,
    },
}


class BERTopicNrReprDocs(BERTopic):
    def _extract_representative_docs(
        self,
        c_tf_idf,
        documents: pd.DataFrame,
        topics: Mapping[str, list[tuple[str, float]]],
        nr_samples: int = 500,
        nr_repr_docs: int = REPRESENTATIVE_DOCS_PER_TOPIC,
        diversity: float | None = None,
    ):
        return super()._extract_representative_docs(
            c_tf_idf,
            documents,
            topics,
            nr_samples=nr_samples,
            nr_repr_docs=nr_repr_docs,
            diversity=diversity,
        )


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        values = []
        for col in columns:
            value = row.get(col, "")
            if isinstance(value, float):
                text = f"{value:.4f}"
            else:
                text = "" if value is None else str(value)
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


def prompt_hash(system_prompt: str, user_prompt: str) -> str:
    return hashlib.sha256((system_prompt + "\n" + user_prompt).encode("utf-8")).hexdigest()[:16]


def load_documents() -> tuple[list[str], list[str], pd.DataFrame, dict[str, Any]]:
    dataset = load_from_disk(str(DATASET_DIR))
    columns = list(dataset.column_names)
    if TEXT_COL not in columns:
        raise ValueError(f"Dataset missing required text column: {TEXT_COL}")

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
        titles.append(str(item.get("title", "")))
        row = {column: item.get(column) for column in columns}
        row["dataset_row"] = idx
        row["document"] = text
        rows.append(row)
        if len(text.split()) < 3:
            short_rows.append(idx)

    lengths = [len(doc) for doc in docs]
    word_counts = [len(doc.split()) for doc in docs]
    meta = {
        "dataset": str(DATASET_DIR.relative_to(ROOT)),
        "columns": columns,
        "source_rows": len(dataset),
        "used_rows": len(docs),
        "empty_rows_count": len(empty_rows),
        "short_rows_lt_3_words_count": len(short_rows),
        "text_col": TEXT_COL,
        "embedding_model": EMBEDDING_MODEL_NAME,
        "stopword_source": str(STOPWORD_MD.relative_to(ROOT)),
        "min_text_len": min(lengths, default=0),
        "max_text_len": max(lengths, default=0),
        "avg_text_len": float(np.mean(lengths)) if lengths else 0.0,
        "min_word_count": min(word_counts, default=0),
        "max_word_count": max(word_counts, default=0),
        "avg_word_count": float(np.mean(word_counts)) if word_counts else 0.0,
    }
    return docs, titles, pd.DataFrame(rows), meta


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
            if not term:
                continue
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
        raise ValueError(f"Could not find stopwords in {path}")
    return sorted(words)


def get_embeddings(docs: list[str]) -> tuple[SentenceTransformer, np.ndarray, str]:
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    current_meta = {"model": EMBEDDING_MODEL_NAME, "doc_count": len(docs), "docs_hash": docs_hash(docs)}
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if EMBEDDINGS_PATH.exists() and EMBEDDINGS_META.exists():
        old_meta = json.loads(EMBEDDINGS_META.read_text(encoding="utf-8"))
        if old_meta == current_meta:
            return model, np.load(EMBEDDINGS_PATH), f"使用 {RUN_BASENAME} 既有 embeddings 快取。"

    for source_path, source_meta_path, note in EMBEDDING_SOURCES:
        if not source_path.exists():
            continue
        if source_meta_path is not None:
            if not source_meta_path.exists():
                continue
            old_meta = json.loads(source_meta_path.read_text(encoding="utf-8"))
            if old_meta != current_meta:
                continue
        embeddings = np.load(source_path)
        if embeddings.shape[0] != len(docs):
            continue
        shutil.copy2(source_path, EMBEDDINGS_PATH)
        EMBEDDINGS_META.write_text(json.dumps(current_meta, ensure_ascii=False, indent=2), encoding="utf-8")
        return model, np.load(EMBEDDINGS_PATH), note

    embeddings = model.encode(docs, show_progress_bar=True, batch_size=64, convert_to_numpy=True)
    np.save(EMBEDDINGS_PATH, embeddings)
    EMBEDDINGS_META.write_text(json.dumps(current_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return model, embeddings, f"重新計算 embeddings 並建立 {RUN_BASENAME} 快取。"


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
            rows.append({"topic": topic_id, "rank": rank, "representative_text": rep})
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


def llm_prompt_messages(topic_id: int, keywords: str, snippets: list[str]) -> list[dict[str, str]]:
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


def openrouter_preflight(api_key: str) -> str:
    last_error = ""
    for attempt in range(1, 4):
        try:
            client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
            response = client.chat.completions.create(
                model=LLM_MODEL_NAME,
                messages=[{"role": "user", "content": "Return exactly: ok"}],
                temperature=LLM_TEMPERATURE,
                max_tokens=16,
                extra_headers={
                    "HTTP-Referer": "https://local.bertopic.m03",
                    "X-OpenRouter-Title": "BERTopic M03 OpenRouter Preflight",
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


def call_openrouter_label(client: OpenAI, messages: list[dict[str, str]]) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL_NAME,
        messages=messages,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
        extra_headers={
            "HTTP-Referer": "https://local.bertopic.m03",
            "X-OpenRouter-Title": "BERTopic M03 LLM50 Validation",
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


def load_llm50_cache(cache_path: Path) -> dict[tuple[int, int, str], dict[str, Any]]:
    cached: dict[tuple[int, int, str], dict[str, Any]] = {}
    if not cache_path.exists():
        return cached
    for line in cache_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if item.get("normalized_label") and not item.get("error"):
            cached[(int(item["topic"]), int(item["run"]), str(item.get("prompt_hash", "")))] = item
    return cached


def llm50_request_task(
    api_key: str,
    topic_id: int,
    run_idx: int,
    keywords: str,
    snippets: list[str],
) -> dict[str, Any]:
    messages = llm_prompt_messages(topic_id, keywords, snippets)
    system_prompt = messages[0]["content"]
    user_prompt = messages[1]["content"]
    p_hash = prompt_hash(system_prompt, user_prompt)
    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    last_error = ""
    for attempt in range(1, 4):
        try:
            label = call_openrouter_label(client, messages)
            return {
                "topic": topic_id,
                "run": run_idx,
                "model": LLM_MODEL_NAME,
                "temperature": LLM_TEMPERATURE,
                "max_tokens": LLM_MAX_TOKENS,
                "keywords": keywords,
                "prompt_hash": p_hash,
                "prompt_system": system_prompt,
                "prompt_user": user_prompt,
                "prompt_json": json.dumps(messages, ensure_ascii=False),
                "label": label,
                "normalized_label": normalize_label(label),
                "error": "",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.75 * attempt)
    return {
        "topic": topic_id,
        "run": run_idx,
        "model": LLM_MODEL_NAME,
        "temperature": LLM_TEMPERATURE,
        "max_tokens": LLM_MAX_TOKENS,
        "keywords": keywords,
        "prompt_hash": p_hash,
        "prompt_system": system_prompt,
        "prompt_user": user_prompt,
        "prompt_json": json.dumps(messages, ensure_ascii=False),
        "label": "",
        "normalized_label": "",
        "error": last_error,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def topic_prompt_inputs(
    topic_words: pd.DataFrame,
    representative_docs: pd.DataFrame,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for topic_id in [int(topic) for topic in topic_words["topic"].tolist() if int(topic) != -1]:
        row = topic_words.loc[topic_words["topic"] == topic_id].iloc[0]
        keywords = str(row.get("words", ""))
        snippets = (
            representative_docs.loc[representative_docs["topic"] == topic_id]
            .sort_values("rank")["representative_text"]
            .dropna()
            .astype(str)
            .head(REPRESENTATIVE_DOCS_PER_TOPIC)
            .tolist()
        )
        messages = llm_prompt_messages(topic_id, keywords, snippets)
        rows.append(
            {
                "topic": topic_id,
                "keywords": keywords,
                "representative_snippets": " || ".join(snippets),
                "prompt_hash": prompt_hash(messages[0]["content"], messages[1]["content"]),
                "prompt_system": messages[0]["content"],
                "prompt_user": messages[1]["content"],
                "prompt_json": json.dumps(messages, ensure_ascii=False),
            }
        )
    return rows


def summarize_llm_detail(detail_df: pd.DataFrame) -> pd.DataFrame:
    summary_rows: list[dict[str, Any]] = []
    if detail_df.empty:
        return pd.DataFrame()
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
        summary_rows.append(
            {
                "topic": int(topic_id),
                "model": LLM_MODEL_NAME,
                "runs_requested": LLM50_RUNS,
                "successful_runs": successful,
                "error_runs": int(group["error"].astype(bool).sum()) if "error" in group.columns else 0,
                "unique_normalized_labels": len(counts),
                "mode_label": display_mode,
                "mode_normalized_label": mode_label,
                "mode_count": mode_count,
                "mode_ratio": exact_ratio,
                "avg_jaccard_to_mode": avg_jaccard,
                "stable": is_stable,
                "符合抽樣結果": "是" if is_stable else "否",
                "keywords": str(group["keywords"].iloc[0]) if "keywords" in group.columns else "",
                "prompt_hash": str(group["prompt_hash"].iloc[0]) if "prompt_hash" in group.columns else "",
                "prompt_system": str(group["prompt_system"].iloc[0]) if "prompt_system" in group.columns else "",
                "prompt_user": str(group["prompt_user"].iloc[0]) if "prompt_user" in group.columns else "",
                "prompt_json": str(group["prompt_json"].iloc[0]) if "prompt_json" in group.columns else "",
                "all_labels": " || ".join(str(label) for label in group["label"].tolist() if label),
            }
        )
    return pd.DataFrame(summary_rows)


def write_llm_md(detail_df: pd.DataFrame, summary_df: pd.DataFrame, prompt_df: pd.DataFrame, status: str, error: str = "") -> None:
    stable_text = "0 / 0"
    if not summary_df.empty and "stable" in summary_df.columns:
        stable_text = f"{int(summary_df['stable'].astype(bool).sum())} / {len(summary_df)}"

    summary_columns = [
        "topic",
        "successful_runs",
        "error_runs",
        "unique_normalized_labels",
        "mode_label",
        "mode_ratio",
        "avg_jaccard_to_mode",
        "符合抽樣結果",
        "keywords",
    ]
    detail_columns = ["topic", "run", "label", "normalized_label", "error"]
    prompt_columns = ["topic", "keywords", "prompt_hash", "prompt_system", "prompt_user"]

    report = [
        f"# {RUN_BASENAME} LLM",
        "",
        f"- model: `{LLM_MODEL_NAME}` via OpenRouter",
        f"- temperature: `{LLM_TEMPERATURE}`",
        f"- max_tokens: `{LLM_MAX_TOKENS}`",
        f"- runs per non-noise topic: {LLM50_RUNS}",
        f"- representative docs per topic: {REPRESENTATIVE_DOCS_PER_TOPIC}",
        "- stable rule: `mode_ratio >= 0.70` or `avg_jaccard_to_mode >= 0.65`",
        f"- stable topics: {stable_text}",
        f"- status: `{status}`",
    ]
    if error:
        report.append(f"- error: {error}")
    report.extend(
        [
            "",
            "## Validation Summary",
            "",
            md_table(summary_df[summary_columns].to_dict("records"), summary_columns)
            if not summary_df.empty
            else "無",
            "",
            "## Prompt By Topic",
            "",
            md_table(prompt_df[prompt_columns].to_dict("records"), prompt_columns)
            if not prompt_df.empty
            else "無",
            "",
            "## All Run Outputs",
            "",
            md_table(detail_df[detail_columns].to_dict("records"), detail_columns)
            if not detail_df.empty
            else "無",
            "",
            "## Interpretation",
            "",
            "若 `符合抽樣結果=是`，代表同一組 keywords 與代表文本重跑時，模型給出的主題名稱在字面或詞彙組成上大致一致；若為 `否`，建議人工檢查該 topic 的 keywords 或代表文本是否過於混雜。",
            "",
        ]
    )
    (OUTPUT_DIR / f"{RUN_BASENAME}_LLM.md").write_text("\n".join(report), encoding="utf-8")


def run_llm50_validation(
    topic_words: pd.DataFrame,
    representative_docs: pd.DataFrame,
    errors: list[dict[str, str]],
) -> dict[str, Any]:
    prompt_rows = topic_prompt_inputs(topic_words, representative_docs)
    prompt_df = pd.DataFrame(prompt_rows)
    prompt_df.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_LLM_prompts.csv", index=False)

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        error = "OPENROUTER_API_KEY was not provided."
        errors.append({"representation_model": "llm50", "model": LLM_MODEL_NAME, "error": error})
        detail_df = pd.DataFrame(
            [
                {
                    **row,
                    "run": 0,
                    "model": LLM_MODEL_NAME,
                    "temperature": LLM_TEMPERATURE,
                    "max_tokens": LLM_MAX_TOKENS,
                    "label": "",
                    "normalized_label": "",
                    "error": error,
                }
                for row in prompt_rows
            ]
        )
        summary_df = summarize_llm_detail(detail_df) if not detail_df.empty else pd.DataFrame()
        detail_df.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_LLM.csv", index=False)
        detail_df.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_LLM_detail.csv", index=False)
        summary_df.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_LLM_validation.csv", index=False)
        write_llm_md(detail_df, summary_df, prompt_df, "skipped", error)
        return {"status": "skipped", "topics": len(prompt_rows), "calls": 0, "stable_topics": 0, "error": error}

    preflight_error = openrouter_preflight(api_key)
    if preflight_error:
        errors.append({"representation_model": "llm50", "model": LLM_MODEL_NAME, "error": preflight_error})
        detail_df = pd.DataFrame(
            [
                {
                    **row,
                    "run": 0,
                    "model": LLM_MODEL_NAME,
                    "temperature": LLM_TEMPERATURE,
                    "max_tokens": LLM_MAX_TOKENS,
                    "label": "",
                    "normalized_label": "",
                    "error": preflight_error,
                }
                for row in prompt_rows
            ]
        )
        summary_df = summarize_llm_detail(detail_df) if not detail_df.empty else pd.DataFrame()
        detail_df.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_LLM.csv", index=False)
        detail_df.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_LLM_detail.csv", index=False)
        summary_df.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_LLM_validation.csv", index=False)
        write_llm_md(detail_df, summary_df, prompt_df, "skipped", preflight_error)
        return {"status": "skipped", "topics": len(prompt_rows), "calls": 0, "stable_topics": 0, "error": preflight_error}

    cache_path = OUTPUT_DIR / f"{RUN_BASENAME}_LLM_cache.jsonl"
    cached = load_llm50_cache(cache_path)
    records: list[dict[str, Any]] = []
    pending: list[tuple[int, int, str, list[str]]] = []

    for row in prompt_rows:
        topic_id = int(row["topic"])
        keywords = str(row["keywords"])
        snippets = str(row.get("representative_snippets", "")).split(" || ") if row.get("representative_snippets") else []
        for run_idx in range(1, LLM50_RUNS + 1):
            cache_key = (topic_id, run_idx, str(row["prompt_hash"]))
            if cache_key in cached:
                records.append(cached[cache_key])
            else:
                pending.append((topic_id, run_idx, keywords, snippets))

    max_workers = max(1, int(os.getenv("OPENROUTER_LLM50_WORKERS", "4")))
    print(f"  LLM50 cache: {len(records)} done, {len(pending)} pending, workers={max_workers}", flush=True)
    completed = 0
    with cache_path.open("a", encoding="utf-8") as cache_file:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(llm50_request_task, api_key, topic_id, run_idx, keywords, snippets)
                for topic_id, run_idx, keywords, snippets in pending
            ]
            for future in as_completed(futures):
                item = future.result()
                cache_file.write(json.dumps(item, ensure_ascii=False) + "\n")
                cache_file.flush()
                records.append(item)
                completed += 1
                if item.get("error"):
                    errors.append(
                        {
                            "representation_model": "llm50",
                            "topic": str(item["topic"]),
                            "run": str(item["run"]),
                            "model": LLM_MODEL_NAME,
                            "error": str(item["error"]),
                        }
                    )
                if completed % 25 == 0 or completed == len(pending):
                    print(f"  LLM50 completed {completed}/{len(pending)} pending calls", flush=True)

    detail_df = pd.DataFrame(records)
    if not detail_df.empty:
        detail_df = detail_df.sort_values(["topic", "run"]).reset_index(drop=True)
    summary_df = summarize_llm_detail(detail_df)
    detail_df.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_LLM.csv", index=False)
    detail_df.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_LLM_detail.csv", index=False)
    summary_df.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_LLM_validation.csv", index=False)
    write_llm_md(detail_df, summary_df, prompt_df, "ok")

    return {
        "status": "ok",
        "topics": len(summary_df),
        "calls": len(detail_df),
        "stable_topics": int(summary_df["stable"].sum()) if not summary_df.empty else 0,
        "llm_result_md": f"{RUN_BASENAME}_LLM.md",
        "llm_result_csv": f"{RUN_BASENAME}_LLM.csv",
        "llm_validation_csv": f"{RUN_BASENAME}_LLM_validation.csv",
    }


def build_combined_representation_table(
    representation_outputs: dict[str, dict[str, Any]],
    representative_docs: pd.DataFrame,
    llm50_summary: pd.DataFrame | None = None,
) -> pd.DataFrame:
    default_info = representation_outputs.get("default", {}).get("info")
    if not isinstance(default_info, pd.DataFrame):
        return pd.DataFrame(columns=["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"])

    llm_lookup: dict[int, str] = {}
    if isinstance(llm50_summary, pd.DataFrame) and not llm50_summary.empty:
        for _, row in llm50_summary.iterrows():
            if "topic" in row and "mode_label" in row and pd.notna(row["mode_label"]):
                llm_lookup[int(row["topic"])] = str(row["mode_label"])

    keybert_lookup = words_lookup(representation_outputs.get("keybert", {}))
    pos_lookup = words_lookup(representation_outputs.get("pos", {}))
    mmr_lookup = words_lookup(representation_outputs.get("mmr", {}))
    original_lookup = {
        int(topic): " || ".join(group.sort_values("rank")["representative_text"].astype(str).tolist())
        for topic, group in representative_docs.groupby("topic")
    } if not representative_docs.empty else {}

    rows = []
    rows_with_docs = []
    for _, row in default_info.iterrows():
        topic = int(row["Topic"])
        item = {
            "Topic": topic,
            "Count": int(row["Count"]),
            "Name": str(row.get("Name", "")),
            "LLM": "Noise / Outlier" if topic == -1 else llm_lookup.get(topic, ""),
            "KeyBERT": keybert_lookup.get(topic, ""),
            "POS": pos_lookup.get(topic, ""),
            "MMR": mmr_lookup.get(topic, ""),
        }
        rows.append(item)
        rows_with_docs.append({**item, "Original_Sentences": original_lookup.get(topic, "")})

    combined = pd.DataFrame(rows, columns=["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"])
    combined_with_docs = pd.DataFrame(
        rows_with_docs,
        columns=["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR", "Original_Sentences"],
    )
    combined.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_combined_representations.csv", index=False)
    combined_with_docs.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_combined_representations_with_docs.csv", index=False)
    (OUTPUT_DIR / f"{RUN_BASENAME}_combined_representations.md").write_text(
        "\n".join(
            [
                f"# {RUN_BASENAME} Combined Topic Representations",
                "",
                md_table(combined.to_dict("records"), ["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"]),
                "",
            ]
        ),
        encoding="utf-8",
    )
    return combined


def info_preview_rows(info: pd.DataFrame, n: int = 20) -> tuple[list[dict[str, Any]], list[str]]:
    preferred = ["Topic", "Count", "Name", "Representation"]
    columns = [col for col in preferred if col in info.columns]
    return info.head(n)[columns].to_dict("records"), columns


def write_report(
    meta: dict[str, Any],
    embedding_note: str,
    custom_stopwords: list[str],
    metrics: dict[str, Any],
    representation_outputs: dict[str, dict[str, Any]],
    combined_representations: pd.DataFrame,
    llm50_summary: dict[str, Any],
    csv_paths: dict[str, str],
    errors: list[dict[str, str]],
    started_at: str,
    finished_at: str,
) -> None:
    parameter_row = {
        "selection_label": CONFIG["selection_label"],
        "selection_reason": CONFIG["selection_reason"],
        "bertopic_nr_topics": CONFIG["nr_topics"],
        "bertopic_nr_repr_docs": REPRESENTATIVE_DOCS_PER_TOPIC,
        "umap_n_neighbors": CONFIG["umap"]["n_neighbors"],
        "umap_n_components": CONFIG["umap"]["n_components"],
        "umap_min_dist": CONFIG["umap"]["min_dist"],
        "umap_metric": CONFIG["umap"]["metric"],
        "umap_random_state": CONFIG["umap"]["random_state"],
        "hdbscan_min_cluster_size": CONFIG["hdbscan"]["min_cluster_size"],
        "hdbscan_min_samples": CONFIG["hdbscan"]["min_samples"],
        "hdbscan_cluster_selection_method": CONFIG["hdbscan"]["cluster_selection_method"],
        "hdbscan_cluster_selection_epsilon": CONFIG["hdbscan"]["cluster_selection_epsilon"],
        "hdbscan_metric": CONFIG["hdbscan"]["metric"],
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
        "llm_temperature": LLM_TEMPERATURE,
        "llm_max_tokens": LLM_MAX_TOKENS,
        "llm50_runs_per_topic": LLM50_RUNS,
        "representative_docs_per_topic": REPRESENTATIVE_DOCS_PER_TOPIC,
    }
    llm_summary_row = {
        "status": llm50_summary.get("status", ""),
        "topics": llm50_summary.get("topics", 0),
        "calls": llm50_summary.get("calls", 0),
        "stable_topics": llm50_summary.get("stable_topics", 0),
        "error": llm50_summary.get("error", ""),
    }

    report = [
        f"# {RUN_BASENAME}",
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
        "- 使用 A05-8.4(human) 報告統整表格第三欄建議停用詞，並加上 sklearn English stop words。",
        "- stopwords 只作用於 BERTopic c-TF-IDF / topic words 表示；embedding 與 HDBSCAN 分群仍使用原始文本向量。",
        "",
        "## Representation Models",
        "",
        "- default: BERTopic c-TF-IDF",
        "- KeyBERT: KeyBERT-Inspired",
        "- POS: Part-of-Speech",
        "- MMR: Maximal Marginal Relevance",
        f"- LLM: OpenRouter `{LLM_MODEL_NAME}`，temperature=0，max_tokens=64，以每個 topic 50 次抽樣驗證後取眾數 label。",
        "",
        "## LLM50 Validation",
        "",
        md_table([llm_summary_row], list(llm_summary_row.keys())),
        "",
        f"- LLM 測試輸出：`{RUN_BASENAME}_LLM.md`、`{RUN_BASENAME}_LLM.csv`，內含每次輸出的 label 與使用的 Prompt。",
        f"- 驗證統計輸出：`{RUN_BASENAME}_LLM_validation.csv`。",
        "",
        "## Combined Topic Representations",
        "",
        md_table(
            combined_representations.to_dict("records"),
            ["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"],
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
                    "",
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
            "KeyBERT-Inspired、POS、MMR 與 LLM 只更新 topic representation，不改變 UMAP/HDBSCAN topic labels，因此 clustering metrics 相同。",
            "BERTopic `nr_topics='auto'` 會在初始 HDBSCAN 分群後使用 c-TF-IDF 相似度自動合併主題；本報告 metrics 為 reduction 後的 topic labels。",
            "",
        ]
    )
    (OUTPUT_DIR / CONFIG["report_name"]).write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    started_at = datetime.now(timezone.utc).isoformat()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    docs, titles, doc_meta, meta = load_documents()
    custom_stopwords = extract_recommended_stopwords(STOPWORD_MD)
    stopwords = sorted(set(ENGLISH_STOP_WORDS).union(custom_stopwords))
    (OUTPUT_DIR / f"{RUN_BASENAME}_custom_stopwords_used.txt").write_text(
        "\n".join(custom_stopwords) + "\n",
        encoding="utf-8",
    )

    embedding_model, embeddings, embedding_note = get_embeddings(docs)
    vectorizer_model = CountVectorizer(stop_words=stopwords, ngram_range=(1, 2), min_df=2)

    umap_conf = CONFIG["umap"]
    hdbscan_conf = CONFIG["hdbscan"]
    print(f"Training {RUN_BASENAME}...", flush=True)
    topic_model = BERTopicNrReprDocs(
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
        nr_topics=CONFIG["nr_topics"],
        calculate_probabilities=False,
        verbose=False,
    )
    topics, _ = topic_model.fit_transform(docs, embeddings)
    topics = [int(topic) for topic in getattr(topic_model, "topics_", topics)]
    metrics = label_metrics(topics)

    artifacts_dir = OUTPUT_DIR / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    doc_topics = doc_meta.copy()
    doc_topics["title"] = titles
    doc_topics["sentence"] = docs
    doc_topics["topic"] = topics
    doc_topics.to_csv(artifacts_dir / "document_topics.csv", index=False)

    base_info = topic_model.get_topic_info()
    representative_docs = representative_docs_df(topic_model, base_info, docs, topics)
    representative_docs.to_csv(artifacts_dir / "representative_docs.csv", index=False)
    topic_size = base_info[["Topic", "Count", "Name"]].copy()
    topic_size["ratio"] = topic_size["Count"] / len(docs)
    topic_size.to_csv(artifacts_dir / "topic_size_distribution.csv", index=False)

    errors: list[dict[str, str]] = []
    representations: dict[str, Any | None] = {
        "default": None,
        "keybert": KeyBERTInspired(top_n_words=10, nr_repr_docs=REPRESENTATIVE_DOCS_PER_TOPIC, random_state=RANDOM_STATE),
        "pos": PartOfSpeech("en_core_web_sm", top_n_words=10),
        "mmr": MaximalMarginalRelevance(diversity=0.35, top_n_words=10),
    }
    representation_outputs: dict[str, dict[str, Any]] = {}
    for name, representation_model in representations.items():
        print(f"  representation: {name}", flush=True)
        representation_outputs[name] = export_representation(
            topic_model,
            docs,
            topics,
            artifacts_dir,
            name,
            representation_model,
            custom_stopwords,
            errors,
        )

    default_words = representation_outputs.get("default", {}).get("words")
    llm50_summary: dict[str, Any] = {"status": "not_run", "topics": 0, "calls": 0, "stable_topics": 0}
    if isinstance(default_words, pd.DataFrame):
        print("  LLM50 validation: openai/gpt-5.5", flush=True)
        llm50_summary = run_llm50_validation(default_words, representative_docs, errors)

    llm_validation_path = OUTPUT_DIR / f"{RUN_BASENAME}_LLM_validation.csv"
    llm_validation_df = pd.read_csv(llm_validation_path) if llm_validation_path.exists() else None
    combined_representations = build_combined_representation_table(
        representation_outputs,
        representative_docs,
        llm_validation_df,
    )

    (artifacts_dir / "representation_errors.json").write_text(
        json.dumps(errors, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    final_config = {
        **CONFIG,
        "metrics": metrics,
        "dataset": str(DATASET_DIR.relative_to(ROOT)),
        "embedding_model": EMBEDDING_MODEL_NAME,
        "embedding_note": embedding_note,
        "custom_stopwords_count": len(custom_stopwords),
        "stopword_source": str(STOPWORD_MD.relative_to(ROOT)),
        "total_stopword_count_with_english": len(stopwords),
        "representation_models": list(representations.keys()),
        "llm_provider": "OpenRouter",
        "llm_model": LLM_MODEL_NAME,
        "llm_temperature": LLM_TEMPERATURE,
        "llm_max_tokens": LLM_MAX_TOKENS,
        "llm50_runs_per_topic": LLM50_RUNS,
        "llm50_summary": llm50_summary,
        "representative_docs_per_topic": REPRESENTATIVE_DOCS_PER_TOPIC,
    }
    (artifacts_dir / "final_config.json").write_text(json.dumps(final_config, ensure_ascii=False, indent=2), encoding="utf-8")

    csv_paths = {
        "main_report": f"{RUN_BASENAME}.md",
        "topic_info_default": "artifacts/topic_info_default.csv",
        "topic_words_default": "artifacts/topic_words_default.csv",
        "topic_info_keybert": "artifacts/topic_info_keybert.csv",
        "topic_words_keybert": "artifacts/topic_words_keybert.csv",
        "topic_info_pos": "artifacts/topic_info_pos.csv",
        "topic_words_pos": "artifacts/topic_words_pos.csv",
        "topic_info_mmr": "artifacts/topic_info_mmr.csv",
        "topic_words_mmr": "artifacts/topic_words_mmr.csv",
        "document_topics": "artifacts/document_topics.csv",
        "representative_docs": "artifacts/representative_docs.csv",
        "topic_size_distribution": "artifacts/topic_size_distribution.csv",
        "combined_representations_csv": f"{RUN_BASENAME}_combined_representations.csv",
        "combined_representations_md": f"{RUN_BASENAME}_combined_representations.md",
        "combined_representations_with_docs_csv": f"{RUN_BASENAME}_combined_representations_with_docs.csv",
        "llm_result_md": f"{RUN_BASENAME}_LLM.md",
        "llm_result_csv": f"{RUN_BASENAME}_LLM.csv",
        "llm_prompts_csv": f"{RUN_BASENAME}_LLM_prompts.csv",
        "llm_validation_csv": f"{RUN_BASENAME}_LLM_validation.csv",
        "llm_detail_csv": f"{RUN_BASENAME}_LLM_detail.csv",
        "final_config": "artifacts/final_config.json",
        "representation_errors": "artifacts/representation_errors.json",
        "custom_stopwords_used": f"{RUN_BASENAME}_custom_stopwords_used.txt",
    }
    finished_at = datetime.now(timezone.utc).isoformat()
    write_report(
        meta,
        embedding_note,
        custom_stopwords,
        metrics,
        representation_outputs,
        combined_representations,
        llm50_summary,
        csv_paths,
        errors,
        started_at,
        finished_at,
    )
    summary = {
        "finished_at": finished_at,
        "dataset": str(DATASET_DIR.relative_to(ROOT)),
        "output_dir": str(OUTPUT_DIR.relative_to(ROOT)),
        "rows": len(docs),
        "metrics": metrics,
        "llm50_summary": llm50_summary,
        "representation_errors": len(errors),
    }
    pd.DataFrame([summary | metrics | {f"llm50_{k}": v for k, v in llm50_summary.items() if not isinstance(v, dict)}]).to_csv(
        OUTPUT_DIR / f"{RUN_BASENAME}_summary.csv",
        index=False,
    )
    (OUTPUT_DIR / f"{RUN_BASENAME}_run_log.json").write_text(
        json.dumps(
            {
                **summary,
                "stopword_md": str(STOPWORD_MD.relative_to(ROOT)),
                "custom_stopword_count": len(custom_stopwords),
                "total_stopword_count_with_english": len(stopwords),
                "embedding_note": embedding_note,
                "parameters": CONFIG,
                "representation_models": list(representations.keys()),
                "llm_model": LLM_MODEL_NAME,
                "llm_temperature": LLM_TEMPERATURE,
                "llm_max_tokens": LLM_MAX_TOKENS,
                "errors": errors,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
