---
title: M01-8 最多主題
description: M01-8 歷史主程式的 最多主題 BERTopic 結果。
experiment_id: m01-8-most-topics
---

# M01-8｜最多主題

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
<aside class="table-note"><strong>歷史比較用途：</strong>此頁對應資料夾「M01主程式（三參數-廢用）」。保留它是為了追溯三種策略與 A05-8.4 human 停用詞導入後的結果，不作為後續 M02 正式模型的唯一依據。</aside>

<div class="run-summary">
<div class="run-stat"><strong>70</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>29.74%</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>3.36%</strong><span>最大主題比例</span></div>
<div class="run-stat"><strong>0.8856</strong><span>balance score</span></div>
</div>

## 結果摘要

以保留最多有效主題為優先，保留較細的主題切分。 本次使用 11,136 句資料，並重用 A04-8 的 embedding 快取。A05-8.4 human 停用詞僅作用於 c-TF-IDF 與主題表徵；embedding 與 HDBSCAN 分群仍使用原始 orig 文本向量。

## 與 A04 基準的對照

<div class="table-scroll"><table class="m01-baseline-table"><thead><tr><th>指標</th><th>A04 基準</th><th>M01 結果</th></tr></thead><tbody><tr><td>有效主題數</td><td>73</td><td>70</td></tr><tr><td>noise ratio</td><td>33.37%</td><td>29.74%</td></tr><tr><td>最大主題比例</td><td>2.86%</td><td>3.36%</td></tr><tr><td>前三主題比例</td><td>6.63%</td><td>7.54%</td></tr><tr><td>balance score</td><td>0.8781</td><td>0.8856</td></tr></tbody></table></div>

## 主題語意與 LLM 命名

<p class="section-intro">分群結果在各表徵方法之間相同；下表以 Default 的代表詞搭配 Claude 與 Gemini 命名，供檢視命名是否有助於主題判讀。僅先列前 10 個有效主題，完整輸出保留在下方。</p>
<div class="table-scroll"><table class="semantic-table m01-topic-table"><thead><tr><th>主題</th><th>句數</th><th>Default 代表詞</th><th>Claude 命名</th><th>Gemini 命名</th></tr></thead><tbody><tr><td>0</td><td>374</td><td>ladies, interesting, fun, congratulations, moment, broadcast, liked, able, answer, enjoy</td><td>Casual Conversation Filler</td><td>Convers</td></tr><tr><td>1</td><td>245</td><td>bmw, series, grand tour, tour, grand, bmw series, new bmw, kidney, new, i4</td><td>BMW Vehicle Features and Design</td><td>BMW</td></tr><tr><td>2</td><td>221</td><td>assist, parking, lane, spot, blind, blind spot, alert, traffic, braking, driver</td><td>Driver Assistance and Parking Features</td><td>Advanced</td></tr><tr><td>3</td><td>220</td><td>car, cars, customers, design, vehicle, prototypes, world, mobility, experience, lives</td><td>Driving Experience and Enjoyment</td><td>Advanced</td></tr><tr><td>4</td><td>219</td><td>ioniq, hyundai, charging, platform, electric, vehicle, 2025, rear, ev, assist</td><td>Hyundai IONIQ EV Lineup</td><td>Hyundai</td></tr><tr><td>5</td><td>218</td><td>kia, ev6, ev, india, new kia, gt, niro, ev6 gt, ev9, fleet</td><td>Kia and BYD EV Models</td><td>Kia</td></tr><tr><td>6</td><td>204</td><td>nissan, leaf, nissan leaf, aria, new nissan, altima, propilot, new, nissan intelligent, intelligent</td><td>Nissan Leaf and ProPilot</td><td>Nissan</td></tr><tr><td>7</td><td>203</td><td>seat, leather, seats, interior, materials, comfort, trim, space, upholstery, comfortable</td><td>EV Interior Seats and Materials</td><td>Premium</td></tr><tr><td>8</td><td>188</td><td>carplay, apple, android, apple carplay, android auto, smartphone, phone, alexa, auto, touchscreen</td><td>Smartphone Integration and Infotainment</td><td>Smartphone</td></tr><tr><td>9</td><td>185</td><td>mbux, screen, display, console, center console, center, control, buttons, digital, functions</td><td>MBUX Hyperscreen Infotainment Display</td><td>Inf</td></tr></tbody></table></div>

