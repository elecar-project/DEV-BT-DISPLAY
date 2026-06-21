from __future__ import annotations

import hashlib
import json
import math
import re
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance, PartOfSpeech
from datasets import load_from_disk
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from umap import UMAP


ROOT = Path(__file__).resolve().parents[3]
RUN_BASENAME = "06.17_T02-2(orig_18-25_tp-X)"
OUTPUT_DIR = ROOT / "Result/06.17_T02_year" / RUN_BASENAME
ARTIFACT_DIR = OUTPUT_DIR / "artifacts"
DATASET_DIR = ROOT / "Result/06.13_[B]tok/06.13_[B]02-pre_LLM(orig)_18-25(257)_tok(para12-80)_dataset"
STOPWORD_MD = ROOT / "Result/06.05_A05_stopword/A05-8(orig)REV_tok(para12-80)/A05-8.4(human)_stopword.md"

TEXT_COL = "sentence"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDINGS_PATH = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.npy"
EMBEDDINGS_META_PATH = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.meta.json"
REPRESENTATIVE_DOCS_PER_TOPIC = 6
TOP_N_WORDS = 10

CONFIG = {
    "selection_label": RUN_BASENAME,
    "selection_reason": "User-specified single BERTopic run with c-TF-IDF topic reduction.",
    "umap": {
        "n_neighbors": 5,
        "n_components": 10,
        "min_dist": 0.0,
        "metric": "cosine",
        "random_state": 42,
    },
    "hdbscan": {
        "min_cluster_size": 100,
        "min_samples": 5,
        "metric": "euclidean",
        "cluster_selection_method": "eom",
        "cluster_selection_epsilon": 0.0,
    },
    "nr_topics": "auto",
    "representation_models": {
        "KeyBERT": "KeyBERTInspired(top_n_words=10, nr_repr_docs=6, random_state=42)",
        "POS": "PartOfSpeech('en_core_web_sm', top_n_words=10)",
        "MMR": "MaximalMarginalRelevance(diversity=0.3, top_n_words=10)",
    },
    "llm_topic_naming": "disabled",
}

