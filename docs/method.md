---
title: Method
description: Research workflow and processing pipeline for DEV-BT.
---

# Method

This page documents the research workflow from raw transcript collection to
topic modeling outputs.

## Pipeline Overview

1. Collect or import transcript data.
2. Clean transcripts for ASR artifacts and low-information text.
3. Split transcripts into sentence-level records.
4. Build BERTopic-friendly datasets.
5. Run BERTopic experiments with controlled parameter settings.
6. Compare topic quality, outliers, topic labels, and time/product groupings.
7. Curate final outputs for internal review and public-facing summaries.

## Components To Migrate

- ASR and transcript-processing notes from the mother repository.
- Pre-process app usage and exported dataset rules.
- BERTopic app parameters and experiment presets.
- Decisions about stopwords, brand removal, sentence splitting, and topic labels.

## Open Items

- Define the canonical preprocessing pipeline.
- Define the final BERTopic parameter set or comparison matrix.
- Link to reproducible scripts for the selected runs.
