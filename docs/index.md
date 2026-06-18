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
      <strong>內部版</strong>
      <span>給研究者整理、檢視與討論</span>
    </div>
    <div class="metric">
      <strong>靜態網站</strong>
      <span>使用 GitHub Pages 發布</span>
    </div>
    <div class="metric">
      <strong>連結式整理</strong>
      <span>大型檔案與 Release 保留在母倉庫</span>
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

這個展示倉庫目前先作為結構化索引使用。後續可以逐步從母倉庫搬移內容，
大型資料集與大量產出檔則保留在外部儲存、GitHub Release 或其他資料平台，
並在本站建立清楚的說明與連結。

<div class="callout">
  這個網站定位為內部研究版。之後若要建立公開或投稿用版本，可以再從這裡
  篩選出較精簡、較適合審查委員與一般讀者閱讀的內容。
</div>

## 主要外部連結

- 母倉庫：<https://github.com/elecar-project/DEV-BT>
- 母倉庫 Release：<https://github.com/elecar-project/DEV-BT/releases>
