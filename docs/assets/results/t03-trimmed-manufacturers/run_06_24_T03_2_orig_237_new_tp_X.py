"""Run the requested T03 BERTopic validation configuration.

This wrapper reuses the maintained BERTopic runner and only replaces the
dataset/output/configuration constants for this validation run.
"""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUN_BASENAME = Path(__file__).resolve().parent.name
SOURCE = ROOT / "Result/06.17_M03_split/06.17_M03-2(orig_20-25_tp-50)/run_06_17_M03_2_orig_20_25_tp_50.py"

spec = spec_from_file_location("bertopic_t03_base", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load runner: {SOURCE}")
runner = module_from_spec(spec)
spec.loader.exec_module(runner)

runner.ROOT = ROOT
runner.RUN_BASENAME = RUN_BASENAME
runner.OUTPUT_DIR = Path(__file__).resolve().parent
runner.DATASET_DIR = ROOT / (
    "#運行BERTopic整理/#2.1 清理後輸入資料集（dataset）/"
    "02.2-驗證集3 刪除頭尾各五家廠商_(237)/"
    "R06.03_A02-pre_LLM(orig)-(237)_tok(para12-80)_dataset"
)
runner.STOPWORD_MD = ROOT / "Result/06.05_A05_stopword/A05-8(orig)REV_tok(para12-80)/A05-8.4(human)_stopword.md"
runner.EMBEDDINGS_PATH = runner.OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.npy"
runner.EMBEDDINGS_META = runner.OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.meta.json"
runner.EMBEDDING_SOURCES = []
runner.REPRESENTATIVE_DOCS_PER_TOPIC = 6
runner.CONFIG = {
    "selection_label": RUN_BASENAME,
    "report_name": f"{RUN_BASENAME}.md",
    "selection_reason": "使用者指定參數，並以 BERTopic nr_topics='auto' 做 c-TF-IDF topic reduction。",
    "nr_topics": "auto",
    "umap": {"n_neighbors": 10, "n_components": 15, "min_dist": 0.0, "metric": "cosine", "random_state": 42},
    "hdbscan": {
        "min_cluster_size": 50,
        "min_samples": 5,
        "metric": "euclidean",
        "cluster_selection_method": "eom",
        "cluster_selection_epsilon": 0.2,
    },
}

if __name__ == "__main__":
    runner.main()