## 表徵方法與錯誤紀錄

<div class="table-scroll"><table class="m01-representation-table"><thead><tr><th>表徵／命名方式</th><th>狀態</th><th>完整輸出</th></tr></thead><tbody><tr><td>Default c-TF-IDF</td><td>完成</td><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_default.csv' | relative_url }}">topic info</a></td></tr><tr><td>KeyBERT-Inspired</td><td>完成</td><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_keybert.csv' | relative_url }}">topic info</a></td></tr><tr><td>Part-of-Speech</td><td>完成</td><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_pos.csv' | relative_url }}">topic info</a></td></tr><tr><td>MMR</td><td>完成</td><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_mmr.csv' | relative_url }}">topic info</a></td></tr><tr><td>Claude Opus 4.7</td><td>完成</td><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_llm_anthropic_claude_opus_4_7.csv' | relative_url }}">topic info</a></td></tr><tr><td>GPT-5.5</td><td>7 個 topic 命名失敗</td><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_llm_openai_gpt_5_5.csv' | relative_url }}">topic info</a></td></tr><tr><td>Gemini 3.1 Pro Preview</td><td>完成</td><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_llm_google_gemini_3_1_pro_preview.csv' | relative_url }}">topic info</a></td></tr></tbody></table></div><aside class="table-note"><strong>LLM 命名狀態：</strong>GPT-5.5 在此策略有 7 個 topic 因 API 回應缺值而未取得名稱；完整錯誤紀錄見 <a href="{{ '/assets/results/m01-8-historical/most_topics/representation_errors.json' | relative_url }}">representation_errors.json</a>。</aside>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/final_config.json' | relative_url }}">final_config.json</a></td><td>此策略的 UMAP、HDBSCAN、停用詞與表徵模型設定</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_size_distribution.csv' | relative_url }}">topic_size_distribution.csv</a></td><td>各 topic 的句數與比例</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/representative_docs.csv' | relative_url }}">representative_docs.csv</a></td><td>各主題的代表文本</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info.csv' | relative_url }}">topic_info.csv</a></td><td>預設主題資訊</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_words.csv' | relative_url }}">topic_words.csv</a></td><td>預設主題詞</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/representation_errors.json' | relative_url }}">representation_errors.json</a></td><td>LLM 命名與表徵失敗紀錄</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_default.csv' | relative_url }}">topic_info_default.csv</a></td><td>Default c-TF-IDF 的主題表徵或命名輸出</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_keybert.csv' | relative_url }}">topic_info_keybert.csv</a></td><td>KeyBERT-Inspired 的主題表徵或命名輸出</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_pos.csv' | relative_url }}">topic_info_pos.csv</a></td><td>Part-of-Speech 的主題表徵或命名輸出</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_mmr.csv' | relative_url }}">topic_info_mmr.csv</a></td><td>MMR 的主題表徵或命名輸出</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_llm_anthropic_claude_opus_4_7.csv' | relative_url }}">topic_info_llm_anthropic_claude_opus_4_7.csv</a></td><td>Claude Opus 4.7 的主題表徵或命名輸出</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_llm_openai_gpt_5_5.csv' | relative_url }}">topic_info_llm_openai_gpt_5_5.csv</a></td><td>GPT-5.5 的主題表徵或命名輸出</td></tr><tr><td><a href="{{ '/assets/results/m01-8-historical/most_topics/topic_info_llm_google_gemini_3_1_pro_preview.csv' | relative_url }}">topic_info_llm_google_gemini_3_1_pro_preview.csv</a></td><td>Gemini 3.1 Pro Preview 的主題表徵或命名輸出</td></tr></tbody></table>
</section>
</div>
