---
title: M01-8 三策略主程式
description: M01-8 歷史主程式的三種 BERTopic 策略比較。
---

# M01-8｜三策略主程式

<div class="table-note" role="note"><strong>歷史比較用途：</strong>本頁整理「M01主程式（三參數-廢用）」中唯一完整的 M01-8 實驗。保留其資料來源、三種策略、停用詞與 LLM 命名結果，供研究追溯；它不取代後續 M02 的正式單一參數模型。</div>

<div class="m01-strategy-links"><a class="m01-strategy-link candidate-lowest_noise" href="{{ '/results/m01-8-lowest-noise.html' | relative_url }}"><strong>最低雜訊</strong><span>以最低 noise ratio 為優先，觀察離群句是否最少。</span></a><a class="m01-strategy-link candidate-most_topics" href="{{ '/results/m01-8-most-topics.html' | relative_url }}"><strong>最多主題</strong><span>以保留最多有效主題為優先，保留較細的主題切分。</span></a><a class="m01-strategy-link candidate-best_balance" href="{{ '/results/m01-8-best-balance.html' | relative_url }}"><strong>最佳平衡</strong><span>依既定平衡條件與 balance score 選取，兼顧離群、集中度與主題數。</span></a></div>

## 運行設定

<div class="run-summary">
<div class="run-stat"><strong>11,136</strong><span>使用句子</span></div>
<div class="run-stat"><strong>170</strong><span>A05-8.4 human 客製停用詞</span></div>
<div class="run-stat"><strong>462</strong><span>合併英文停用詞總數</span></div>
<div class="run-stat"><strong>7</strong><span>主題表徵／命名方式</span></div>
</div>

資料使用 <code>Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok(para12-80)_dataset</code>，重用 A04-8 的 <code>all-MiniLM-L6-v2</code> embedding 快取。客製停用詞取自 <a href="{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}">A05-8.4 human</a>；它只影響 c-TF-IDF／主題表徵，並不改變 embedding 或 HDBSCAN 分群輸入。

## 三策略比較

<div class="table-scroll"><table class="candidate-table m01-strategy-table"><thead><tr>
<th>策略</th><th>選擇方式</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>前三主題比例</th><th>balance score</th><th>LLM 命名失敗</th>
</tr></thead><tbody><tr class="candidate-lowest_noise"><td><a href="{{ '/results/m01-8-lowest-noise.html' | relative_url }}">最低雜訊</a></td><td>以最低 noise ratio 為優先，觀察離群句是否最少。</td><td>4</td><td>10.29%</td><td>77.70%</td><td>87.28%</td><td>0.3935</td><td>1</td></tr><tr class="candidate-most_topics"><td><a href="{{ '/results/m01-8-most-topics.html' | relative_url }}">最多主題</a></td><td>以保留最多有效主題為優先，保留較細的主題切分。</td><td>70</td><td>29.74%</td><td>3.36%</td><td>7.54%</td><td>0.8856</td><td>7</td></tr><tr class="candidate-best_balance"><td><a href="{{ '/results/m01-8-best-balance.html' | relative_url }}">最佳平衡</a></td><td>依既定平衡條件與 balance score 選取，兼顧離群、集中度與主題數。</td><td>51</td><td>19.58%</td><td>19.12%</td><td>26.32%</td><td>0.8313</td><td>4</td></tr></tbody></table></div>

<div class="table-note" role="note"><strong>如何判讀：</strong>最低雜訊策略雖使離群句較少，但最大主題高度集中；最多主題策略的 balance score 最高，但 LLM 命名失敗也較多；最佳平衡策略則在較低雜訊與 51 個主題之間取得另一種取捨。三者均保留，供語意品質的人工檢閱。</div>

## 資料與原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody>
<tr><td><a href="{{ '/assets/results/m01-8-historical/M01-8_comparison_summary.csv' | relative_url }}">M01-8_comparison_summary.csv</a></td><td>三種策略的量化比較摘要</td></tr>
<tr><td><a href="{{ '/assets/results/m01-8-historical/M01-8_run_log.json' | relative_url }}">M01-8_run_log.json</a></td><td>資料、停用詞、embedding 快取與 LLM 執行紀錄</td></tr>
<tr><td><a href="{{ '/assets/results/m01-8-historical/M01-8_custom_stopwords_used.txt' | relative_url }}">M01-8_custom_stopwords_used.txt</a></td><td>本次實際使用的客製停用詞清單</td></tr>
<tr><td><a href="{{ '/assets/results/m01-8-historical/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py' | relative_url }}">執行程式</a></td><td>M01-8 主程式與表徵模型執行流程</td></tr>
</tbody></table>
