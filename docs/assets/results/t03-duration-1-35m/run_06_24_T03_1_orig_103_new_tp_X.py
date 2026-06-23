from __future__ import annotations

"""BERTopic run for validation set 2 (orig, 103 files).

LLM topic naming is deliberately disabled for this run.  The companion LLM
files document that decision so downstream review does not mistake an empty
LLM column for a failed request.
"""

import json
import re
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

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
DATASET_DIR = ROOT / "#運行BERTopic整理/#2.1 清理後輸入資料集（dataset）/02.1-驗證集2 1-35 分鐘_(103)/R06.03_A02-pre_LLM(orig)-(103)_tok(para12-80)_dataset"
STOPWORD_MD = ROOT / "Result/06.05_A05_stopword/A05-8(orig)REV_tok(para12-80)/A05-8.4(human)_stopword.md"
OUTPUT_DIR = Path(__file__).resolve().parent
RUN_BASENAME = OUTPUT_DIR.name
TEXT_COL = "sentence"
RANDOM_STATE = 42
NR_REPR_DOCS = 6
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

CONFIG = {
    "nr_topics": "auto",
    "umap_n_neighbors": 10,
    "umap_n_components": 15,
    "umap_min_dist": 0.0,
    "hdbscan_min_cluster_size": 50,
    "hdbscan_min_samples": 5,
    "hdbscan_cluster_selection_method": "eom",
    "hdbscan_cluster_selection_epsilon": 0.2,
    "nr_repr_docs": NR_REPR_DOCS,
    "llm_topic_naming": "disabled",
}


