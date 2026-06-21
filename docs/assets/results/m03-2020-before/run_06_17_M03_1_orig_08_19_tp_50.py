from __future__ import annotations

import importlib.util
import json
import os
import re
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
SOURCE_SCRIPT = ROOT / "Result/06.06_M02_single/M02-1(orig-new-tp-30)/run_M02_1_orig_new_tp_30.py"
RUN_BASENAME = "06.17_M03-1(orig_08-19_tp-50)"
OUTPUT_DIR = ROOT / "Result/06.17_M03_split" / RUN_BASENAME
DATASET_DIR = (
    ROOT
    / "Result/06.13_[B]tok/06.13_[B]01-pre_LLM(orig)_08-19(240)_tok(para12-80)_dataset"
)


def load_pipeline_module():
    spec = importlib.util.spec_from_file_location("m02_pipeline", SOURCE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import pipeline module from {SOURCE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


m = load_pipeline_module()

m.ROOT = ROOT
m.RUN_BASENAME = RUN_BASENAME
m.DATASET_DIR = DATASET_DIR
m.OUTPUT_DIR = OUTPUT_DIR
m.EMBEDDINGS_PATH = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.npy"
m.EMBEDDINGS_META = OUTPUT_DIR / "embeddings_all-MiniLM-L6-v2.meta.json"
m.A04_EMBEDDINGS = OUTPUT_DIR / "__no_external_embedding_reuse__.npy"
m.A04_EMBEDDINGS_META = OUTPUT_DIR / "__no_external_embedding_reuse__.meta.json"
m.REPRESENTATIVE_DOCS_PER_TOPIC = 6
m.LLM50_RUNS = 50
m.LLM_MODEL_KEY = "llm_openai_gpt_5_5"
m.LLM_MODEL_NAME = "openai/gpt-5.5"
m.LLM_MODELS = [(m.LLM_MODEL_KEY, m.LLM_MODEL_NAME)]
m.CONFIGS = [
    {
        "selection_label": RUN_BASENAME,
        "report_name": f"{RUN_BASENAME}.md",
        "selection_reason": "User-specified M03 split run with BERTopic nr_topics='auto' c-TF-IDF reduction.",
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
    }
]


def prompt_to_text(messages: list[dict[str, str]]) -> str:
    return "\n\n".join(f"{message['role'].upper()}:\n{message['content']}" for message in messages)


def prompt_parts(topic_id: int, keywords: str, snippets: list[str]) -> dict[str, str]:
    messages = m.llm50_prompt(topic_id, keywords, snippets)
    return {
        "system_prompt": messages[0]["content"],
        "user_prompt": messages[1]["content"],
        "prompt": prompt_to_text(messages),
    }


def llm50_request_task(
    api_key: str,
    topic_id: int,
    run_idx: int,
    keywords: str,
    snippets: list[str],
) -> dict[str, Any]:
    client = m.OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    prompt = prompt_parts(topic_id, keywords, snippets)
    last_error = ""
    for attempt in range(1, 4):
        try:
            label = m.call_openrouter_label(client, topic_id, keywords, snippets, temperature=0.0)
            return {
                "topic": topic_id,
                "run": run_idx,
                "model": m.LLM_MODEL_NAME,
                "temperature": 0.0,
                "max_tokens": 64,
                "keywords": keywords,
                "label": label,
                "normalized_label": m.normalize_label(label),
                "error": "",
                **prompt,
            }
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.75 * attempt)
    return {
        "topic": topic_id,
        "run": run_idx,
        "model": m.LLM_MODEL_NAME,
        "temperature": 0.0,
        "max_tokens": 64,
        "keywords": keywords,
        "label": "",
        "normalized_label": "",
        "error": last_error,
        **prompt,
    }


def run_llm50_validation(
    docs: list[str],
    topics: list[int],
    topic_words: pd.DataFrame,
    out_dir: Path,
    errors: list[dict[str, str]],
) -> dict[str, Any]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    existing_validation = out_dir / f"{RUN_BASENAME}_LLM_validation.csv"
    if not api_key:
        if existing_validation.exists():
            existing_df = pd.read_csv(existing_validation)
            if "successful_runs" in existing_df.columns and len(existing_df) > 1:
                return {
                    "status": "skipped_existing_validation_preserved",
                    "topics": len(existing_df),
                    "calls": int(existing_df["successful_runs"].sum()),
                    "stable_topics": int(existing_df["stable"].astype(bool).sum())
                    if "stable" in existing_df.columns
                    else 0,
                }
        errors.append({"representation_model": "llm50", "error": "OPENROUTER_API_KEY was not provided."})
        return {"status": "skipped", "topics": 0, "calls": 0, "stable_topics": 0}

    preflight_error = m.openrouter_preflight(api_key)
    if preflight_error:
        errors.append({"representation_model": "llm50", "model": m.LLM_MODEL_NAME, "error": preflight_error})
        skipped_df = pd.DataFrame(
            [
                {
                    "topic": "",
                    "model": m.LLM_MODEL_NAME,
                    "runs_requested": m.LLM50_RUNS,
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
                    "prompt": "",
                    "status": "skipped",
                    "error": preflight_error,
                }
            ]
        )
        skipped_df.to_csv(out_dir / f"{RUN_BASENAME}_LLM_validation.csv", index=False)
        pd.DataFrame(
            columns=[
                "topic",
                "run",
                "model",
                "temperature",
                "max_tokens",
                "keywords",
                "label",
                "normalized_label",
                "error",
                "system_prompt",
                "user_prompt",
                "prompt",
            ]
        ).to_csv(out_dir / f"{RUN_BASENAME}_LLM_detail.csv", index=False)
        (out_dir / f"{RUN_BASENAME}_LLM_validation.md").write_text(
            "\n".join(
                [
                    f"# {RUN_BASENAME} LLM50 Validation",
                    "",
                    f"- model: `{m.LLM_MODEL_NAME}` via OpenRouter",
                    "- status: `skipped`",
                    f"- reason: {preflight_error}",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return {"status": "skipped", "topics": 0, "calls": 0, "stable_topics": 0, "error": preflight_error}

    doc_df = pd.DataFrame({"Document": docs, "Topic": topics})
    topic_ids = [int(topic) for topic in topic_words["topic"].tolist()]
    cache_path = out_dir / f"{RUN_BASENAME}_LLM_cache.jsonl"
    cached = m.load_llm50_cache(cache_path)
    records: list[dict[str, Any]] = []
    max_workers = max(1, int(os.getenv("OPENROUTER_LLM50_WORKERS", "6")))
    pending: list[tuple[int, int, str, list[str]]] = []

    for topic_id in topic_ids:
        row = topic_words.loc[topic_words["topic"] == topic_id].iloc[0]
        keywords = str(row.get("words", ""))
        snippets = (
            doc_df.loc[doc_df["Topic"] == topic_id, "Document"]
            .dropna()
            .astype(str)
            .head(m.REPRESENTATIVE_DOCS_PER_TOPIC)
            .tolist()
        )
        for run_idx in range(1, m.LLM50_RUNS + 1):
            cache_key = (topic_id, run_idx)
            if cache_key in cached:
                item = cached[cache_key]
                if "prompt" not in item:
                    item = {**item, **prompt_parts(topic_id, keywords, snippets)}
                records.append(item)
            else:
                pending.append((topic_id, run_idx, keywords, snippets))

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
                cached[(int(item["topic"]), int(item["run"]))] = item
                records.append(item)
                completed += 1
                if item.get("error"):
                    errors.append(
                        {
                            "representation_model": "llm50",
                            "topic": str(item["topic"]),
                            "run": str(item["run"]),
                            "model": m.LLM_MODEL_NAME,
                            "error": str(item["error"]),
                        }
                    )
                if completed % 25 == 0 or completed == len(pending):
                    print(f"  LLM50 completed {completed}/{len(pending)} pending calls", flush=True)

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
        avg_jaccard = float(np.mean([m.jaccard_similarity(label, mode_label) for label in labels])) if labels else 0.0
        is_stable = bool(exact_ratio >= 0.70 or avg_jaccard >= 0.65)
        first = group.iloc[0]
        summary_rows.append(
            {
                "topic": int(topic_id),
                "model": m.LLM_MODEL_NAME,
                "temperature": 0.0,
                "max_tokens": 64,
                "runs_requested": m.LLM50_RUNS,
                "successful_runs": successful,
                "error_runs": int(group["error"].astype(bool).sum()),
                "unique_normalized_labels": len(counts),
                "mode_label": display_mode,
                "mode_normalized_label": mode_label,
                "mode_count": mode_count,
                "mode_ratio": exact_ratio,
                "avg_jaccard_to_mode": avg_jaccard,
                "stable": is_stable,
                "keywords": str(first.get("keywords", "")),
                "system_prompt": str(first.get("system_prompt", "")),
                "user_prompt": str(first.get("user_prompt", "")),
                "prompt": str(first.get("prompt", "")),
                "all_labels": " || ".join(str(label) for label in group["label"].tolist() if label),
            }
        )
    summary_df = pd.DataFrame(summary_rows)
    detail_df.to_csv(out_dir / f"{RUN_BASENAME}_LLM_detail.csv", index=False)
    summary_df.to_csv(out_dir / f"{RUN_BASENAME}_LLM_validation.csv", index=False)

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
    prompt_example = summary_df["prompt"].iloc[0] if not summary_df.empty else ""
    report = [
        f"# {RUN_BASENAME} LLM50 Validation",
        "",
        f"- model: `{m.LLM_MODEL_NAME}` via OpenRouter",
        "- temperature: `0.0`",
        "- max_tokens: `64`",
        f"- runs per topic, including topic `-1`: {m.LLM50_RUNS}",
        f"- input per topic: same default c-TF-IDF keywords and same first {m.REPRESENTATIVE_DOCS_PER_TOPIC} representative topic documents",
        "- stable rule: `mode_ratio >= 0.70` or `avg_jaccard_to_mode >= 0.65`",
        f"- stable topics: {int(summary_df['stable'].sum()) if not summary_df.empty else 0} / {len(summary_df)}",
        "",
        "## Prompt Used",
        "",
        "```text",
        prompt_example,
        "```",
        "",
        "## Validation Summary",
        "",
        m.md_table(md_rows, list(md_rows[0].keys()) if md_rows else ["topic"]),
        "",
        "## Interpretation",
        "",
        "若 `stable=True`，代表同一組 keywords 與文本重跑時，模型給出的主題名稱在字面或詞彙組成上大致一致；若為 `False`，建議人工檢查該 topic 的 keywords 是否過於混雜。",
        "",
    ]
    (out_dir / f"{RUN_BASENAME}_LLM_validation.md").write_text("\n".join(report), encoding="utf-8")
    return {
        "status": "ok",
        "topics": len(summary_df),
        "calls": len(detail_df),
        "stable_topics": int(summary_df["stable"].sum()) if not summary_df.empty else 0,
        "csv": f"{RUN_BASENAME}_LLM_validation.csv",
        "md": f"{RUN_BASENAME}_LLM_validation.md",
    }


def write_llm_result_files(combined: pd.DataFrame, validation: pd.DataFrame | None, out_dir: Path) -> None:
    columns = ["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"]
    combined_rows = combined[columns].to_dict("records") if not combined.empty else []
    validation_rows: list[dict[str, Any]] = []
    stable_text = "0 / 0"
    successful_text = "0 / 0"

    llm_csv = combined.copy()
    if isinstance(validation, pd.DataFrame) and not validation.empty and "topic" in validation.columns:
        validation = validation.copy()
        if "stable" in validation.columns:
            stable_count = int(validation["stable"].astype(bool).sum())
            stable_text = f"{stable_count} / {len(validation)}"
        if {"successful_runs", "runs_requested"}.issubset(validation.columns):
            successful = int(validation["successful_runs"].sum())
            requested = int(validation["runs_requested"].sum())
            successful_text = f"{successful} / {requested}"
        validation_columns = [
            "topic",
            "successful_runs",
            "unique_normalized_labels",
            "mode_label",
            "mode_ratio",
            "avg_jaccard_to_mode",
            "stable",
            "keywords",
        ]
        available = [col for col in validation_columns if col in validation.columns]
        validation_rows = validation[available].to_dict("records")
        merge_cols = [
            col
            for col in [
                "topic",
                "model",
                "temperature",
                "max_tokens",
                "runs_requested",
                "successful_runs",
                "error_runs",
                "unique_normalized_labels",
                "mode_label",
                "mode_ratio",
                "avg_jaccard_to_mode",
                "stable",
                "keywords",
                "prompt",
            ]
            if col in validation.columns
        ]
        llm_csv = llm_csv.merge(validation[merge_cols], how="left", left_on="Topic", right_on="topic")
        llm_csv = llm_csv.drop(columns=["topic"], errors="ignore")
    llm_csv.to_csv(out_dir / f"{RUN_BASENAME}_LLM.csv", index=False)

    prompt_text = ""
    if isinstance(validation, pd.DataFrame) and not validation.empty and "prompt" in validation.columns:
        prompts = validation["prompt"].dropna().astype(str)
        prompt_text = prompts.iloc[0] if not prompts.empty else ""

    report = [
        f"# {RUN_BASENAME} LLM Topic Results",
        "",
        f"- model: `{m.LLM_MODEL_NAME}` via OpenRouter",
        "- temperature: `0.0`",
        "- max_tokens: `64`",
        f"- runs per topic, including topic `-1`: {m.LLM50_RUNS}",
        f"- representative docs per topic: {m.REPRESENTATIVE_DOCS_PER_TOPIC}",
        "- stable rule: `mode_ratio >= 0.70` or `avg_jaccard_to_mode >= 0.65`",
        f"- successful validation calls: {successful_text}",
        f"- stable topics: {stable_text}",
        "",
        "## Prompt Used",
        "",
        "```text",
        prompt_text,
        "```",
        "",
        "## Combined Topic Representations",
        "",
        m.md_table(combined_rows, columns) if combined_rows else "無",
        "",
        "## LLM50 Validation Summary",
        "",
        m.md_table(validation_rows, list(validation_rows[0].keys())) if validation_rows else "無",
        "",
        "## Interpretation",
        "",
        "若 `stable=True`，代表同一組 keywords 與文本重跑時，模型給出的主題名稱在字面或詞彙組成上大致一致；若為 `False`，建議人工檢查該 topic 的 keywords 是否過於混雜。",
        "",
    ]
    (out_dir / f"{RUN_BASENAME}_LLM.md").write_text("\n".join(report), encoding="utf-8")


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
    validation_path = OUTPUT_DIR / f"{RUN_BASENAME}_LLM_validation.csv"
    validation_df = pd.read_csv(validation_path) if validation_path.exists() else pd.DataFrame()
    stable_text = "0 / 0"
    successful_text = "0 / 0"
    if not validation_df.empty and "stable" in validation_df.columns:
        stable_text = f"{int(validation_df['stable'].astype(bool).sum())} / {len(validation_df)}"
    if not validation_df.empty and {"successful_runs", "runs_requested"}.issubset(validation_df.columns):
        successful_text = f"{int(validation_df['successful_runs'].sum())} / {int(validation_df['runs_requested'].sum())}"

    run_row = {
        "started_at": started_at,
        "finished_at": finished_at,
        "dataset": meta["dataset"],
        "used_rows": meta["used_rows"],
        "embedding_model": m.EMBEDDING_MODEL_NAME,
        "custom_stopword_count": len(custom_stopwords),
        "llm_provider": "OpenRouter",
        "llm_model": m.LLM_MODEL_NAME,
        "llm50_successful_calls": successful_text,
        "representative_docs_per_topic": m.REPRESENTATIVE_DOCS_PER_TOPIC,
    }
    parameter_row = {
        "bertopic_nr_topics": config.get("nr_topics"),
        "umap_n_neighbors": config["umap"]["n_neighbors"],
        "umap_n_components": config["umap"]["n_components"],
        "umap_min_dist": config["umap"]["min_dist"],
        "hdbscan_min_cluster_size": config["hdbscan"]["min_cluster_size"],
        "hdbscan_min_samples": config["hdbscan"]["min_samples"],
        "hdbscan_cluster_selection_method": config["hdbscan"]["cluster_selection_method"],
        "hdbscan_cluster_selection_epsilon": config["hdbscan"]["cluster_selection_epsilon"],
    }
    metric_row = {
        "n_clusters": metrics.get("n_clusters"),
        "noise_ratio": metrics.get("noise_ratio"),
        "topic_-1_count": metrics.get("topic_-1_count"),
        "largest_topic_count": metrics.get("largest_topic_count"),
        "stable_topics": stable_text,
        "representation_errors": len(errors),
    }
    columns = ["Topic", "Count", "Name", "LLM", "KeyBERT", "POS", "MMR"]
    report = [
        f"# {RUN_BASENAME} BERTopic + A05-8.4(human) stopwords + c-TF-IDF reduction",
        "",
        "## Run Info",
        "",
        m.md_table([run_row], list(run_row.keys())),
        "",
        "## Parameters",
        "",
        m.md_table([parameter_row], list(parameter_row.keys())),
        "",
        "## Metrics",
        "",
        m.md_table([metric_row], list(metric_row.keys())),
        "",
        "## Stopword Setting",
        "",
        f"- stopword source: `{m.STOPWORD_MD.relative_to(ROOT)}`",
        "- 使用 A05-8.4(human) 報告表格第三欄建議停用詞，並加上 sklearn English stop words。",
        "",
        "## Topic Representation",
        "",
        "- KeyBERT-Inspired",
        "- Part-of-Speech (POS)",
        "- Maximal Marginal Relevance (MMR)",
        f"- OpenRouter `{m.LLM_MODEL_NAME}` topic labels",
        "",
        "## LLM50 Validation",
        "",
        f"- 每個 topic（包含 `-1` outlier topic）使用 `{m.LLM_MODEL_NAME}` 對相同 keywords 與 {m.REPRESENTATIVE_DOCS_PER_TOPIC} 個代表文本重跑 {m.LLM50_RUNS} 次。",
        "- temperature: `0.0`; max_tokens: `64`。",
        "- 穩定判定：normalized label 眾數比例 >= 0.70，或平均 token Jaccard similarity >= 0.65。",
        f"- 穩定 topic：{stable_text}。",
        f"- 詳細 prompt 與每次輸出：`{RUN_BASENAME}_LLM.md`、`{RUN_BASENAME}_LLM.csv`、`{RUN_BASENAME}_LLM_detail.csv`。",
        "",
        "## Combined Topic Representations",
        "",
        m.md_table(combined_representations.to_dict("records"), columns)
        if not combined_representations.empty
        else "無",
        "",
        "## Output Files",
        "",
        m.md_table([csv_paths], list(csv_paths.keys())),
        "",
        "## Representation Errors",
        "",
        "無" if not errors else "```json\n" + json.dumps(errors, ensure_ascii=False, indent=2) + "\n```",
        "",
        "## Notes",
        "",
        "BERTopic `nr_topics='auto'` 在初始 HDBSCAN 分群後用 c-TF-IDF 相似度自動合併主題；本報告 metrics 為 reduction 後的 topic labels。",
        "KeyBERT-Inspired、POS、MMR 與 LLM 只更新 topic representation，不改變 UMAP/HDBSCAN topic labels。",
        "",
    ]
    (OUTPUT_DIR / config["report_name"]).write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    docs, titles, meta = m.load_documents()
    custom_stopwords = m.extract_recommended_stopwords(m.STOPWORD_MD)
    stopwords = sorted(set(m.ENGLISH_STOP_WORDS).union(custom_stopwords))
    (OUTPUT_DIR / f"{RUN_BASENAME}_custom_stopwords_used.txt").write_text(
        "\n".join(custom_stopwords) + "\n", encoding="utf-8"
    )
    embedding_model, embeddings, embedding_note = m.get_embeddings(docs)
    vectorizer_model = m.CountVectorizer(stop_words=stopwords, ngram_range=(1, 2), min_df=2)
    global_errors: list[dict[str, str]] = []
    summaries = []
    for config in m.CONFIGS:
        print(f"Training {config['selection_label']}...", flush=True)
        llm_representations = m.build_llm_representations(global_errors)
        summaries.append(
            m.run_one(
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
    pd.DataFrame(summaries).to_csv(OUTPUT_DIR / f"{RUN_BASENAME}_summary.csv", index=False)
    (OUTPUT_DIR / f"{RUN_BASENAME}_run_summary.json").write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUTPUT_DIR / f"{RUN_BASENAME}_run_log.json").write_text(
        json.dumps(
            {
                "finished_at": datetime.now(timezone.utc).isoformat(),
                "dataset": str(DATASET_DIR.relative_to(ROOT)),
                "output_dir": str(OUTPUT_DIR.relative_to(ROOT)),
                "stopword_md": str(m.STOPWORD_MD.relative_to(ROOT)),
                "custom_stopword_count": len(custom_stopwords),
                "total_stopword_count_with_english": len(stopwords),
                "embedding_note": embedding_note,
                "rows": len(docs),
                "configs": [config["selection_label"] for config in m.CONFIGS],
                "representation_models": ["default", "keybert", "pos", "mmr", *[name for name, _ in m.LLM_MODELS]],
                "llm_provider": "OpenRouter",
                "llm_model": m.LLM_MODEL_NAME,
                "llm_temperature": 0.0,
                "llm_max_tokens": 64,
                "llm50_runs_per_topic": m.LLM50_RUNS,
                "llm50_includes_outlier_topic": True,
                "representative_docs_per_topic": m.REPRESENTATIVE_DOCS_PER_TOPIC,
                "global_errors": global_errors,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


m.run_llm50_validation = run_llm50_validation
m.write_llm_result_files = write_llm_result_files
m.write_report = write_report


if __name__ == "__main__":
    main()
