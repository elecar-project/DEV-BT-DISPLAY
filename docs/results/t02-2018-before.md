---
title: T02 2018 前 年份切分
description: T02 年份切分驗證：2008-2017。
experiment_id: t02-2018-before
---

# T02｜2018 前（2008-2017）

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
<div class="run-summary">
<div class="run-stat"><strong>5</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>5.59%</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>85.10%</strong><span>最大主題比例</span></div>
<div class="run-stat"><strong>0.387</strong><span>balance score</span></div>
</div>

## 結果摘要

以 2018 為切點的前段資料。 此頁用於與同一年度切點的另一側資料比較，檢查不同年份界線是否改變主題結構、離群比例或主題集中度。

<aside class="table-note"><strong>LLM 狀態：</strong>原始輸出未保留可用的 LLM 命名驗證結果，因此本頁標示為「未設定／未執行」。Default、KeyBERT、POS 與 MMR 的主題表徵輸出均已保留。</aside>

## 預設主題語意摘要

<p class="section-intro">以下列出前 10 個有效主題的 Default c-TF-IDF 代表詞，供比較不同年份切分後的主題內容。</p>

<div class="table-scroll"><table class="semantic-table"><thead><tr><th>Topic</th><th>句數</th><th>Default 代表詞（前 10）</th></tr></thead><tbody><tr><td>0</td><td>6,972</td><td>car, new, vehicle, electric, drive, driving, design, rear, power, battery</td></tr><tr><td>1</td><td>224</td><td>hyundai, sonata, ioniq, kia, hyundai sonata, new, 2018, fleet, optima, new kia</td></tr><tr><td>2</td><td>200</td><td>bmw, series, i8, new bmw, bmw series, new, i3, car, driving, bmw i3</td></tr><tr><td>3</td><td>174</td><td>infiniti, q50, infinity, new, brand, performance, cancer, johan, market, future</td></tr><tr><td>4</td><td>165</td><td>volvo, xc90, new, new xc90, design, safety, xc90 new, cars, s90, volvo cars</td></tr></tbody></table></div>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X).md' | relative_url }}">06.17_T02-1(orig_08-17_tp-X).md</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X)_LLM.csv' | relative_url }}">06.17_T02-1(orig_08-17_tp-X)_LLM.csv</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X)_LLM.md' | relative_url }}">06.17_T02-1(orig_08-17_tp-X)_LLM.md</a></td><td>LLM 命名輸出或報告</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X)_LLM_detail.csv' | relative_url }}">06.17_T02-1(orig_08-17_tp-X)_LLM_detail.csv</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X)_LLM_validation.csv' | relative_url }}">06.17_T02-1(orig_08-17_tp-X)_LLM_validation.csv</a></td><td>LLM 驗證輸出；本次未執行或未保留可用結果</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X)_LLM_validation.md' | relative_url }}">06.17_T02-1(orig_08-17_tp-X)_LLM_validation.md</a></td><td>LLM 驗證輸出；本次未執行或未保留可用結果</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X)_combined_representations.csv' | relative_url }}">06.17_T02-1(orig_08-17_tp-X)_combined_representations.csv</a></td><td>Default、KeyBERT、POS、MMR 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X)_combined_representations.md' | relative_url }}">06.17_T02-1(orig_08-17_tp-X)_combined_representations.md</a></td><td>Default、KeyBERT、POS、MMR 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X)_combined_representations_with_docs.csv' | relative_url }}">06.17_T02-1(orig_08-17_tp-X)_combined_representations_with_docs.csv</a></td><td>Default、KeyBERT、POS、MMR 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X)_custom_stopwords_used.txt' | relative_url }}">06.17_T02-1(orig_08-17_tp-X)_custom_stopwords_used.txt</a></td><td>本次實際使用的客製停用詞</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X)_run_log.json' | relative_url }}">06.17_T02-1(orig_08-17_tp-X)_run_log.json</a></td><td>執行資料與參數紀錄</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X)_run_summary.json' | relative_url }}">06.17_T02-1(orig_08-17_tp-X)_run_summary.json</a></td><td>模型量化結果摘要</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/06.17_T02-1(orig_08-17_tp-X)_summary.csv' | relative_url }}">06.17_T02-1(orig_08-17_tp-X)_summary.csv</a></td><td>模型量化結果摘要 CSV</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/final_config.json' | relative_url }}">artifacts/final_config.json</a></td><td>最終模型設定</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/representation_errors.json' | relative_url }}">artifacts/representation_errors.json</a></td><td>表徵與 LLM 錯誤紀錄</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/representative_docs.csv' | relative_url }}">artifacts/representative_docs.csv</a></td><td>各主題代表文本</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/topic_info.csv' | relative_url }}">artifacts/topic_info.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/topic_info_default.csv' | relative_url }}">artifacts/topic_info_default.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/topic_info_keybert.csv' | relative_url }}">artifacts/topic_info_keybert.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/topic_info_mmr.csv' | relative_url }}">artifacts/topic_info_mmr.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/topic_info_pos.csv' | relative_url }}">artifacts/topic_info_pos.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/topic_size_distribution.csv' | relative_url }}">artifacts/topic_size_distribution.csv</a></td><td>主題大小分布</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/topic_words.csv' | relative_url }}">artifacts/topic_words.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/topic_words_default.csv' | relative_url }}">artifacts/topic_words_default.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/topic_words_keybert.csv' | relative_url }}">artifacts/topic_words_keybert.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/topic_words_mmr.csv' | relative_url }}">artifacts/topic_words_mmr.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/artifacts/topic_words_pos.csv' | relative_url }}">artifacts/topic_words_pos.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/embeddings_all-MiniLM-L6-v2.meta.json' | relative_url }}">embeddings_all-MiniLM-L6-v2.meta.json</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2018-before/run_06_17_T02_1_orig_08_17_tp_X.py' | relative_url }}">run_06_17_T02_1_orig_08_17_tp_X.py</a></td><td>原始實驗輸出</td></tr></tbody></table>
</section>
</div>
