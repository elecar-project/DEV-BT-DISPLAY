---
title: T01-6｜替換品牌／車款
description: T01 品牌與車款文字處理驗證：repl。
---

# T01-6｜替換品牌／車款

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料與模型

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>Result/06.03_A02/R06.03_A02-pre_LLM(repl)_tok(para12-80)_dataset</code></td></tr>
<tr><td>可用句子</td><td>10,978</td></tr>
<tr><td>Embedding</td><td><code>all-MiniLM-L6-v2</code></td></tr>
<tr><td>UMAP</td><td>neighbors 10 / components 15 / min dist 0.0 / cosine</td></tr>
<tr><td>HDBSCAN</td><td>cluster 50 / samples 5 / eom / eps 0.2</td></tr>
<tr><td>Topic reduction</td><td><code>nr_topics=auto</code></td></tr>
</tbody></table>

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>停用詞</td><td><a href="{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}">A05-8.4 human</a>，客製 170 個</td></tr>
<tr><td>LLM 設計</td><td>OpenRouter / <code>openai/gpt-5.5</code>，每 topic 50 次</td></tr>
<tr><td>代表句</td><td>6 句 / topic</td></tr>
</tbody></table>

### 來源資料夾

<p><code>#運行BERTopic整理/#7.1 T01刪&移廠商、模型與原版的比較（未整理）/06.08_Test1-2(repl-new-tp-X)</code></p>

<p><a href="{{ '/results/t01-overview.html' | relative_url }}">回到 T01 刪除／替換驗證總覽</a></p>
</aside>

<section markdown="1">
<div class="run-summary">
<div class="run-stat"><strong>29</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>32.02%</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>8.07%</strong><span>最大主題比例</span></div>
<div class="run-stat"><strong>0.838</strong><span>balance score</span></div>
</div>

## 結果摘要

將品牌與車款名稱分別替換為 Brand／Model，保留詞類位置但降低特定品牌名稱的主導性。 此頁用來與原始語料及另一種處理方式比較，判讀品牌／車款名稱是否主導主題結構。

<aside class="table-note"><strong>LLM50 未執行：</strong>本次分群與 Default、KeyBERT、POS、MMR 表徵皆已輸出；但當時未提供 <code>OPENROUTER_API_KEY</code>，因此 LLM topic label 與 50 次穩定性驗證被跳過。這不是「0 個穩定主題」，而是沒有可判定的 LLM 驗證結果。</aside>

## 預設主題語意摘要

<p class="section-intro">以下列出前 10 個有效主題的 Default c-TF-IDF 代表詞；可作為檢查刪除或替換後是否仍殘留品牌／車款語意的起點。</p>

