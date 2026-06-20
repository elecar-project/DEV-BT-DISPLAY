from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path
from typing import Any

import pandas as pd
from bertopic import BERTopic
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from umap import UMAP


ROOT = Path(__file__).resolve().parents[3]
BASE_SCRIPT = ROOT / "Result/06.03_A03_min-test/A03-6(repl)_tok(para12-80)/run_06.03_A03_6_repl_tok_para12_80.py"
DATASET_DIR = ROOT / "Result/06.03_A02/R06.03_A02-pre_LLM(repl)_tok(para12-80)_dataset"
OUTPUT_DIR = ROOT / "Result/06.03_A03_min-test/A03-6.1(repl-y)_tok(para12-80)"

REPORT_PATH = OUTPUT_DIR / "Result_06.03_A03-6.1(repl-y)_tok(para12-80).md"
MIN_TEST_CSV = OUTPUT_DIR / "Result_06.03_A03-6.1(repl-y)_tok(para12-80)-min_cluster_size.csv"
BEST_TOPIC_INFO_CSV = OUTPUT_DIR / "Result_06.03_A03-6.1(repl-y)_tok(para12-80)-best_topic_info.csv"
BEST_DOC_TOPICS_CSV = OUTPUT_DIR / "Result_06.03_A03-6.1(repl-y)_tok(para12-80)-best_document_topics.csv"
RUN_LOG_JSON = OUTPUT_DIR / "Result_06.03_A03-6.1(repl-y)_tok(para12-80)-run_log.json"

REPORT_LABEL = "06.03_A03-6.1(repl-y)_tok(para12-80)"
BASE_LABEL = "06.03_A03-6(repl)_tok(para12-80)"
CUSTOM_STOPWORDS = sorted(set(ENGLISH_STOP_WORDS) | {"brand", "model"})


def load_base_module() -> Any:
    spec = importlib.util.spec_from_file_location("a03_6_base_runner", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load base script: {BASE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def patch_module(module: Any) -> None:
    module.DATASET_DIR = DATASET_DIR
    module.OUTPUT_DIR = OUTPUT_DIR
    module.REPORT_PATH = REPORT_PATH
    module.MIN_TEST_CSV = MIN_TEST_CSV
    module.BEST_TOPIC_INFO_CSV = BEST_TOPIC_INFO_CSV
    module.BEST_DOC_TOPICS_CSV = BEST_DOC_TOPICS_CSV
    module.RUN_LOG_JSON = RUN_LOG_JSON

    def train_best_topic_model(
        documents: list[str],
        titles: list[str],
        embedding_model: Any,
        embeddings: Any,
        best_size: int,
    ) -> dict[str, Any]:
        topic_model = BERTopic(
            embedding_model=embedding_model,
            umap_model=UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric="cosine", random_state=42),
            hdbscan_model=HDBSCAN(
                min_cluster_size=best_size,
                metric="euclidean",
                cluster_selection_method="eom",
                prediction_data=True,
            ),
            vectorizer_model=CountVectorizer(stop_words=CUSTOM_STOPWORDS, ngram_range=(1, 2), min_df=2),
            top_n_words=10,
            calculate_probabilities=False,
            verbose=False,
        )
        topics, _ = topic_model.fit_transform(documents, embeddings)
        topic_info = topic_model.get_topic_info()
        doc_topics = pd.DataFrame(
            {
                "title": titles,
                "document": documents,
                "topic": [int(topic) for topic in topics],
            }
        )
        topic_info.to_csv(BEST_TOPIC_INFO_CSV, index=False)
        doc_topics.to_csv(BEST_DOC_TOPICS_CSV, index=False)
        return {
            "topic_count": int(len(topic_info)),
            "topic_info_rows": int(len(topic_info)),
            "custom_stopwords_added": ["brand", "model"],
        }

    module.train_best_topic_model = train_best_topic_model


def patch_report() -> None:
    if not REPORT_PATH.exists():
        return
    text = REPORT_PATH.read_text(encoding="utf-8")
    text = text.replace(BASE_LABEL, REPORT_LABEL)
    old_vectorizer_row = (
        "| CountVectorizer | stop_words=english, ngram_range=(1, 2), min_df=2 | "
        "最佳參數 BERTopic 訓練時使用，降低極低頻詞干擾 |"
    )
    new_vectorizer_row = (
        "| CountVectorizer | stop_words=custom(english + brand/model), ngram_range=(1, 2), min_df=2 | "
        "Embedding 完成後才在 BERTopic vectorizer 排除 brand、model，避免替換詞進入 topic words |"
    )
    text = text.replace(old_vectorizer_row, new_vectorizer_row)
    marker = "| 環境開始運行 | 環境套件可載入，開始 BERTopic min_cluster_size 檢測。 |\n"
    insert = (
        marker
        + "| BERTopic | 已套用自訂 stopwords：英文停用詞加上 brand、model；topic words/Name 已排除，代表句保留原始文本。 |\n"
    )
    text = text.replace(marker, insert)
    REPORT_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    module = load_base_module()
    patch_module(module)
    module.run()
    patch_report()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
