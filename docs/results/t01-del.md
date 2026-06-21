---
title: T01-3｜刪除品牌／車款
description: T01 品牌與車款文字處理驗證：del。
---

# T01-3｜刪除品牌／車款

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料與模型

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>Result/06.03_A02/R06.03_A02-pre_LLM(del)_tok(para12-80)_dataset</code></td></tr>
<tr><td>可用句子</td><td>10,945</td></tr>
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

<p><code>#運行BERTopic整理/#7.1 T01刪&移廠商、模型與原版的比較（未整理）/06.08_Test1-1(del-new-tp-X)</code></p>

<p><a href="{{ '/results/t01-overview.html' | relative_url }}">回到 T01 刪除／替換驗證總覽</a></p>
</aside>

<section markdown="1">
<div class="run-summary">
<div class="run-stat"><strong>14</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>30.27%</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>23.03%</strong><span>最大主題比例</span></div>
<div class="run-stat"><strong>0.647</strong><span>balance score</span></div>
</div>

## 結果摘要

將品牌與車款名稱從資料集中刪除，檢查移除專有名詞後主題結構的變化。 此頁用來與原始語料及另一種處理方式比較，判讀品牌／車款名稱是否主導主題結構。

<aside class="table-note"><strong>LLM50 未執行：</strong>本次分群與 Default、KeyBERT、POS、MMR 表徵皆已輸出；但當時未提供 <code>OPENROUTER_API_KEY</code>，因此 LLM topic label 與 50 次穩定性驗證被跳過。這不是「0 個穩定主題」，而是沒有可判定的 LLM 驗證結果。</aside>

## 預設主題語意摘要

<p class="section-intro">以下列出前 10 個有效主題的 Default c-TF-IDF 代表詞；可作為檢查刪除或替換後是否仍殘留品牌／車款語意的起點。</p>

<div class="table-scroll"><table class="semantic-table"><thead><tr><th>Topic</th><th>句數</th><th>Default 代表詞（前 10）</th></tr></thead><tbody><tr><td>0</td><td>2,521</td><td>car, new, design, electric, rear, interior, vehicle, seats, cars, look</td></tr><tr><td>1</td><td>1,668</td><td>charging, hybrid, electric, battery, charge, drive, engine, range, power, horsepower</td></tr><tr><td>2</td><td>1,560</td><td>assist, safety, control, steering, available, car, driver, features, display, standard</td></tr><tr><td>3</td><td>742</td><td>ladies, auto, president, new, vice, vice president, hello, press, excited, happy</td></tr><tr><td>4</td><td>312</td><td>brand, design, products, new, product, customers, customer, best, designers, clay</td></tr><tr><td>5</td><td>147</td><td>black, available, standard, 19, grade, led, trd, 18, nightshade, 20</td></tr><tr><td>6</td><td>115</td><td>door, trunk, rear, open, tailgate, pull, release, cover, cargo, place</td></tr><tr><td>7</td><td>114</td><td>amg, gt, performance, racing, gt3, new, coupe, race, car, door</td></tr><tr><td>8</td><td>100</td><td>class, new class, new, luxury, car, customers, high, best, class new, quality</td></tr><tr><td>9</td><td>89</td><td>sound, noise, quiet, acoustic, car, engine, silent, sounds, wind, quietness</td></tr></tbody></table></div>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X).md' | relative_url }}">06.08_Test1-1(del-new-tp-X).md</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X)_LLM.csv' | relative_url }}">06.08_Test1-1(del-new-tp-X)_LLM.csv</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X)_LLM.md' | relative_url }}">06.08_Test1-1(del-new-tp-X)_LLM.md</a></td><td>LLM 命名輸出或驗證報告</td></tr><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X)_LLM_detail.csv' | relative_url }}">06.08_Test1-1(del-new-tp-X)_LLM_detail.csv</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X)_LLM_validation.csv' | relative_url }}">06.08_Test1-1(del-new-tp-X)_LLM_validation.csv</a></td><td>LLM50 驗證輸出；本次因 API key 缺失而跳過</td></tr><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X)_LLM_validation.md' | relative_url }}">06.08_Test1-1(del-new-tp-X)_LLM_validation.md</a></td><td>LLM50 驗證輸出；本次因 API key 缺失而跳過</td></tr><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X)_combined_representations.csv' | relative_url }}">06.08_Test1-1(del-new-tp-X)_combined_representations.csv</a></td><td>Default、KeyBERT、POS、MMR 與 LLM 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X)_combined_representations.md' | relative_url }}">06.08_Test1-1(del-new-tp-X)_combined_representations.md</a></td><td>Default、KeyBERT、POS、MMR 與 LLM 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X)_combined_representations_with_docs.csv' | relative_url }}">06.08_Test1-1(del-new-tp-X)_combined_representations_with_docs.csv</a></td><td>Default、KeyBERT、POS、MMR 與 LLM 表徵對照</td></tr><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X)_custom_stopwords_used.txt' | relative_url }}">06.08_Test1-1(del-new-tp-X)_custom_stopwords_used.txt</a></td><td>本次實際使用的客製停用詞</td></tr><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X)_run_log.json' | relative_url }}">06.08_Test1-1(del-new-tp-X)_run_log.json</a></td><td>執行資料、停用詞與錯誤紀錄</td></tr><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X)_run_summary.json' | relative_url }}">06.08_Test1-1(del-new-tp-X)_run_summary.json</a></td><td>模型量化結果摘要</td></tr><tr><td><a href="{{ '/assets/results/t01-del/06.08_Test1-1(del-new-tp-X)_summary.csv' | relative_url }}">06.08_Test1-1(del-new-tp-X)_summary.csv</a></td><td>模型量化結果摘要 CSV</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/final_config.json' | relative_url }}">artifacts/final_config.json</a></td><td>最終模型與 LLM 設定</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/representation_errors.json' | relative_url }}">artifacts/representation_errors.json</a></td><td>表徵與 LLM 命名錯誤紀錄</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/representative_docs.csv' | relative_url }}">artifacts/representative_docs.csv</a></td><td>各主題代表文本</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/topic_info.csv' | relative_url }}">artifacts/topic_info.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/topic_info_default.csv' | relative_url }}">artifacts/topic_info_default.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/topic_info_keybert.csv' | relative_url }}">artifacts/topic_info_keybert.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/topic_info_mmr.csv' | relative_url }}">artifacts/topic_info_mmr.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/topic_info_pos.csv' | relative_url }}">artifacts/topic_info_pos.csv</a></td><td>主題資訊與表徵輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/topic_size_distribution.csv' | relative_url }}">artifacts/topic_size_distribution.csv</a></td><td>主題大小分布</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/topic_words.csv' | relative_url }}">artifacts/topic_words.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/topic_words_default.csv' | relative_url }}">artifacts/topic_words_default.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/topic_words_keybert.csv' | relative_url }}">artifacts/topic_words_keybert.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/topic_words_mmr.csv' | relative_url }}">artifacts/topic_words_mmr.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/artifacts/topic_words_pos.csv' | relative_url }}">artifacts/topic_words_pos.csv</a></td><td>主題代表詞輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/embeddings_all-MiniLM-L6-v2.meta.json' | relative_url }}">embeddings_all-MiniLM-L6-v2.meta.json</a></td><td>原始實驗輸出</td></tr><tr><td><a href="{{ '/assets/results/t01-del/run_06_08_Test1_1_del_new_tp_X.py' | relative_url }}">run_06_08_Test1_1_del_new_tp_X.py</a></td><td>原始實驗輸出</td></tr></tbody></table>
</section>
</div>
