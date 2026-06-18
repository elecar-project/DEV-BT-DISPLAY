#!/usr/bin/env python3
"""Build static dataset comparison assets for GitHub Pages."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

from datasets import DatasetDict, load_from_disk


SOURCE_ROOT = Path("/workspaces/Dev-BT")
DOCS_ROOT = Path(__file__).resolve().parents[1] / "docs"
OUTPUT_ROOT = DOCS_ROOT / "assets" / "datasets"

DATASETS = [
    {
        "id": "initial-txt",
        "label": "初始 txt",
        "source": SOURCE_ROOT / "#TXT_DATA/2. 文字稿－txt",
        "description": "初始逐字稿資料夾。",
        "kind": "txt_folder",
    },
    {
        "id": "deleted-20-no-voice",
        "label": "刪除 20 份無人聲 dataset",
        "source": SOURCE_ROOT / "#TXT_DATA/05.24_txt-test_deleted(434)",
        "description": "刪除 20 份無人聲後保留的 434 個 txt。",
        "kind": "txt_folder",
    },
    {
        "id": "llm-del",
        "label": "LLM 清理 del",
        "source": SOURCE_ROOT / "Result/06.03_A02/R06.03_A02-pre_LLM(del)_dataset",
        "description": "LLM 清理後，刪除廠商與款式名稱。",
        "kind": "hf_dataset",
    },
    {
        "id": "llm-repl",
        "label": "LLM 清理 repl",
        "source": SOURCE_ROOT / "Result/06.03_A02/R06.03_A02-pre_LLM(repl)_dataset",
        "description": "LLM 清理後，將廠商與款式名稱替換成 Brand、Model。",
        "kind": "hf_dataset",
    },
    {
        "id": "year-08-19",
        "label": "年份切分 08-19",
        "source": SOURCE_ROOT / "Result/06.13_[A]/06.13_[A]-01-pre_LLM(orig)_08-19(240)_dataset",
        "description": "以 2020 切分，2008-2019。",
        "kind": "hf_dataset",
    },
    {
        "id": "year-20-25",
        "label": "年份切分 20-25",
        "source": SOURCE_ROOT / "Result/06.13_[A]/06.13_[A]-01-pre_LLM(orig)_20-25(194)_dataset",
        "description": "以 2020 切分，2020-2025。",
        "kind": "hf_dataset",
    },
    {
        "id": "validation-08-17",
        "label": "驗證集1 08-17",
        "source": SOURCE_ROOT / "Result/06.13_[A]/06.13_[A]-02-pre_LLM(orig)_08-17(177)_dataset",
        "description": "以 2018 切分，2008-2017。",
        "kind": "hf_dataset",
    },
    {
        "id": "validation-18-25",
        "label": "驗證集1 18-25",
        "source": SOURCE_ROOT / "Result/06.13_[A]/06.13_[A]-02-pre_LLM(orig)_18-25(257)_dataset",
        "description": "以 2018 切分，2018-2025。",
        "kind": "hf_dataset",
    },
    {
        "id": "validation-08-18",
        "label": "驗證集1 08-18",
        "source": SOURCE_ROOT / "Result/06.13_[A]/06.13_[A]-03-pre_LLM(orig)_08-18(221)_dataset",
        "description": "以 2019 切分，2008-2018。",
        "kind": "hf_dataset",
    },
    {
        "id": "validation-19-25",
        "label": "驗證集1 19-25",
        "source": SOURCE_ROOT / "Result/06.13_[A]/06.13_[A]-03-pre_LLM(orig)_19-25(213)_dataset",
        "description": "以 2019 切分，2019-2025。",
        "kind": "hf_dataset",
    },
    {
        "id": "validation-08-20",
        "label": "驗證集1 08-20",
        "source": SOURCE_ROOT / "Result/06.13_[A]/06.13_[A]-04-pre_LLM(orig)_08-20(288)_dataset",
        "description": "以 2021 切分，2008-2020。",
        "kind": "hf_dataset",
    },
    {
        "id": "validation-21-25",
        "label": "驗證集1 21-25",
        "source": SOURCE_ROOT / "Result/06.13_[A]/06.13_[A]-04-pre_LLM(orig)_21-25(146)_dataset",
        "description": "以 2021 切分，2021-2025。",
        "kind": "hf_dataset",
    },
    {
        "id": "duration-600-2159",
        "label": "驗證集2 1-35 分鐘",
        "source": SOURCE_ROOT / "#TXT_DATA/06.03_600-2159sec(103)",
        "description": "只使用 1-35 分鐘影片。",
        "kind": "txt_folder",
    },
    {
        "id": "manufacturer-trimmed",
        "label": "驗證集3 刪除頭尾各五家廠商",
        "source": SOURCE_ROOT / "#TXT_DATA/06.03_廠商去頭尾各5家(237)",
        "description": "刪除頭尾各五家廠商後保留的 237 個 txt。",
        "kind": "txt_folder",
    },
]


def normalize_name(name: str) -> str:
    stem = Path(name).stem
    if "__" in stem:
        stem = stem.split("__", 1)[1]
    stem = re.sub(r"\([^)]*(?:fps|H264|AV1|AAC|kbit|p_)[^)]*\)", " ", stem, flags=re.I)
    stem = stem.replace("¦", " ").replace("⁄", " ").replace("|", " ")
    stem = re.sub(r"[_;:,#'\"–—-]+", " ", stem)
    stem = re.sub(r"[^0-9A-Za-z]+", " ", stem)
    stem = re.sub(r"\s+", " ", stem).strip().lower()
    return stem


def asset_name(key: str, source: Path) -> str:
    digest = hashlib.sha1(str(source).encode("utf-8")).hexdigest()[:10]
    safe = re.sub(r"[^0-9A-Za-z]+", "-", key).strip("-")[:96] or "file"
    return f"{safe}-{digest}.txt"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def value_to_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(value_to_text(item) for item in value if value_to_text(item))
    return str(value)


def iter_txt_folder(source_dir: Path):
    for source_file in sorted(source_dir.rglob("*.txt")):
        text = read_text(source_file)
        yield {
            "key_source": source_file.name,
            "name": source_file.name,
            "source_path": str(source_file.relative_to(SOURCE_ROOT)),
            "text": text,
        }


def iter_hf_dataset(dataset_path: Path):
    dataset = load_from_disk(str(dataset_path))
    rows = []
    if isinstance(dataset, DatasetDict):
        for split_name, split_dataset in dataset.items():
            for row in split_dataset:
                record = dict(row)
                record.setdefault("split", str(split_name))
                rows.append(record)
    else:
        rows = [dict(row) for row in dataset]

    for index, row in enumerate(rows, start=1):
        title = value_to_text(row.get("title") or row.get("source_file") or row.get("file_name") or row.get("id") or f"row-{index:05d}")
        text = value_to_text(row.get("transcript") or row.get("text") or row.get("sentence") or row.get("content") or "")
        yield {
            "key_source": title,
            "name": title,
            "source_path": f"{dataset_path.relative_to(SOURCE_ROOT)}#{index}",
            "text": text,
        }


def iter_dataset_records(dataset: dict):
    kind = dataset.get("kind", "txt_folder")
    source = dataset["source"]
    if kind == "hf_dataset":
        return iter_hf_dataset(source)
    return iter_txt_folder(source)


def main() -> None:
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    manifest = {
        "generated_from": str(SOURCE_ROOT),
        "matching": "normalized filename; manufacturer prefix and media suffix are ignored when possible",
        "datasets": [],
    }

    for dataset in DATASETS:
        dataset_dir = OUTPUT_ROOT / dataset["id"]
        files_dir = dataset_dir / "files"
        files_dir.mkdir(parents=True, exist_ok=True)

        files = []
        seen_keys: dict[str, int] = {}
        for record in iter_dataset_records(dataset):
            text = record["text"]
            key = normalize_name(record["key_source"])
            seen_keys[key] = seen_keys.get(key, 0) + 1
            if seen_keys[key] > 1:
                key = f"{key} duplicate {seen_keys[key]}"
            output_name = asset_name(key, Path(record["source_path"]))
            output_path = files_dir / output_name
            output_path.write_text(text, encoding="utf-8")
            rel_url = f"assets/datasets/{dataset['id']}/files/{output_name}"
            files.append(
                {
                    "key": key,
                    "name": record["name"],
                    "source_path": record["source_path"],
                    "url": rel_url,
                    "chars": len(text),
                    "lines": text.count("\n") + (1 if text else 0),
                    "sha1": hashlib.sha1(text.encode("utf-8")).hexdigest(),
                }
            )

        manifest["datasets"].append(
            {
                "id": dataset["id"],
                "label": dataset["label"],
                "description": dataset["description"],
                "kind": dataset.get("kind", "txt_folder"),
                "source": str(dataset["source"].relative_to(SOURCE_ROOT)),
                "count": len(files),
                "files": files,
            }
        )

    (OUTPUT_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