<div class="table-scroll"><table class="semantic-table"><thead><tr><th>Topic</th><th>句數</th><th>Default 代表詞（前 10）</th></tr></thead><tbody><tr><td>0</td><td>886</td><td>brand, model, car, new, design, cars, customers, best, sedan, market</td></tr><tr><td>1</td><td>833</td><td>hybrid, engine, horsepower, electric, model, battery, torque, motor, range, liter</td></tr><tr><td>2</td><td>565</td><td>apple, audio, android, carplay, available, wireless, apple carplay, touchscreen, smartphone, connected</td></tr><tr><td>3</td><td>551</td><td>rear, grille, led, light, design, car, headlights, look, lights, line</td></tr><tr><td>4</td><td>541</td><td>electric, brand, ev, vehicles, model, vehicle, electric vehicle, new, electric car, car</td></tr><tr><td>5</td><td>520</td><td>assist, safety, lane, parking, spot, alert, collision, blind, blind spot, traffic</td></tr><tr><td>6</td><td>410</td><td>charging, charge, stations, fast, charger, level, dc, charging stations, volt, station</td></tr><tr><td>7</td><td>393</td><td>episode, everybody, talking, absolutely, afternoon, minutes, congratulations, moment, excited, able</td></tr><tr><td>8</td><td>340</td><td>seats, seat, space, rear, heated, cargo, rear seats, interior, leather, passengers</td></tr><tr><td>9</td><td>265</td><td>display, screen, mbux, information, navigation, displays, functions, control, driver, new</td></tr></tbody></table></div>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X).md' | relative_url }}">06.08_Test1-2(repl-new-tp-X).md</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X)_LLM.csv' | relative_url }}">06.08_Test1-2(repl-new-tp-X)_LLM.csv</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X)_LLM.md' | relative_url }}">06.08_Test1-2(repl-new-tp-X)_LLM.md</a></td><td>LLM 命名輸出或驗證報告</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X)_LLM_detail.csv' | relative_url }}">06.08_Test1-2(repl-new-tp-X)_LLM_detail.csv</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X)_LLM_validation.csv' | relative_url }}">06.08_Test1-2(repl-new-tp-X)_LLM_validation.csv</a></td><td>LLM50 驗證輸出；本次因 API key 缺失而跳過</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X)_LLM_validation.md' | relative_url }}">06.08_Test1-2(repl-new-tp-X)_LLM_validation.md</a></td><td>LLM50 驗證輸出；本次因 API key 缺失而跳過</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X)_combined_representations.csv' | relative_url }}">06.08_Test1-2(repl-new-tp-X)_combined_representations.csv</a></td><td>Default、KeyBERT、POS、MMR 與 LLM 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X)_combined_representations.md' | relative_url }}">06.08_Test1-2(repl-new-tp-X)_combined_representations.md</a></td><td>Default、KeyBERT、POS、MMR 與 LLM 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X)_combined_representations_with_docs.csv' | relative_url }}">06.08_Test1-2(repl-new-tp-X)_combined_representations_with_docs.csv</a></td><td>Default、KeyBERT、POS、MMR 與 LLM 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X)_custom_stopwords_used.txt' | relative_url }}">06.08_Test1-2(repl-new-tp-X)_custom_stopwords_used.txt</a></td><td>本次實際使用的客製停用詞</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X)_run_log.json' | relative_url }}">06.08_Test1-2(repl-new-tp-X)_run_log.json</a></td><td>執行資料、停用詞與錯誤紀錄</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X)_run_summary.json' | relative_url }}">06.08_Test1-2(repl-new-tp-X)_run_summary.json</a></td><td>模型量化結果摘要</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/06.08_Test1-2(repl-new-tp-X)_summary.csv' | relative_url }}">06.08_Test1-2(repl-new-tp-X)_summary.csv</a></td><td>模型量化結果摘要 CSV</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/final_config.json' | relative_url }}">artifacts/final_config.json</a></td><td>最終模型與 LLM 設定</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/representation_errors.json' | relative_url }}">artifacts/representation_errors.json</a></td><td>表徵與 LLM 命名錯誤紀錄</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/representative_docs.csv' | relative_url }}">artifacts/representative_docs.csv</a></td><td>各主題代表文本</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/topic_info.csv' | relative_url }}">artifacts/topic_info.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/topic_info_default.csv' | relative_url }}">artifacts/topic_info_default.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/topic_info_keybert.csv' | relative_url }}">artifacts/topic_info_keybert.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/topic_info_mmr.csv' | relative_url }}">artifacts/topic_info_mmr.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/topic_info_pos.csv' | relative_url }}">artifacts/topic_info_pos.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/topic_size_distribution.csv' | relative_url }}">artifacts/topic_size_distribution.csv</a></td><td>主題大小分布</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/topic_words.csv' | relative_url }}">artifacts/topic_words.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/topic_words_default.csv' | relative_url }}">artifacts/topic_words_default.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/topic_words_keybert.csv' | relative_url }}">artifacts/topic_words_keybert.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/topic_words_mmr.csv' | relative_url }}">artifacts/topic_words_mmr.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/artifacts/topic_words_pos.csv' | relative_url }}">artifacts/topic_words_pos.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/embeddings_all-MiniLM-L6-v2.meta.json' | relative_url }}">embeddings_all-MiniLM-L6-v2.meta.json</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-repl/run_06_08_Test1_2_repl_new_tp_X.py' | relative_url }}">run_06_08_Test1_2_repl_new_tp_X.py</a></td><td>原始實驗輸出</td></tr></tbody></table>
</section>
</div>
