---
title: T02 2021 前 年份切分
description: T02 年份切分驗證：2008-2020。
experiment_id: t02-2021-before
---

# T02｜2021 前（2008-2020）

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
<div class="run-summary">
<div class="run-stat"><strong>19</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>28.99%</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>27.86%</strong><span>最大主題比例</span></div>
<div class="run-stat"><strong>0.704</strong><span>balance score</span></div>
</div>

## 結果摘要

以 2021 為切點的前段資料。 此頁用於與同一年度切點的另一側資料比較，檢查不同年份界線是否改變主題結構、離群比例或主題集中度。

<aside class="table-note"><strong>LLM 狀態：</strong>原始輸出未保留可用的 LLM 命名驗證結果，因此本頁標示為「未設定／未執行」。Default、KeyBERT、POS 與 MMR 的主題表徵輸出均已保留。</aside>

## 預設主題語意摘要

<p class="section-intro">以下列出前 10 個有效主題的 Default c-TF-IDF 代表詞，供比較不同年份切分後的主題內容。</p>

<div class="table-scroll"><table class="semantic-table"><thead><tr><th>Topic</th><th>句數</th><th>Default 代表詞（前 10）</th></tr></thead><tbody><tr><td>0</td><td>4,058</td><td>new, car, bmw, design, lexus, cars, volvo, customers, world, series</td></tr><tr><td>1</td><td>785</td><td>rear, steering, suspension, speed, car, transmission, aerodynamics, drive, air, line</td></tr><tr><td>2</td><td>777</td><td>electric, engine, horsepower, torque, power, liter, cylinder, battery, motor, car</td></tr><tr><td>3</td><td>652</td><td>seat, seats, door, cargo, trunk, rear, space, storage, leather, carbon</td></tr><tr><td>4</td><td>595</td><td>display, navigation, screen, voice, phone, carplay, apple, android, information, apple carplay</td></tr><tr><td>5</td><td>491</td><td>lane, assist, mode, braking, brake, blind, traffic, blind spot, spot, collision</td></tr><tr><td>6</td><td>438</td><td>charging, charge, taycan, charger, stations, charging stations, station, volt, charging station, battery</td></tr><tr><td>7</td><td>366</td><td>led, grille, light, lights, headlights, kidney, tail, rear, design, laser</td></tr><tr><td>8</td><td>348</td><td>interior, materials, design, colors, color, inside, surfaces, orange, premium, beautiful</td></tr><tr><td>9</td><td>290</td><td>sonata, hyundai, kia, hyundai sonata, warranty, new, 2018, 2018 hyundai, 2020, fleet</td></tr></tbody></table></div>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/t02-2021-before/06.17_T02-5(orig_08-20_tp-X).md' | relative_url }}">06.17_T02-5(orig_08-20_tp-X).md</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/06.17_T02-5(orig_08-20_tp-X)_LLM.csv' | relative_url }}">06.17_T02-5(orig_08-20_tp-X)_LLM.csv</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/06.17_T02-5(orig_08-20_tp-X)_LLM.md' | relative_url }}">06.17_T02-5(orig_08-20_tp-X)_LLM.md</a></td><td>LLM 命名輸出或報告</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/06.17_T02-5(orig_08-20_tp-X)_combined_representations.csv' | relative_url }}">06.17_T02-5(orig_08-20_tp-X)_combined_representations.csv</a></td><td>Default、KeyBERT、POS、MMR 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/06.17_T02-5(orig_08-20_tp-X)_combined_representations.md' | relative_url }}">06.17_T02-5(orig_08-20_tp-X)_combined_representations.md</a></td><td>Default、KeyBERT、POS、MMR 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/06.17_T02-5(orig_08-20_tp-X)_combined_representations_with_docs.csv' | relative_url }}">06.17_T02-5(orig_08-20_tp-X)_combined_representations_with_docs.csv</a></td><td>Default、KeyBERT、POS、MMR 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/06.17_T02-5(orig_08-20_tp-X)_custom_stopwords_used.txt' | relative_url }}">06.17_T02-5(orig_08-20_tp-X)_custom_stopwords_used.txt</a></td><td>本次實際使用的客製停用詞</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/06.17_T02-5(orig_08-20_tp-X)_run_log.json' | relative_url }}">06.17_T02-5(orig_08-20_tp-X)_run_log.json</a></td><td>執行資料與參數紀錄</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/06.17_T02-5(orig_08-20_tp-X)_summary.csv' | relative_url }}">06.17_T02-5(orig_08-20_tp-X)_summary.csv</a></td><td>模型量化結果摘要 CSV</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/final_config.json' | relative_url }}">artifacts/final_config.json</a></td><td>最終模型設定</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/representation_errors.json' | relative_url }}">artifacts/representation_errors.json</a></td><td>表徵與 LLM 錯誤紀錄</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/representative_docs.csv' | relative_url }}">artifacts/representative_docs.csv</a></td><td>各主題代表文本</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/topic_info.csv' | relative_url }}">artifacts/topic_info.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/topic_info_default.csv' | relative_url }}">artifacts/topic_info_default.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/topic_info_keybert.csv' | relative_url }}">artifacts/topic_info_keybert.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/topic_info_mmr.csv' | relative_url }}">artifacts/topic_info_mmr.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/topic_info_pos.csv' | relative_url }}">artifacts/topic_info_pos.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/topic_size_distribution.csv' | relative_url }}">artifacts/topic_size_distribution.csv</a></td><td>主題大小分布</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/topic_words.csv' | relative_url }}">artifacts/topic_words.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/topic_words_default.csv' | relative_url }}">artifacts/topic_words_default.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/topic_words_keybert.csv' | relative_url }}">artifacts/topic_words_keybert.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/topic_words_mmr.csv' | relative_url }}">artifacts/topic_words_mmr.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/artifacts/topic_words_pos.csv' | relative_url }}">artifacts/topic_words_pos.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/embeddings_all-MiniLM-L6-v2.meta.json' | relative_url }}">embeddings_all-MiniLM-L6-v2.meta.json</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t02-2021-before/run_06_17_T02_5_orig_08_20_tp_X.py' | relative_url }}">run_06_17_T02_5_orig_08_20_tp_X.py</a></td><td>原始實驗輸出</td></tr></tbody></table>
</section>
</div>
