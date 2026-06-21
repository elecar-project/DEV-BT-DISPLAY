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
      <strong>14 組</strong>
      <span>已載入左右比對的資料集版本</span>
    </div>
    <div class="metric">
      <strong>8 條</strong>
      <span>已整理的實驗與驗證路徑</span>
    </div>
  </aside>
</section>

## 快速索引

| 類型 | 目前整理到的內容 | 主要來源 |
| --- | --- | --- |
| 原始與清理後逐字稿 | 454 筆原始逐字稿、434 筆主要清理後逐字稿 | `#TXT_DATA/` |
| 篩選資料集 | 600-2159 秒區間 103 筆、廠商去頭尾各 5 家 237 筆 | `#TXT_DATA/`、`Result/DB_Filter/` |
| 前處理結果 | OpenRouter/LLM 清理 434 筆，成功 434 筆 | `Result/06.03_A02/` |
| BERTopic 結果 | A03-A05 探索、M01-M03 主程式、T01-T02 驗證結果與原始輸出 | `Result/`、`#運行BERTopic整理/` |
| 時間切分比對 | 434 筆與資料庫 upload year 對齊的 match report | `Result/06.13_A02/` |
| 工具與 App | Pre-process、BERTopic、A/B/C 系列工具 | 母倉庫各工具資料夾與 Release |
