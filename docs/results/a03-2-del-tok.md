---
title: A03-2 del tok min_cluster_size 掃描
description: del + tokenizer 資料集的 HDBSCAN min_cluster_size 敏感度分析。
experiment_id: a03-2-del-tok
---

# A03-2｜min_cluster_size 掃描

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
<div class="run-summary">
  <div class="run-stat"><strong>21</strong><span>測試參數組數</span></div>
  <div class="run-stat"><strong>100</strong><span>自動選擇值</span></div>
  <div class="run-stat"><strong>2.18%</strong><span>該設定 noise ratio</span></div>
  <div class="run-stat"><strong>2</strong><span>非 noise 主題數</span></div>
</div>

## 結果摘要

本實驗以固定的 embedding 與 UMAP 結果，測試 21 組 `min_cluster_size`。程式的自動選擇規則為：先保留至少兩個非 noise 主題的結果，再選擇 noise ratio 最低者；若相同，再選擇主題較多、參數較小者。

> **判讀提醒：** `min_cluster_size=100` 雖有最低的 noise ratio（2.18%），但 97.42% 的句子被歸到同一個主題。它應視為「依既定規則選出的候選值」，尚不能當成語意區辨性最佳的最終模型。

### 圖表檢視

<div class="result-figure-scroller" aria-label="A03-2 min_cluster_size 圖表檢視">
  <figure>
    <img src="{{ '/assets/results/a03-2-del-tok/a03-2-min-en.png' | relative_url }}" alt="A03-2 del tok min cluster size 掃描圖英文版">
    <figcaption>英文版：A03-2 個別參數掃描結果</figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/results/a03-2-del-tok/a03-2-min-zh.png' | relative_url }}" alt="A03-2 del tok min cluster size 掃描圖中文版">
    <figcaption>中文版：A03-2 個別參數掃描結果</figcaption>
  </figure>
</div>

## 參數掃描結果

<div class="table-scroll">
<table class="scan-table">
  <thead><tr><th>min cluster size</th><th>非 noise 主題數</th><th>noise ratio</th><th>離群句數</th><th>主題 0</th><th>主題 1</th><th>判讀</th></tr></thead>
  <tbody>
    <tr><td>50</td><td>84</td><td>50.77%</td><td>15,979</td><td>100</td><td>53</td><td></td></tr>
    <tr><td>75</td><td>53</td><td>52.55%</td><td>16,540</td><td>100</td><td>85</td><td></td></tr>
    <tr class="selection-row"><td>100</td><td>2</td><td>2.18%</td><td>687</td><td>30,663</td><td>124</td><td><span class="scan-badge">自動選擇：最低雜訊</span></td></tr>
    <tr><td>125</td><td>28</td><td>54.50%</td><td>17,153</td><td>214</td><td>146</td><td></td></tr>
    <tr><td>150</td><td>16</td><td>48.59%</td><td>15,293</td><td>219</td><td>4,429</td><td></td></tr>
    <tr><td>175</td><td>15</td><td>51.08%</td><td>16,076</td><td>218</td><td>4,454</td><td></td></tr>
    <tr><td>200</td><td>14</td><td>53.80%</td><td>16,933</td><td>205</td><td>4,453</td><td></td></tr>
    <tr><td>225</td><td>2</td><td>11.70%</td><td>3,683</td><td>4,743</td><td>23,048</td><td></td></tr>
    <tr><td>250</td><td>11</td><td>55.19%</td><td>17,369</td><td>4,178</td><td>738</td><td></td></tr>
    <tr><td>275</td><td>2</td><td>13.15%</td><td>4,138</td><td>4,676</td><td>22,660</td><td></td></tr>
    <tr><td>300</td><td>2</td><td>13.82%</td><td>4,350</td><td>4,622</td><td>22,502</td><td></td></tr>
    <tr><td>325</td><td>2</td><td>14.39%</td><td>4,530</td><td>4,584</td><td>22,360</td><td></td></tr>
    <tr><td>350</td><td>2</td><td>14.74%</td><td>4,639</td><td>4,582</td><td>22,253</td><td></td></tr>
    <tr><td>375</td><td>2</td><td>15.15%</td><td>4,768</td><td>4,562</td><td>22,144</td><td></td></tr>
    <tr><td>400</td><td>2</td><td>15.40%</td><td>4,848</td><td>4,551</td><td>22,075</td><td></td></tr>
    <tr><td>500</td><td>2</td><td>17.79%</td><td>5,600</td><td>4,430</td><td>21,444</td><td></td></tr>
    <tr><td>600</td><td>2</td><td>22.08%</td><td>6,949</td><td>4,233</td><td>20,292</td><td></td></tr>
    <tr><td>700</td><td>2</td><td>22.34%</td><td>7,031</td><td>4,149</td><td>20,294</td><td></td></tr>
    <tr><td>800</td><td>2</td><td>22.49%</td><td>7,077</td><td>4,103</td><td>20,294</td><td></td></tr>
    <tr><td>900</td><td>2</td><td>24.72%</td><td>7,781</td><td>3,911</td><td>19,782</td><td></td></tr>
    <tr><td>1000</td><td>2</td><td>23.31%</td><td>7,336</td><td>3,684</td><td>20,454</td><td></td></tr>
  </tbody>