class BERTopicWithReprDocs(BERTopic):
    def _extract_representative_docs(
        self, c_tf_idf, documents: pd.DataFrame, topics: Mapping[str, list[tuple[str, float]]],
        nr_samples: int = 500, nr_repr_docs: int = NR_REPR_DOCS, diversity: float | None = None,
    ):
        return super()._extract_representative_docs(
            c_tf_idf, documents, topics, nr_samples=nr_samples,
            nr_repr_docs=nr_repr_docs, diversity=diversity,
        )


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        vals = []
        for col in columns:
            value = row.get(col, "")
            value = "" if value is None else str(value)
            vals.append(value.replace("|", "\\|").replace("\n", "<br>"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def extract_stopwords(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    words: set[str] = set()
    for line in text.splitlines():
        if not line.startswith("| ") or line.startswith("| ---") or "停用詞類型" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        for item in cells[2].split(","):
            term = item.strip().strip("`").lower()
            if term:
                words.add(term)
                words.update(re.findall(r"(?u)\b\w\w+\b", term))
    if not words:
        raise RuntimeError(f"No recommended stopwords found in {path}")
    return sorted(words)


def load_docs() -> tuple[list[str], pd.DataFrame]:
    dataset = load_from_disk(str(DATASET_DIR))
    if TEXT_COL not in dataset.column_names:
        raise ValueError(f"Missing {TEXT_COL!r}; available: {dataset.column_names}")
    rows = []
    for idx, item in enumerate(dataset):
        text = str(item.get(TEXT_COL) or "").strip()
        if text:
            rows.append({**{key: item.get(key) for key in dataset.column_names}, "dataset_row": idx, "document": text})
    frame = pd.DataFrame(rows)
    return frame["document"].tolist(), frame


def topic_words(model: BERTopic, info: pd.DataFrame, representation: str) -> pd.DataFrame:
    rows = []
    for topic in info["Topic"].astype(int):
        terms = model.get_topic(topic) or []
        rows.append({
            "representation_model": representation,
            "topic": topic,
            "words": ", ".join(str(word) for word, _ in terms),
            "weighted_words": json.dumps([(str(word), float(weight)) for word, weight in terms], ensure_ascii=False),
        })
    return pd.DataFrame(rows)


def representative_docs(model: BERTopic, info: pd.DataFrame, docs: list[str], topics: list[int]) -> pd.DataFrame:
    by_topic: dict[int, list[str]] = {}
    for doc, topic in zip(docs, topics, strict=True):
        by_topic.setdefault(topic, []).append(doc)
    rows = []
    for topic in info["Topic"].astype(int):
        picked = list(model.get_representative_docs(topic) or [])
        seen = set(picked)
        for doc in by_topic.get(topic, []):
            if len(picked) >= NR_REPR_DOCS:
                break
            if doc not in seen:
                picked.append(doc)
                seen.add(doc)
        rows.extend({"topic": topic, "rank": rank, "representative_text": text}
                    for rank, text in enumerate(picked[:NR_REPR_DOCS], 1))
    return pd.DataFrame(rows)


def export_representation(model: BERTopic, docs: list[str], topics: list[int], name: str, representation: Any | None,
                          custom_stopwords: set[str], artifacts: Path, errors: list[dict[str, str]]) -> dict[str, Any]:
    try:
        if representation is not None:
            model.update_topics(docs, topics=topics, representation_model=representation, top_n_words=10)
        for topic, terms in model.topic_representations_.items():
            kept = [(str(term), float(weight)) for term, weight in terms if str(term).lower() not in custom_stopwords]
            model.topic_representations_[topic] = kept or [("filtered_topic_terms_unavailable", 0.0)]
        info = model.get_topic_info()
        words = topic_words(model, info, name)
        info.to_csv(artifacts / f"topic_info_{name}.csv", index=False)
        words.to_csv(artifacts / f"topic_words_{name}.csv", index=False)
        return {"info": info, "words": words, "status": "ok"}
    except Exception as exc:
        errors.append({"representation": name, "error": str(exc), "traceback": traceback.format_exc()})
        return {"info": None, "words": None, "status": "failed"}


def words_by_topic(payload: dict[str, Any]) -> dict[int, str]:
    words = payload.get("words")
    if not isinstance(words, pd.DataFrame):
        return {}
    return {int(row.topic): str(row.words) for row in words.itertuples(index=False)}


def make_combined(outputs: dict[str, dict[str, Any]], reps: pd.DataFrame) -> pd.DataFrame:
    info = outputs["default"]["info"]
    if not isinstance(info, pd.DataFrame):
        return pd.DataFrame(columns=["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"])
    lookups = {name: words_by_topic(outputs.get(name, {})) for name in ("keybert", "pos", "mmr")}
    rows = []
    rows_with_docs = []
    for row in info.itertuples(index=False):
        topic = int(row.Topic)
        item = {
            "Topic": topic, "Count": int(row.Count), "Name": str(row.Name),
            "LLM": "未使用（本次停用 LLM 主題命名）",
            "KeyBERT": lookups["keybert"].get(topic, ""),
            "POS": lookups["pos"].get(topic, ""),
            "MMR": lookups["mmr"].get(topic, ""),
        }
        rows.append(item)
        selected = reps.loc[reps["topic"] == topic].sort_values("rank")["representative_text"].tolist()
        rows_with_docs.append({**item, "Original_Sentences": " || ".join(selected)})
    combined = pd.DataFrame(rows)
    combined.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_combined_representations.csv", index=False)
    pd.DataFrame(rows_with_docs).to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_combined_representations_with_docs.csv", index=False)
    return combined


def main() -> None:
    started_at = datetime.now(timezone.utc).isoformat()
    artifacts = OUTPUT_DIR / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    docs, document_frame = load_docs()
    custom_stopwords = extract_stopwords(STOPWORD_MD)
    (OUTPUT_DIR / f"{RUN_BASENAME}_custom_stopwords_used.txt").write_text("\n".join(custom_stopwords) + "\n", encoding="utf-8")
    vectorizer = CountVectorizer(stop_words=sorted(set(ENGLISH_STOP_WORDS) | set(custom_stopwords)), ngram_range=(1, 2), min_df=2)

    print(f"Encoding {len(docs)} documents with {EMBEDDING_MODEL_NAME}...", flush=True)
    encoder = SentenceTransformer(EMBEDDING_MODEL_NAME)
    embeddings = encoder.encode(docs, batch_size=64, show_progress_bar=True, convert_to_numpy=True)
    np.save(OUTPUT_DIR / f"embeddings_{EMBEDDING_MODEL_NAME}.npy", embeddings)
    print("Fitting BERTopic...", flush=True)
    model = BERTopicWithReprDocs(
        embedding_model=encoder,
        umap_model=UMAP(n_neighbors=10, n_components=15, min_dist=0.0, metric="cosine", random_state=RANDOM_STATE, low_memory=True),
        hdbscan_model=HDBSCAN(min_cluster_size=50, min_samples=5, metric="euclidean", cluster_selection_method="eom", cluster_selection_epsilon=0.2, prediction_data=True, core_dist_n_jobs=-1),
        vectorizer_model=vectorizer, nr_topics="auto", top_n_words=10, calculate_probabilities=False, verbose=False,
    )
    raw_topics, _ = model.fit_transform(docs, embeddings)
    topics = [int(topic) for topic in model.topics_]
    document_frame["topic"] = topics
    document_frame.to_csv(artifacts / "document_topics.csv", index=False)
    base_info = model.get_topic_info()
    reps = representative_docs(model, base_info, docs, topics)
    reps.to_csv(artifacts / "representative_docs.csv", index=False)
    base_info[["Topic", "Count", "Name"]].to_csv(artifacts / "topic_size_distribution.csv", index=False)

    errors: list[dict[str, str]] = []
    models = {
        "default": None,
        "keybert": KeyBERTInspired(top_n_words=10, nr_repr_docs=NR_REPR_DOCS, random_state=RANDOM_STATE),
        "pos": PartOfSpeech("en_core_web_sm", top_n_words=10),
        "mmr": MaximalMarginalRelevance(diversity=0.35, top_n_words=10),
    }
    outputs = {}
    for name, representation in models.items():
        print(f"Exporting {name} representation...", flush=True)
        outputs[name] = export_representation(model, docs, topics, name, representation, set(custom_stopwords), artifacts, errors)
    combined = make_combined(outputs, reps)
    combined.to_markdown(OUTPUT_DIR / f"{RUN_BASENAME}_combined_representations.md", index=False)

    # Requested companion outputs, explicitly documenting disabled LLM naming.
    llm_df = pd.DataFrame([{
        "status": "disabled", "reason": "User requested no LLM topic naming for this run.",
        "prompt": "Not applicable: LLM topic naming was disabled by run configuration.",
    }])
    llm_df.to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_LLM.csv", index=False)
    (OUTPUT_DIR / f"{RUN_BASENAME}_LLM.md").write_text(
        f"# {RUN_BASENAME} LLM\n\n| status | reason | Prompt |\n| --- | --- | --- |\n| disabled | User requested no LLM topic naming for this run. | Not applicable: LLM topic naming was disabled by run configuration. |\n",
        encoding="utf-8",
    )
    counts = Counter(topics)
    metrics = {"documents": len(docs), "topics_excluding_noise": len([t for t in counts if t != -1]), "noise_documents": counts.get(-1, 0), "noise_ratio": round(counts.get(-1, 0) / len(docs), 6)}
    finished_at = datetime.now(timezone.utc).isoformat()
    report = [
        f"# {RUN_BASENAME}", "", "## Run Settings", "",
        markdown_table([{**CONFIG, "dataset": str(DATASET_DIR.relative_to(ROOT)), "stopword_source": str(STOPWORD_MD.relative_to(ROOT)), "started_at": started_at, "finished_at": finished_at}], [*CONFIG.keys(), "dataset", "stopword_source", "started_at", "finished_at"]),
        "", "## Metrics", "", markdown_table([metrics], list(metrics)),
        "", "## Topic Representations", "",
        markdown_table(combined.to_dict("records"), ["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"]),
        "", "## Notes", "", "- 已套用 A05-8.4(human) 建議停用詞與 sklearn English stop words。",
        "- `nr_topics=auto` 已以 c-TF-IDF reduction 自動縮減主題。",
        "- LLM 主題命名依本次指示停用；`_LLM.md` 與 `_LLM.csv` 僅記錄此設定，沒有模型輸出或實際 Prompt。",
        "", "## Representation Errors", "", "無" if not errors else "```json\n" + json.dumps(errors, ensure_ascii=False, indent=2) + "\n```", "",
    ]
    (OUTPUT_DIR / f"{RUN_BASENAME}.md").write_text("\n".join(report), encoding="utf-8")
    (artifacts / "final_config.json").write_text(json.dumps({**CONFIG, "metrics": metrics, "errors": errors}, ensure_ascii=False, indent=2), encoding="utf-8")
    (artifacts / "representation_errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Completed: {OUTPUT_DIR}", flush=True)


if __name__ == "__main__":
    main()
