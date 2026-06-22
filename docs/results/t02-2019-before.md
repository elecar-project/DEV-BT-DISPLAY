---
title: T02 2019 前 年份切分
description: T02 年份切分驗證：2008-2018。
experiment_id: t02-2019-before
---

# T02｜2019 前（2008-2018）

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
<div class="run-summary">
<div class="run-stat"><strong>9</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>31.50%</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>40.46%</strong><span>最大主題比例</span></div>
<div class="run-stat"><strong>0.547</strong><span>balance score</span></div>
</div>

## 結果摘要

以 2019 為切點的前段資料。 此頁用於與同一年度切點的另一側資料比較，檢查不同年份界線是否改變主題結構、離群比例或主題集中度。

<div class="table-note" role="note"><strong>LLM 狀態：</strong>原始輸出未保留可用的 LLM 命名驗證結果，因此本頁標示為「未設定／未執行」。Default、KeyBERT、POS 與 MMR 的主題表徵輸出均已保留。</div>

## 預設主題語意摘要

<p class="section-intro">以下列出前 10 個有效主題的 Default c-TF-IDF 代表詞，供比較不同年份切分後的主題內容。</p>

<div class="table-scroll"><table class="semantic-table"><thead><tr><th>Topic</th><th>句數</th><th>Default 代表詞（前 10）</th></tr></thead><tbody><tr><td>0</td><td>4,130</td><td>new, car, design, cars, hyundai, vehicle, electric, volvo, audi, lexus</td></tr><tr><td>1</td><td>1,008</td><td>interior, rear, car, steering, design, led, light, high, dynamic, carbon</td></tr><tr><td>2</td><td>447</td><td>seat, seats, rear, storage, cargo, space, trunk, door, open, passenger</td></tr><tr><td>3</td><td>347</td><td>display, navigation, screen, information, destination, apple, apple carplay, carplay, smartphone, touchscreen</td></tr><tr><td>4</td><td>279</td><td>horsepower, engine, torque, liter, cylinder, gallon, fuel, electric, motor, power</td></tr><tr><td>5</td><td>273</td><td>lane, blind, traffic, brake, spot, blind spot, collision, braking, assist, detection</td></tr><tr><td>6</td><td>192</td><td>charging, charge, vehicle, stations, plug, indicates, charging stations, displayed, cable, charger</td></tr><tr><td>7</td><td>161</td><td>battery, lithium, batteries, pack, battery pack, lithium ion, ion, energy, electric, iron</td></tr><tr><td>8</td><td>155</td><td>infiniti, q50, infinity, new, brand, johan, performance, market, design, sedan</td></tr></tbody></table></div>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/t02-2019-before/06.17_T02-3(orig_08-18_tp-X).md' | relative_url }}">06.17_T02-3(orig_08-18_tp-X).md</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/06.17_T02-3(orig_08-18_tp-X)_LLM.csv' | relative_url }}">06.17_T02-3(orig_08-18_tp-X)_LLM.csv</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/06.17_T02-3(orig_08-18_tp-X)_LLM.md' | relative_url }}">06.17_T02-3(orig_08-18_tp-X)_LLM.md</a></td><td>LLM 命名輸出或報告</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/06.17_T02-3(orig_08-18_tp-X)_combined_representations.csv' | relative_url }}">06.17_T02-3(orig_08-18_tp-X)_combined_representations.csv</a></td><td>Default、KeyBERT、POS、MMR 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/06.17_T02-3(orig_08-18_tp-X)_combined_representations.md' | relative_url }}">06.17_T02-3(orig_08-18_tp-X)_combined_representations.md</a></td><td>Default、KeyBERT、POS、MMR 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/06.17_T02-3(orig_08-18_tp-X)_combined_representations_with_docs.csv' | relative_url }}">06.17_T02-3(orig_08-18_tp-X)_combined_representations_with_docs.csv</a></td><td>Default、KeyBERT、POS、MMR 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/06.17_T02-3(orig_08-18_tp-X)_custom_stopwords_used.txt' | relative_url }}">06.17_T02-3(orig_08-18_tp-X)_custom_stopwords_used.txt</a></td><td>本次實際使用的客製停用詞</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/06.17_T02-3(orig_08-18_tp-X)_run_log.json' | relative_url }}">06.17_T02-3(orig_08-18_tp-X)_run_log.json</a></td><td>執行資料與參數紀錄</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/06.17_T02-3(orig_08-18_tp-X)_summary.csv' | relative_url }}">06.17_T02-3(orig_08-18_tp-X)_summary.csv</a></td><td>模型量化結果摘要 CSV</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/final_config.json' | relative_url }}">artifacts/final_config.json</a></td><td>最終模型設定</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/representation_errors.json' | relative_url }}">artifacts/representation_errors.json</a></td><td>表徵與 LLM 錯誤紀錄</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/representative_docs.csv' | relative_url }}">artifacts/representative_docs.csv</a></td><td>各主題代表文本</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/topic_info.csv' | relative_url }}">artifacts/topic_info.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/topic_info_default.csv' | relative_url }}">artifacts/topic_info_default.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/topic_info_keybert.csv' | relative_url }}">artifacts/topic_info_keybert.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/topic_info_mmr.csv' | relative_url }}">artifacts/topic_info_mmr.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/topic_info_pos.csv' | relative_url }}">artifacts/topic_info_pos.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/topic_size_distribution.csv' | relative_url }}">artifacts/topic_size_distribution.csv</a></td><td>主題大小分布</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/topic_words.csv' | relative_url }}">artifacts/topic_words.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/topic_words_default.csv' | relative_url }}">artifacts/topic_words_default.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/topic_words_keybert.csv' | relative_url }}">artifacts/topic_words_keybert.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/topic_words_mmr.csv' | relative_url }}">artifacts/topic_words_mmr.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/artifacts/topic_words_pos.csv' | relative_url }}">artifacts/topic_words_pos.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/embeddings_all-MiniLM-L6-v2.meta.json' | relative_url }}">embeddings_all-MiniLM-L6-v2.meta.json</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2019-before/run_06_17_T02_3_orig_08_18_tp_X.py' | relative_url }}">run_06_17_T02_3_orig_08_18_tp_X.py</a></td><td>原始實驗輸出</td></tr></tbody></table>
</section>
</div>
