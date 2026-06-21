---
title: M01-8 最佳平衡
description: M01-8 歷史主程式的 最佳平衡 BERTopic 結果。
---

# M01-8｜最佳平衡

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok(para12-80)_dataset</code></td></tr>
<tr><td>選擇依據</td><td>符合指定最佳平衡條件後取最高 balance_score。</td></tr>
<tr><td>Embedding</td><td><code>all-MiniLM-L6-v2</code></td></tr>
<tr><td>UMAP</td><td>neighbors 5 / components 5 / min dist 0.0 / cosine</td></tr>
<tr><td>HDBSCAN</td><td>cluster 50 / samples 5 / eom / eps 0.2</td></tr>
</tbody></table>

### 停用詞與命名

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>停用詞來源</td><td><a href="{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}">A05-8.4 human</a></td></tr>
<tr><td>客製停用詞</td><td>170 個；合併英文停用詞共 462 個</td></tr>
<tr><td>LLM Provider</td><td>OpenRouter</td></tr>
<tr><td>LLM models</td><td>anthropic/claude-opus-4.7 / openai/gpt-5.5 / google/gemini-3.1-pro-preview</td></tr>
</tbody></table>

### 導覽

<p><a href="{{ '/results/m01-8-historical.html' | relative_url }}">回到 M01 三策略總覽</a></p>
</aside>

<section markdown="1">
<aside class="table-note"><strong>歷史比較用途：</strong>此頁對應資料夾「M01主程式（三參數-廢用）」。保留它是為了追溯三種策略與 A05-8.4 human 停用詞導入後的結果，不作為後續 M02 正式模型的唯一依據。</aside>

<div class="run-summary">
<div class="run-stat"><strong>51</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>19.58%</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>19.12%</strong><span>最大主題比例</span></div>
<div class="run-stat"><strong>0.8313</strong><span>balance score</span></div>
</div>

## 結果摘要

依既定平衡條件與 balance score 選取，兼顧離群、集中度與主題數。 本次使用 11,136 句資料，並重用 A04-8 的 embedding 快取。A05-8.4 human 停用詞僅作用於 c-TF-IDF 與主題表徵；embedding 與 HDBSCAN 分群仍使用原始 orig 文本向量。

## 與 A04 基準的對照

<div class="table-scroll"><table class="m01-baseline-table"><thead><tr><th>指標</th><th>A04 基準</th><th>M01 結果</th></tr></thead><tbody><tr><td>有效主題數</td><td>62</td><td>51</td></tr><tr><td>noise ratio</td><td>27.68%</td><td>19.58%</td></tr><tr><td>最大主題比例</td><td>4.07%</td><td>19.12%</td></tr><tr><td>前三主題比例</td><td>10.61%</td><td>26.32%</td></tr><tr><td>balance score</td><td>0.8835</td><td>0.8313</td></tr></tbody></table></div>

## 主題語意與 LLM 命名

<p class="section-intro">分群結果在各表徵方法之間相同；下表以 Default 的代表詞搭配 Claude 與 Gemini 命名，供檢視命名是否有助於主題判讀。僅先列前 10 個有效主題，完整輸出保留在下方。</p>
<div class="table-scroll"><table class="semantic-table m01-topic-table"><thead><tr><th>主題</th><th>句數</th><th>Default 代表詞</th><th>Claude 命名</th><th>Gemini 命名</th></tr></thead><tbody><tr><td>0</td><td>2,129</td><td>car, new, design, cars, customers, look, product, different, world, brand</td><td>EV Ownership Experience</td><td>General</td></tr><tr><td>1</td><td>442</td><td>interior, seat, seats, leather, space, rear, materials, design, comfort, feel</td><td>Interior and Seat Design</td><td>Interior</td></tr><tr><td>2</td><td>360</td><td>charging, charge, range, charger, minutes, hour, fast, battery, volt, level</td><td>EV Charging and Range</td><td>EV</td></tr><tr><td>3</td><td>277</td><td>electric, torque, hybrid, motor, pedal, power, battery, engine, electric motor, drive</td><td>Hybrid Powertrain Motor Torque</td><td>Electric</td></tr><tr><td>4</td><td>245</td><td>bmw, series, grand tour, tour, grand, bmw series, new bmw, kidney, new, i4</td><td>BMW vehicle features and dealerships</td><td>BMW</td></tr><tr><td>5</td><td>245</td><td>sonata, hyundai, hyundai sonata, safety, elantra, features, xc40, xc40 recharge, camry, recharge</td><td>Vehicle Safety Features and Ratings</td><td>Hyundai</td></tr><tr><td>6</td><td>229</td><td>volvo, xc90, s60, new xc90, new, ex90, safety, world, car, new s60</td><td>Volvo XC90 and S60 Reviews</td><td>Volvo</td></tr><tr><td>7</td><td>221</td><td>assist, parking, lane, spot, blind, blind spot, alert, traffic, driver, braking</td><td>Driver Assistance and Parking Features</td><td>Advanced</td></tr><tr><td>8</td><td>219</td><td>ioniq, hyundai, charging, electric, platform, vehicle, rear, 2025, interior, assist</td><td>Hyundai IONIQ EV Lineup</td><td>Hyundai</td></tr><tr><td>9</td><td>218</td><td>kia, ev6, ev, india, gt, new kia, niro, ev6 gt, ev9, fleet</td><td>BYD E6 and Kia EV6 Models</td><td>Kia</td></tr></tbody></table></div>

