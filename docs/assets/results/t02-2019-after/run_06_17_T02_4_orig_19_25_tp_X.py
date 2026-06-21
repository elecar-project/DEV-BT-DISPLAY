from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_SCRIPT = (
    ROOT
    / "Result/06.17_T02_year/06.17_T02-2(orig_18-25_tp-X)/run_06_17_T02_2_orig_18_25_tp_X.py"
)
RUN_BASENAME = "06.17_T02-4(orig_19-25_tp-X)"
OUTPUT_DIR = ROOT / "Result/06.17_T02_year" / RUN_BASENAME
DATASET_DIR = (
    ROOT
    / "Result/06.13_[B]tok/06.13_[B]03-pre_LLM(orig)_19-25(213)_tok(para12-80)_dataset"
)
STOPWORD_MD = (
    ROOT
    / "Result/06.05_A05_stopword/A05-8(orig)REV_tok(para12-80)/A05-8.4(human)_stopword.md"
)


def load_pipeline_module():
    spec = importlib.util.spec_from_file_location("t02_pipeline", SOURCE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import pipeline module from {SOURCE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


m = load_pipeline_module()

m.ROOT = ROOT
m.RUN_BASENAME = RUN_BASENAME
m.OUTPUT_DIR = OUTPUT_DIR
m.ARTIFACT_DIR = OUTPUT_DIR / "artifacts"
m.DATASET_DIR = DATASET_DIR
m.STOPWORD_MD = STOPWORD_MD
m.EMBEDDINGS_PATH = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.npy"
m.EMBEDDINGS_META_PATH = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.meta.json"
m.REPRESENTATIVE_DOCS_PER_TOPIC = 6
m.CONFIG = {
    "selection_label": RUN_BASENAME,
    "selection_reason": "User-specified T02 2019-2025 BERTopic run with c-TF-IDF topic reduction.",
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


def keep_combined_report_only() -> None:
    report_path = OUTPUT_DIR / f"{RUN_BASENAME}.md"
    if not report_path.exists():
        return
    text = report_path.read_text(encoding="utf-8")
    start = text.find("\n### default\n")
    end = text.find("\n## Output Files\n")
    if start == -1 or end == -1 or start >= end:
        return
    report_path.write_text(text[:start] + text[end:], encoding="utf-8")


if __name__ == "__main__":
    m.main()
    keep_combined_report_only()
