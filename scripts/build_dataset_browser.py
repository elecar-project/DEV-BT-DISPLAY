#!/usr/bin/env python3
"""Build static dataset comparison assets for GitHub Pages."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path


SOURCE_ROOT = Path("/workspaces/Dev-BT")
DOCS_ROOT = Path(__file__).resolve().parents[1] / "docs"
OUTPUT_ROOT = DOCS_ROOT / "assets" / "datasets"

DATASETS = [
    {
        "id": "raw-transcripts",
        "label": "原始逐字稿",
        "source": SOURCE_ROOT / "#TXT_DATA/2. 文字稿－txt",
        "description": "454 個原始逐字稿 txt。",
    },
    {
        "id": "cleaned-434",
        "label": "主要清理後逐字稿",
        "source": SOURCE_ROOT / "#TXT_DATA/05.24_txt-test_deleted(434)",
        "description": "434 個主要分析逐字稿。",
    },
    {
        "id": "duration-600-2159",
        "label": "600-2159 秒篩選資料",
        "source": SOURCE_ROOT / "#TXT_DATA/06.03_600-2159sec(103)",
        "description": "依影片長度篩選後的 103 個 txt。",
    },
    {
        "id": "manufacturer-trimmed",
        "label": "廠商去頭尾資料",
        "source": SOURCE_ROOT / "#TXT_DATA/06.03_廠商去頭尾各5家(237)",
        "description": "每個廠商去除頭尾各 5 筆後保留的 237 個 txt。",
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
        source_dir = dataset["source"]
        for source_file in sorted(source_dir.rglob("*.txt")):
            text = read_text(source_file)
            key = normalize_name(source_file.name)
            output_name = asset_name(key, source_file)
            output_path = files_dir / output_name
            output_path.write_text(text, encoding="utf-8")
            rel_url = f"assets/datasets/{dataset['id']}/files/{output_name}"
            files.append(
                {
                    "key": key,
                    "name": source_file.name,
                    "source_path": str(source_file.relative_to(SOURCE_ROOT)),
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
