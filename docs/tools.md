---
title: 工具
description: Release 檔案、工作流程分組與流程圖展示。
---

# 工具

本頁保留 DEV-BT 研究流程中最常用的工具入口與流程概覽。

## Release 檔案

可下載工具目前發布在母倉庫的 Release：

<https://github.com/elecar-project/DEV-BT/releases>

## 工作流程分組

| 階段 | 對應工具 | 研究用途 |
| --- | --- | --- |
| A. 音檔與 ASR 處理 | Audio V2A、Audio-tran、ASR-result、ASR-analysis、TXT Compare、TXT Delete | 取得逐字稿、檢查 ASR 品質、整理可用文本 |
| B. 資料清理與切分 | LLM Clean、TXTcp-2、TXT Filter、TXT Tokenizer、Pre-process Workbench | 清理逐字稿、建立資料集版本、切成 BERTopic 可用句子 |
| C. BERTopic 處理 | BERTopic Workbench、BERTopic Deploy、Min & Elbow、Batch | 訓練 topic model、調整參數、匯出主題結果 |

## 流程圖展示

<div class="figure-gallery">
  <figure>
    <img src="{{ '/assets/img/115.06.05_資料蒐集架構圖（詳細）_ver.3.drawio.png' | relative_url }}" alt="資料蒐集架構圖">
    <figcaption>
      <strong>圖 1｜資料蒐集架構圖（詳細）ver.3</strong>
      <span>資料來源、篩選、轉錄與前處理流程</span>
    </figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/img/115.06.05_BERTopic流程_ver.4_新增(產業與管理論壇).drawio.png' | relative_url }}" alt="BERTopic流程">
    <figcaption>
      <strong>圖 2｜BERTopic 主題建模流程</strong>
      <span>語意向量化、降維、分群、權重計算與主題命名</span>
    </figcaption>
  </figure>
</div>

## OpenRouter API 與 LLM