## 表徵方法與錯誤紀錄

<div class="table-scroll"><table class="m01-representation-table"><thead><tr><th>表徵／命名方式</th><th>狀態</th><th>完整輸出</th></tr></thead><tbody><tr><td>Default c-TF-IDF</td><td>完成</td><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_default.csv' | relative_url }}">topic info</a></td></tr><tr><td>KeyBERT-Inspired</td><td>完成</td><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_keybert.csv' | relative_url }}">topic info</a></td></tr><tr><td>Part-of-Speech</td><td>完成</td><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_pos.csv' | relative_url }}">topic info</a></td></tr><tr><td>MMR</td><td>完成</td><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_mmr.csv' | relative_url }}">topic info</a></td></tr><tr><td>Claude Opus 4.7</td><td>完成</td><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_llm_anthropic_claude_opus_4_7.csv' | relative_url }}">topic info</a></td></tr><tr><td>GPT-5.5</td><td>4 個 topic 命名失敗</td><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_llm_openai_gpt_5_5.csv' | relative_url }}">topic info</a></td></tr><tr><td>Gemini 3.1 Pro Preview</td><td>完成</td><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_llm_google_gemini_3_1_pro_preview.csv' | relative_url }}">topic info</a></td></tr></tbody></table></div><aside class="table-note"><strong>LLM 命名狀態：</strong>GPT-5.5 在此策略有 4 個 topic 因 API 回應缺值而未取得名稱；完整錯誤紀錄見 <a href="{{ '/assets/results/m01-8-historical/best_balance/representation_errors.json' | relative_url }}">representation_errors.json</a>。</aside>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/final_config.json' | relative_url }}">final_config.json</a></td><td>此策略的 UMAP、HDBSCAN、停用詞與表徵模型設定</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_size_distribution.csv' | relative_url }}">topic_size_distribution.csv</a></td><td>各 topic 的句數與比例</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/representative_docs.csv' | relative_url }}">representative_docs.csv</a></td><td>各主題的代表文本</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info.csv' | relative_url }}">topic_info.csv</a></td><td>預設主題資訊</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_words.csv' | relative_url }}">topic_words.csv</a></td><td>預設主題詞</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/representation_errors.json' | relative_url }}">representation_errors.json</a></td><td>LLM 命名與表徵失敗紀錄</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_default.csv' | relative_url }}">topic_info_default.csv</a></td><td>Default c-TF-IDF 的主題表徵或命名輸出</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_keybert.csv' | relative_url }}">topic_info_keybert.csv</a></td><td>KeyBERT-Inspired 的主題表徵或命名輸出</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_pos.csv' | relative_url }}">topic_info_pos.csv</a></td><td>Part-of-Speech 的主題表徵或命名輸出</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_mmr.csv' | relative_url }}">topic_info_mmr.csv</a></td><td>MMR 的主題表徵或命名輸出</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_llm_anthropic_claude_opus_4_7.csv' | relative_url }}">topic_info_llm_anthropic_claude_opus_4_7.csv</a></td><td>Claude Opus 4.7 的主題表徵或命名輸出</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_llm_openai_gpt_5_5.csv' | relative_url }}">topic_info_llm_openai_gpt_5_5.csv</a></td><td>GPT-5.5 的主題表徵或命名輸出</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/best_balance/topic_info_llm_google_gemini_3_1_pro_preview.csv' | relative_url }}">topic_info_llm_google_gemini_3_1_pro_preview.csv</a></td><td>Gemini 3.1 Pro Preview 的主題表徵或命名輸出</td></tr></tbody></table>
</section>
</div>
