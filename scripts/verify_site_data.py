#!/usr/bin/env python3
"""Verify published dataset counts and text hashes against the research source.

Run: python3 scripts/verify_site_data.py --source-root /path/to/DEV-BT
Requires the datasets package already used by build_dataset_browser.py.
No transcripts, credentials or absolute local paths are written to the report.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import build_dataset_browser as exporter


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', required=True, type=Path)
    parser.add_argument('--manifest', type=Path, default=Path(__file__).resolve().parents[1] / 'docs/assets/datasets/manifest.json')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    exporter.SOURCE_ROOT = args.source_root.resolve()
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    checks = []
    for dataset in manifest['datasets']:
        source = exporter.SOURCE_ROOT / dataset.get('current_source', dataset['source'])
        if not source.is_dir():
            checks.append({'id': dataset['id'], 'passed': False, 'error': 'Source directory not found'})
            continue
        records = list(exporter.iter_dataset_records({'source': source, 'kind': dataset['kind']}))
        expected = Counter((item['sha1'], item['chars']) for item in dataset['files'])
        actual = Counter((hashlib.sha1(row['text'].encode('utf-8')).hexdigest(), len(row['text'])) for row in records)
        duplicates = len(dataset['files']) - len({row['key'] for row in dataset['files']})
        passed = dataset['count'] == len(dataset['files']) == len(records) and expected == actual and duplicates == 0
        checks.append({'id': dataset['id'], 'published_records': dataset['count'], 'source_records': len(records), 'missing_or_different_records': sum((expected - actual).values()), 'duplicate_match_keys': duplicates, 'passed': passed})
    report = {'status': 'passed' if all(item['passed'] for item in checks) else 'failed', 'dataset_versions': len(checks), 'published_version_records': sum(dataset['count'] for dataset in manifest['datasets']), 'checks': checks}
    encoded = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding='utf-8')
    print(encoded)
    raise SystemExit(0 if report['status'] == 'passed' else 1)


if __name__ == '__main__':
    main()