LLM_PROMPT_STATUS = "LLM topic naming disabled by user request; no prompt was submitted."
LLM_PROMPT_TEMPLATE = """[NOT SENT]
System:
You label BERTopic topics for an electric vehicle research corpus. Return one concise English topic label, 2 to 6 words. Prefer EV meaning when present. Do not explain.

User:
Topic ID: {topic_id}
Keywords: {keywords}
Representative snippets:
{representative_snippets}

Topic label:
"""


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values: list[str] = []
        for col in columns:
            value = row.get(col, "")
            if isinstance(value, float):
                text = f"{value:.4f}"
            elif value is None:
                text = ""
            else:
                text = str(value)
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
    source_rows: list[Any] = []
    paragraph_ids: list[Any] = []
    for item in dataset:
        text = "" if item.get(TEXT_COL) is None else str(item.get(TEXT_COL)).strip()
        if not text:
            continue
        docs.append(text)
        titles.append(str(item.get("title", "")))
        source_rows.append(item.get("source_row", ""))
        paragraph_ids.append(item.get("paragraph_id", ""))

    lengths = [len(doc) for doc in docs]
    word_counts = [len(doc.split()) for doc in docs]
    meta = {
        "dataset": str(DATASET_DIR.relative_to(ROOT)),
        "source_rows": len(dataset),
        "used_rows": len(docs),
        "text_col": TEXT_COL,
        "title_col": "title",
        "embedding_model": EMBEDDING_MODEL_NAME,
        "stopword_source": str(STOPWORD_MD.relative_to(ROOT)),
        "min_text_len": min(lengths),
        "max_text_len": max(lengths),
        "avg_text_len": float(np.mean(lengths)),
        "min_word_count": min(word_counts),
        "max_word_count": max(word_counts),
        "avg_word_count": float(np.mean(word_counts)),
        "source_row_count": len(set(source_rows)),
        "paragraph_count": len(set(paragraph_ids)),
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
        raise ValueError(f"Could not extract stopwords from {path}")
    return sorted(words)


def get_embeddings(docs: list[str]) -> tuple[SentenceTransformer, np.ndarray, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    current_meta = {
        "model": EMBEDDING_MODEL_NAME,
        "doc_count": len(docs),
        "docs_hash": docs_hash(docs),
    }
    if EMBEDDINGS_PATH.exists() and EMBEDDINGS_META_PATH.exists():
        old_meta = json.loads(EMBEDDINGS_META_PATH.read_text(encoding="utf-8"))
        if old_meta == current_meta:
            return model, np.load(EMBEDDINGS_PATH), "Reused existing embeddings cache from this output folder."

    embeddings = model.encode(docs, show_progress_bar=True, batch_size=64, convert_to_numpy=True)
    np.save(EMBEDDINGS_PATH, embeddings)
    EMBEDDINGS_META_PATH.write_text(json.dumps(current_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return model, embeddings, "Computed embeddings and saved cache in this output folder."


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
        "n_topics_without_noise": int(n_clusters),
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


def normalize_term(term: Any) -> str:
    return re.sub(r"\s+", " ", str(term).strip().lower())


def filter_topic_representations(topic_model: BERTopic, stopwords: set[str]) -> None:
    for topic, words in list(topic_model.topic_representations_.items()):
        filtered = []
        for word, weight in words:
            normalized = normalize_term(word)
            tokens = re.findall(r"(?u)\b\w\w+\b", normalized)
            if normalized in stopwords:
                continue
            if tokens and all(token in stopwords for token in tokens):
                continue
            filtered.append((str(word), float(weight)))
        if not filtered:
            filtered = [("filtered_topic_terms_unavailable", 0.0)]
        topic_model.topic_representations_[topic] = filtered


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


def export_representation(
    topic_model: BERTopic,
    docs: list[str],
    topics: list[int],
    name: str,
    representation_model: Any | None,
    all_stopwords: set[str],
    errors: list[dict[str, str]],
) -> dict[str, Any]:
    try:
        if representation_model is not None:
            topic_model.update_topics(
                docs,
                topics=topics,
                representation_model=representation_model,
                top_n_words=TOP_N_WORDS,
            )
        filter_topic_representations(topic_model, all_stopwords)
        info = topic_model.get_topic_info()
        words = topic_words_df(topic_model, info, name)
        safe_name = name.lower()
        info.to_csv(ARTIFACT_DIR / f"topic_info_{safe_name}.csv", index=False)
        words.to_csv(ARTIFACT_DIR / f"topic_words_{safe_name}.csv", index=False)
        if name == "default":
            info.to_csv(ARTIFACT_DIR / "topic_info.csv", index=False)
            words.to_csv(ARTIFACT_DIR / "topic_words.csv", index=False)
        return {"status": "ok", "info": info, "words": words}
    except Exception as exc:
        errors.append({"representation_model": name, "error": str(exc), "traceback": traceback.format_exc()})
        return {"status": "failed", "info": None, "words": None}


def words_lookup(payload: dict[str, Any]) -> dict[int, str]:
    words = payload.get("words")
    if not isinstance(words, pd.DataFrame) or "topic" not in words.columns or "words" not in words.columns:
        return {}
    return {int(row["topic"]): str(row.get("words", "")) for _, row in words.iterrows()}


def build_combined_table(
    representation_outputs: dict[str, dict[str, Any]],
    representative_docs: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    default_info = representation_outputs.get("default", {}).get("info")
    if not isinstance(default_info, pd.DataFrame):
        columns = ["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"]
        return pd.DataFrame(columns=columns), pd.DataFrame(columns=[*columns, "Original_Sentences"])

    keybert_lookup = words_lookup(representation_outputs.get("KeyBERT", {}))
    pos_lookup = words_lookup(representation_outputs.get("POS", {}))
    mmr_lookup = words_lookup(representation_outputs.get("MMR", {}))
    if representative_docs.empty:
        docs_lookup: dict[int, str] = {}
    else:
        docs_lookup = {
            int(topic): " || ".join(group.sort_values("rank")["representative_text"].astype(str).tolist())
            for topic, group in representative_docs.groupby("topic")
        }

    rows = []
    rows_with_docs = []
    for _, row in default_info.iterrows():
        topic = int(row["Topic"])
        item = {
            "Topic": topic,
            "Count": int(row["Count"]),
            "Name": str(row.get("Name", "")),
            "LLM": "Noise / Outlier" if topic == -1 else "",
            "KeyBERT": keybert_lookup.get(topic, ""),
            "POS": pos_lookup.get(topic, ""),
            "MMR": mmr_lookup.get(topic, ""),
        }
        rows.append(item)
        rows_with_docs.append({**item, "Original_Sentences": docs_lookup.get(topic, "")})

    columns = ["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"]
    combined = pd.DataFrame(rows, columns=columns)
    combined_with_docs = pd.DataFrame(rows_with_docs, columns=[*columns, "Original_Sentences"])
    return combined, combined_with_docs


def prompt_preview(topic: int, keywords: str, representative_docs: pd.DataFrame) -> str:
    snippets: list[str] = []
    if not representative_docs.empty:
        snippets = (
            representative_docs.loc[representative_docs["topic"] == topic]
            .sort_values("rank")["representative_text"]
            .astype(str)
            .head(REPRESENTATIVE_DOCS_PER_TOPIC)
            .tolist()
        )
    snippet_text = "\n".join(f"- {snippet[:420]}" for snippet in snippets)
    return LLM_PROMPT_TEMPLATE.format(
        topic_id=topic,
        keywords=keywords,
        representative_snippets=snippet_text,
    )


def write_llm_files(combined: pd.DataFrame, representative_docs: pd.DataFrame) -> None:
    llm_rows = []
    for _, row in combined.iterrows():
        topic = int(row["Topic"])
        keywords = str(row.get("Name", ""))
        llm_rows.append(
            {
                **row.to_dict(),
                "LLM_Status": "not_used",
                "LLM_Model": "not_used",
                "Prompt_Status": LLM_PROMPT_STATUS,
                "Prompt": prompt_preview(topic, keywords, representative_docs),
            }
        )
    llm_df = pd.DataFrame(llm_rows)
    llm_df.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_LLM.csv", index=False)

    report = [
        f"# {RUN_BASENAME} LLM Topic Results",
        "",
        "- LLM topic naming: `not_used`",
        f"- prompt status: {LLM_PROMPT_STATUS}",
        f"- representative docs per topic prepared for prompt preview: {REPRESENTATIVE_DOCS_PER_TOPIC}",
        "",
        "## Combined Topic Representations",
        "",
        md_table(combined.to_dict("records"), ["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"])
        if not combined.empty
        else "無",
        "",
        "## Prompt",
        "",
        "```text",
        LLM_PROMPT_TEMPLATE.strip(),
        "```",
        "",
        "## Notes",
        "",
        "No LLM request was sent. The CSV includes a per-topic prompt preview column only for traceability.",
        "",
    ]
    (OUTPUT_DIR / f"{RUN_BASENAME}_LLM.md").write_text("\n".join(report), encoding="utf-8")


def write_report(
    meta: dict[str, Any],
    embedding_note: str,
    custom_stopwords: list[str],
    total_stopword_count: int,
    metrics: dict[str, Any],
    representation_outputs: dict[str, dict[str, Any]],
    combined: pd.DataFrame,
    errors: list[dict[str, str]],
    started_at: str,
    finished_at: str,
) -> None:
    run_row = {
        "started_at": started_at,
        "finished_at": finished_at,
        "dataset": meta["dataset"],
        "embedding_model": EMBEDDING_MODEL_NAME,
        "embedding_note": embedding_note,
        "custom_stopword_count": len(custom_stopwords),
        "total_stopword_count_with_sklearn_english": total_stopword_count,
        "representative_docs_per_topic": REPRESENTATIVE_DOCS_PER_TOPIC,
        "llm_topic_naming": "not_used",
    }
    parameter_row = {
        "bertopic_nr_topics": CONFIG["nr_topics"],
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
    output_row = {
        "main_report": f"{RUN_BASENAME}.md",
        "llm_report": f"{RUN_BASENAME}_LLM.md",
        "llm_csv": f"{RUN_BASENAME}_LLM.csv",
        "combined_csv": f"{RUN_BASENAME}_combined_representations.csv",
        "combined_with_docs_csv": f"{RUN_BASENAME}_combined_representations_with_docs.csv",
        "document_topics": "artifacts/document_topics.csv",
        "representative_docs": "artifacts/representative_docs.csv",
        "final_config": "artifacts/final_config.json",
    }

    report = [
        f"# {RUN_BASENAME} BERTopic Result",
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
        md_table([metrics], list(metrics.keys())),
        "",
        "## Stopword Setting",
        "",
        f"- stopword source: `{STOPWORD_MD.relative_to(ROOT)}`",
        "- Used the recommended stopwords extracted from the markdown table.",
        "- Added sklearn English stop words for CountVectorizer and representation filtering.",
        "- Stopwords affect c-TF-IDF/topic-word representations; embeddings and HDBSCAN clustering use the original sentence texts.",
        "",
        "## Representation Models",
        "",
        "- KeyBERT: KeyBERT-Inspired, `nr_repr_docs=6`",
        "- POS: Part-of-Speech using `en_core_web_sm`",
        "- MMR: Maximal Marginal Relevance, `diversity=0.3`",
        "- LLM: not used",
        "",
        "## Combined Topic Representations",
        "",
        md_table(combined.to_dict("records"), ["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"])
        if not combined.empty
        else "無",
        "",
    ]
    for name, payload in representation_outputs.items():
        report.extend([f"### {name}", "", f"- status: `{payload.get('status', 'unknown')}`"])
        info = payload.get("info")
        words = payload.get("words")
        if isinstance(info, pd.DataFrame) and isinstance(words, pd.DataFrame):
            info_cols = [col for col in ["Topic", "Count", "Name", "Representation"] if col in info.columns]
            report.extend(
                [
                    "",
                    "#### Topic Info Top 20",
                    "",
                    md_table(info.head(20)[info_cols].to_dict("records"), info_cols),
                    "",
                    "#### Topic Words Top 20",
                    "",
                    md_table(words.head(20).to_dict("records"), ["topic", "words"]),
                    "",
                ]
            )
    report.extend(
        [
            "## Output Files",
            "",
            md_table([output_row], list(output_row.keys())),
            "",
            "## Representation Errors",
            "",
            "無" if not errors else "```json\n" + json.dumps(errors, ensure_ascii=False, indent=2) + "\n```",
            "",
            "## Notes",
            "",
            "BERTopic `nr_topics='auto'` applies c-TF-IDF based topic reduction after the initial HDBSCAN clustering.",
            "Representation models update topic words only; they do not change document-topic assignments.",
            "",
        ]
    )
    (OUTPUT_DIR / f"{RUN_BASENAME}.md").write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now(timezone.utc).isoformat()

    docs, titles, meta = load_documents()
    custom_stopwords = extract_recommended_stopwords(STOPWORD_MD)
    all_stopwords = set(custom_stopwords).union(str(word).lower() for word in ENGLISH_STOP_WORDS)
    (OUTPUT_DIR / f"{RUN_BASENAME}_custom_stopwords_used.txt").write_text(
        "\n".join(custom_stopwords) + "\n",
        encoding="utf-8",
    )

    embedding_model, embeddings, embedding_note = get_embeddings(docs)
    vectorizer_model = CountVectorizer(
        stop_words=sorted(all_stopwords),
        ngram_range=(1, 2),
        min_df=2,
    )

    print(f"Training {RUN_BASENAME} with {len(docs)} documents...", flush=True)
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=UMAP(
            n_neighbors=CONFIG["umap"]["n_neighbors"],
            n_components=CONFIG["umap"]["n_components"],
            min_dist=CONFIG["umap"]["min_dist"],
            metric=CONFIG["umap"]["metric"],
            random_state=CONFIG["umap"]["random_state"],
            low_memory=True,
        ),
        hdbscan_model=HDBSCAN(
            min_cluster_size=CONFIG["hdbscan"]["min_cluster_size"],
            min_samples=CONFIG["hdbscan"]["min_samples"],
            metric=CONFIG["hdbscan"]["metric"],
            cluster_selection_method=CONFIG["hdbscan"]["cluster_selection_method"],
            cluster_selection_epsilon=CONFIG["hdbscan"]["cluster_selection_epsilon"],
            prediction_data=True,
            core_dist_n_jobs=-1,
        ),
        vectorizer_model=vectorizer_model,
        top_n_words=TOP_N_WORDS,
        nr_topics=CONFIG["nr_topics"],
        calculate_probabilities=False,
        verbose=False,
    )
    topics, _ = topic_model.fit_transform(docs, embeddings)
    topics = [int(topic) for topic in getattr(topic_model, "topics_", topics)]
    metrics = label_metrics(topics)

    pd.DataFrame({"title": titles, "sentence": docs, "topic": topics}).to_csv(
        ARTIFACT_DIR / "document_topics.csv",
        index=False,
    )
    base_info = topic_model.get_topic_info()
    representative_docs = representative_docs_df(topic_model, base_info, docs, topics)
    representative_docs.to_csv(ARTIFACT_DIR / "representative_docs.csv", index=False)
    topic_size = base_info[["Topic", "Count", "Name"]].copy()
    topic_size["ratio"] = topic_size["Count"] / len(docs)
    topic_size.to_csv(ARTIFACT_DIR / "topic_size_distribution.csv", index=False)

    errors: list[dict[str, str]] = []
    representations: dict[str, Any | None] = {
        "default": None,
        "KeyBERT": KeyBERTInspired(
            top_n_words=TOP_N_WORDS,
            nr_repr_docs=REPRESENTATIVE_DOCS_PER_TOPIC,
            random_state=42,
        ),
        "POS": PartOfSpeech("en_core_web_sm", top_n_words=TOP_N_WORDS),
        "MMR": MaximalMarginalRelevance(diversity=0.3, top_n_words=TOP_N_WORDS),
    }

    representation_outputs: dict[str, dict[str, Any]] = {}
    for name, representation_model in representations.items():
        print(f"  representation: {name}", flush=True)
        representation_outputs[name] = export_representation(
            topic_model,
            docs,
            topics,
            name,
            representation_model,
            all_stopwords,
            errors,
        )

    combined, combined_with_docs = build_combined_table(representation_outputs, representative_docs)
    combined.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_combined_representations.csv", index=False)
    combined_with_docs.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_combined_representations_with_docs.csv", index=False)
    (OUTPUT_DIR / f"{RUN_BASENAME}_combined_representations.md").write_text(
        "\n".join(
            [
                f"# {RUN_BASENAME} Combined Topic Representations",
                "",
                md_table(
                    combined.to_dict("records"),
                    ["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"],
                ),
                "",
            ]
        ),
        encoding="utf-8",
    )
    write_llm_files(combined, representative_docs)

    final_config = {
        **CONFIG,
        "dataset": str(DATASET_DIR.relative_to(ROOT)),
        "output_dir": str(OUTPUT_DIR.relative_to(ROOT)),
        "embedding_model": EMBEDDING_MODEL_NAME,
        "embedding_note": embedding_note,
        "custom_stopword_count": len(custom_stopwords),
        "total_stopword_count_with_sklearn_english": len(all_stopwords),
        "stopword_source": str(STOPWORD_MD.relative_to(ROOT)),
        "metrics": metrics,
        "representative_docs_per_topic": REPRESENTATIVE_DOCS_PER_TOPIC,
        "llm_prompt_status": LLM_PROMPT_STATUS,
        "llm_prompt_template": LLM_PROMPT_TEMPLATE,
    }
    (ARTIFACT_DIR / "final_config.json").write_text(json.dumps(final_config, ensure_ascii=False, indent=2), encoding="utf-8")
    (ARTIFACT_DIR / "representation_errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")

    finished_at = datetime.now(timezone.utc).isoformat()
    write_report(
        meta,
        embedding_note,
        custom_stopwords,
        len(all_stopwords),
        metrics,
        representation_outputs,
        combined,
        errors,
        started_at,
        finished_at,
    )
    pd.DataFrame([{**metrics, "report": f"{RUN_BASENAME}.md", "llm_topic_naming": "not_used"}]).to_csv(
        OUTPUT_DIR / f"{RUN_BASENAME}_summary.csv",
        index=False,
    )
    (OUTPUT_DIR / f"{RUN_BASENAME}_run_log.json").write_text(
        json.dumps(
            {
                "started_at": started_at,
                "finished_at": finished_at,
                "dataset": str(DATASET_DIR.relative_to(ROOT)),
                "output_dir": str(OUTPUT_DIR.relative_to(ROOT)),
                "rows": len(docs),
                "config": CONFIG,
                "metrics": metrics,
                "embedding_note": embedding_note,
                "errors": errors,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Done. Output: {OUTPUT_DIR.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