</table>
</div>

## 自動選擇值的主題分布

<div class="table-scroll">
<table class="topic-table">
  <thead><tr><th>Topic</th><th>句數</th><th>比例</th><th>前十個代表詞</th></tr></thead>
  <tbody>
    <tr><td>-1（noise）</td><td>687</td><td>2.18%</td><td>thank, thank thank, absolutely, crown, aria, okay, yeah, google, android, ex90</td></tr>
    <tr><td>0</td><td>30,663</td><td>97.42%</td><td>car, new, like, just, vehicle, really, electric, design, drive, driving</td></tr>
    <tr><td>1</td><td>124</td><td>0.39%</td><td>warranty, 000, 000 mile, mile, year, whichever, whichever comes, years, 000 miles, 100 000</td></tr>
  </tbody>
</table>
</div>

Topic 0 的代表句同時涵蓋車輛設計、電動車、駕駛感受等多種內容，因此目前較接近「一般汽車產品敘述」的寬泛集合。後續應以代表詞、代表句與主題大小的平衡性，人工比較候選設定，而非只降低離群比例。

## 後續判讀方向

1. 優先人工比較 `50`、`75`、`125`、`150` 的代表詞與代表句，確認多群結果是否具有可解釋性。
2. 以「最大主題比例、主題數、noise ratio、代表句一致性」建立複合選擇規則。
3. 另測排除少於 3 或 5 words 的短句，檢查短句是否改變密度分群與離群比例。

## 來源檔案與下載

| 檔案 | 用途 |
| --- | --- |
| [參數掃描 CSV]({{ '/assets/results/a03-2-del-tok/Result_06.03_A03-2(del)_tok-min_cluster_size.csv' | relative_url }}) | 21 組參數的完整統計 |
| [主題摘要 CSV]({{ '/assets/results/a03-2-del-tok/Result_06.03_A03-2(del)_tok-best_topic_info.csv' | relative_url }}) | 自動選擇值的 topic 關鍵詞與代表句 |
| [句子－主題對照 CSV]({{ '/assets/results/a03-2-del-tok/Result_06.03_A03-2(del)_tok-best_document_topics.csv' | relative_url }}) | 31,474 筆完整句子指派結果 |
| [實驗報告 Markdown]({{ '/assets/results/a03-2-del-tok/Result_06.03_A03-2(del)_tok.md' | relative_url }}) | 原始執行報告 |
| [run log JSON]({{ '/assets/results/a03-2-del-tok/Result_06.03_A03-2(del)_tok-run_log.json' | relative_url }}) | 機器可讀的執行紀錄與選擇規則 |
| [執行程式 Python]({{ '/assets/results/a03-2-del-tok/run_06.03_A03_2_del_tok.py' | relative_url }}) | 可重現的實驗程式 |

</section>
</div>