本研究在兩個位置透過 [OpenRouter API 文件](https://openrouter.ai/docs/api-reference/overview) 呼叫 LLM：逐字稿清理，以及 BERTopic 主題命名／穩定性檢驗。API key 僅從執行環境的 <code>OPENROUTER_API_KEY</code> 或工具輸入欄讀取；不應寫入資料集、報告或網站。

### 1. LLM-clean：補標點與清理逐字稿

對應工具：<code>#B1-4【資料清理與切分】(v0.4.1-0.4.4)/#B1(v0.4.1.0)LLM-clean【LLM補標點、清文本】_V0(exe)</code>。

LLM-clean 先處理 Whisper 逐字稿的標點、重複片段與明顯 ASR 雜訊；之後才由 <code>man-model.md</code> 詞表進行 deterministic 後處理，產出移除品牌／車款的 <code>del</code> 資料集，以及替換為 <code>Brand</code>／<code>Model</code> 的 <code>repl</code> 資料集。也就是說，LLM 不負責刪除或替換品牌與車款名稱。

<div class="table-scroll"><table class="m01-strategy-table"><thead><tr><th>項目</th><th>預設設定</th><th>用途</th></tr></thead><tbody>
<tr><td>Provider / model</td><td>OpenRouter / <code>openai/gpt-5.4-mini</code></td><td>清理英文 ASR 逐字稿。</td></tr>
<tr><td>temperature</td><td><code>0.1</code></td><td>降低清理結果的隨機差異。</td></tr>
<tr><td>每段最大字元</td><td><code>20,000</code></td><td>長逐字稿會先依段落、句點或空白切成 chunks。</td></tr>
<tr><td>max_tokens</td><td><code>24,000</code></td><td>保留足夠輸出長度，避免長文本被截斷。</td></tr>
<tr><td>timeout / retries / workers</td><td><code>600 秒 / 2 次 / 4</code></td><td>逾時重試，並以有限平行數處理多筆逐字稿。</td></tr>
</tbody></table></div>

<details>
<summary>LLM-clean 使用的 prompt</summary>

```text
SYSTEM
You clean Whisper ASR transcripts for research topic modeling.
Return only the cleaned transcript. Do not summarize, translate, classify, or add commentary.
Preserve the original meaning and order.
Repair missing or awkward punctuation so sentence boundaries are readable.
Remove repeated sentences, repeated fragments, and meaningless filler loops caused by ASR hallucinations.
Remove obvious transcription artifacts such as repeated "uh", "um", "[Music]", and duplicated captions when they add no meaning.
Preserve valid English even if grammar is imperfect, fragmented, or colloquial.
Preserve vehicle brand and model names in this LLM step; a deterministic dictionary pass will delete or neutralize them after the LLM cleaning.

USER
Clean this transcript chunk and return only the cleaned transcript:

{transcript_chunk}
```
</details>

### 2. BERTopic：LLM 主題命名與穩定性檢驗

LLM 僅更新 topic representation（讓主題名稱更可讀），不參與 embedding、UMAP 或 HDBSCAN 分群；因此不會改變群集指派或 noise ratio。網站中 M02、M03、T01、T02、T03 等結果頁會依實際執行狀態標示「已執行」、「未執行」或「未設定」。

<div class="table-scroll"><table class="m01-strategy-table"><thead><tr><th>版本／用途</th><th>模型與輸入</th><th>驗證設定</th></tr></thead><tbody>
<tr><td>早期 A06–A08 主題標籤試驗</td><td>OpenRouter / <code>openai/gpt-4o-mini</code>；BERTopic 的文件與關鍵詞。</td><td>單次生成短主題標籤，最多 5 個英文詞；若未提供 API key 則改保留本地表徵結果。</td></tr>
<tr><td>M02 正式命名與後續 M03、T01–T03 驗證</td><td>OpenRouter / <code>openai/gpt-5.5</code>；每個主題輸入 Default c-TF-IDF 前 10 個關鍵詞與前 6 個代表句。</td><td><code>temperature=0.0</code>、<code>max_tokens=64</code>；每個代表句最多取前 420 字元。M02 分別做 30 次與 50 次命名；後續驗證多採 50 次，實際是否成功以個別結果頁為準。</td></tr>
</tbody></table></div>

<details>
<summary>BERTopic LLM50 使用的 prompt</summary>

```text
SYSTEM
You label BERTopic topics for an electric vehicle research corpus.
Return one concise English topic label, 2 to 6 words.
Prefer EV meaning when present. Do not explain.

USER
Topic ID: {topic_id}
Keywords: {top_10_c_tf_idf_keywords}
Representative snippets:
- {representative_document_1}
- ... up to 6 documents

Topic label:
```
</details>

LLM50 的穩定性規則為：同一主題多次命名後，若眾數名稱比例 <code>mode_ratio >= 0.70</code>，或各名稱與眾數之平均 token Jaccard similarity <code>>= 0.65</code>，即標示為穩定。這是名稱一致性檢查，不是 BERTopic 分群品質分數。

### 3. 歷史與原型中的 LLM 使用

| 位置 | LLM 用途 | 是否屬於目前正式流程 |
| --- | --- | --- |
| <code>#運行BERTopic整理/#5.1 試跑停用詞</code>、A06–A08 結果 | OpenRouter 主題標籤與停用詞設計前的試跑。 | 歷史探索；保留作為方法演變紀錄。 |
| <code>#B1-4/.../#BC-test</code> | 多個 BERTopic 與 OpenRouter 主題命名原型，主要使用 <code>openai/gpt-4o-mini</code>。 | 否；測試腳本。 |
| <code>v0.0.1_HF-PUSH_【推上HF】/app.py</code> | 提供將 LLM-normalized transcript 推送到 Hugging Face 的批次範本，也含 BERTopic 命名範本。 | 否；部署／匯入工具範本。 |
| <code>Result/06.03_A01</code> 與 <code>Result/06.03_A02</code> | 早期與正式的 LLM 前處理執行紀錄。 | A02 是目前資料清理脈絡的正式來源；A01 為早期版本。 |

<aside class="table-note"><strong>安全提醒：</strong>檢查歷史程式時發現部分舊腳本曾把 OpenRouter key 寫入原始碼。請立即在 OpenRouter 後台撤銷並重新產生該 key，之後僅透過環境變數或密鑰管理工具提供，不要再次提交到 Git。</aside>
