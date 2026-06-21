from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_SCRIPT = (
    ROOT
    / "Result/06.17_T02_year/06.17_T02-2(orig_18-25_tp-X)/run_06_17_T02_2_orig_18_25_tp_X.py"
)
RUN_BASENAME = "06.17_T02-1(orig_08-17_tp-X)"
OUTPUT_DIR = ROOT / "Result/06.17_T02_year" / RUN_BASENAME
DATASET_DIR = (
    ROOT
    / "Result/06.13_[B]tok/06.13_[B]02-pre_LLM(orig)_08-17(177)_tok(para12-80)_dataset"
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
m.CONFIG = {
    **m.CONFIG,
    "selection_label": RUN_BASENAME,
    "selection_reason": "User-specified T02 2008-2017 BERTopic run with c-TF-IDF topic reduction.",
    "umap": {
        **m.CONFIG["umap"],
        "n_neighbors": 10,
        "n_components": 5,
        "min_dist": 0.0,
    },
    "hdbscan": {
        **m.CONFIG["hdbscan"],
        "min_cluster_size": 125,
        "min_samples": 5,
        "cluster_selection_method": "eom",
        "cluster_selection_epsilon": 0.0,
    },
    "nr_topics": "auto",
}


if __name__ == "__main__":
    m.main()
