---
title: 資料集
description: 資料版本、篩選規則與存取位置。
---

# 資料集

本頁追蹤 DEV-BT 研究流程中已出現的主要資料集版本、篩選規則與存放位置。

## 資料集清單

| 資料集 | 說明 | 位置 | 狀態 |
| --- | --- | --- | --- |
| 原始逐字稿 | 454 個 `.txt`，作為後續清理與篩選的起點 | `#TXT_DATA/2. 文字稿－txt/` | 已盤點 |
| 主要清理後逐字稿 | 434 個 `.txt`，目前多數 BERTopic 實驗的主資料來源 | `#TXT_DATA/05.24_txt-test_deleted(434)/` | 已盤點 |
| Hugging Face Dataset 版本 | 434 筆，欄位為 `title`、`transcript`，以 Arrow 格式保存 | `#TXT_DATA/05.24_txt-test_deleted(434)_dataset/` | 已盤點 |
| 600-2159 秒篩選資料 | 103 個 `.txt`，依影片長度區間篩選 | `#TXT_DATA/06.03_600-2159sec(103)/` | 已盤點 |
| 廠商去頭尾資料 | 237 個 `.txt`，每個廠商去除頭尾各 5 筆後保留 | `#TXT_DATA/06.03_廠商去頭尾各5家(237)/` | 已盤點 |
| 車廠/車款詞表 | 用於品牌與型號移除或替換的詞表 | `#TXT_DATA/man-model.md` | 已盤點 |
| EVcar URL SQLite | `ver.5.5`、`ver.5.6`、`ver.5.7` 等資料庫版本 | `#TXT_DATA/*.db` | 已盤點 |

## 資料集左右比對

<div class="dataset-compare">
  <div class="compare-controls">
    <div class="compare-field">
      <label for="dataset-left">左側資料集</label>
      <select id="dataset-left"></select>
    </div>
    <div class="compare-field">
      <label for="dataset-right">右側資料集</label>
      <select id="dataset-right"></select>
    </div>
    <div class="compare-field">
      <label for="dataset-status">狀態</label>
      <select id="dataset-status">
        <option value="all">全部</option>
        <option value="same">兩邊相同</option>
        <option value="different">兩邊都有但不同</option>
        <option value="missing">單側缺少</option>
      </select>
    </div>
    <div class="compare-field">
      <label for="dataset-search">搜尋檔名</label>
      <input id="dataset-search" type="search" placeholder="輸入檔名或關鍵字">
    </div>
    <div class="compare-field">
      <label for="dataset-preview">預覽模式</label>
      <select id="dataset-preview">
        <option value="full">顯示完整左右比對</option>
        <option value="diff">只顯示差異與前後文</option>
      </select>
    </div>
    <div class="compare-field checkbox-field">
      <label>
        <input id="dataset-ignore-case" type="checkbox" checked>
        忽略大小寫
      </label>
    </div>
    <div class="compare-field checkbox-field">
      <label>
        <input id="dataset-ignore-punctuation" type="checkbox" checked>
        忽略標點符號
      </label>
    </div>
  </div>

  <div id="dataset-summary" class="compare-summary"></div>

  <div class="file-list-header">
    <h3>檔案對照</h3>
    <span id="dataset-file-count"></span>
  </div>
  <div id="dataset-file-list" class="file-list"></div>

  <div id="dataset-compare-output" class="compare-output">
    <p class="loading-text">載入資料集 manifest 中...</p>
  </div>
</div>

<script src="{{ '/assets/js/dataset-compare.js' | relative_url }}"></script>
