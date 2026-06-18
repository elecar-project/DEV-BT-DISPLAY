---
title: 總覽
description: DEV-BT 專案的內部研究展示站。
---

<section class="hero">
  <div>
    <p class="eyebrow">內部研究展示站</p>
    <h1>DEV-BT 研究展示站</h1>
    <p>
      這裡整理 DEV-BT 專案從母倉庫累積而來的研究流程、資料集、
      工具、BERTopic 結果與解釋筆記，方便內部研究者快速回顧與協作。
    </p>
    <div class="badge-row">
      <span class="badge">研究流程</span>
      <span class="badge">資料集</span>
      <span class="badge">工具</span>
      <span class="badge">BERTopic 結果</span>
    </div>
  </div>
  <aside class="hero-panel" aria-label="專案狀態">
    <div class="metric">
      <strong>434</strong>
      <span>主要清理後逐字稿資料數</span>
    </div>
    <div class="metric">
      <strong>26,978</strong>
      <span>A06-A08 實驗的 BERTopic 輸入句數</span>
    </div>
    <div class="metric">
      <strong>5 組</strong>
      <span>已建立 topic_info CSV 的 BERTopic 結果</span>
    </div>
  </aside>
</section>

## 研究區塊

<div class="card-grid">
  <a class="link-card" href="method.html">
    <h3>方法</h3>
    <p>從逐字稿收集、清理到 BERTopic 實驗的完整流程。</p>
  </a>
  <a class="link-card" href="datasets.html">
    <h3>資料集</h3>
    <p>資料版本、篩選規則、欄位說明與存取位置。</p>
  </a>
  <a class="link-card" href="tools.html">
    <h3>工具</h3>
    <p>Python App、Windows 工具、exe Release 與原始碼連結。</p>
  </a>
  <a class="link-card" href="results.html">
    <h3>結果</h3>
    <p>整理後的主題模型輸出、比較結果與解釋筆記。</p>
  </a>
  <a class="link-card" href="appendix.html">
    <h3>附錄</h3>
    <p>實驗紀錄、歷史資料夾對照與搬遷紀錄。</p>
  </a>
  <a class="link-card" href="https://github.com/elecar-project/DEV-BT/releases">
    <h3>Release 檔案</h3>
    <p>母倉庫中已封裝的執行檔、工具與相關成果檔。</p>
  </a>
</div>

## 倉庫分工

| 倉庫 | 角色 | 主要對象 |
| --- | --- | --- |
| `DEV-BT` | 母倉庫與歷史工作區 | 維護者 |
| `DEV-BT-DISPLAY` | 整理後的內部研究展示站 | 內部研究者 |
| 未來公開／投稿用倉庫 | 簡化後的補充材料與讀者版內容 | 審查委員、編輯、讀者 |

## 目前狀態

這個展示倉庫已先放入一批來自母倉庫的真實研究索引，包括資料集版本、
工具流程、BERTopic 實驗結果與資料品質檢查。大型資料集、`.db`、`.csv`、
`.arrow` 與完整報告目前不直接複製到本站，而是保留在母倉庫或 Release，
本站負責建立可讀的導覽層。

<div class="callout">
  這個網站定位為內部研究版。之後若要建立公開或投稿用版本，可以再從這裡
  篩選出較精簡、較適合審查委員與一般讀者閱讀的內容。
</div>

## 快速索引

| 類型 | 目前整理到的內容 | 主要來源 |
| --- | --- | --- |
| 原始與清理後逐字稿 | 454 筆原始逐字稿、434 筆主要清理後逐字稿 | `#TXT_DATA/` |
| 篩選資料集 | 600-2159 秒區間 103 筆、廠商去頭尾各 5 家 237 筆 | `#TXT_DATA/`、`Result/DB_Filter/` |
| 前處理結果 | OpenRouter/LLM 清理 434 筆，成功 434 筆 | `Result/06.03_A02/` |
| BERTopic 結果 | A06、A07、A08 topic_info 與試跑報告 | `Result/` |
| 時間切分比對 | 434 筆與資料庫 upload year 對齊的 match report | `Result/06.13_A02/` |
| 工具與 App | Pre-process、BERTopic、A/B/C 系列工具 | 母倉庫各工具資料夾與 Release |

## 主要外部連結

- 母倉庫：<https://github.com/elecar-project/DEV-BT>
- 母倉庫 Release：<https://github.com/elecar-project/DEV-BT/releases>
