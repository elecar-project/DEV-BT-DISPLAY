---
title: 資料集
description: 資料版本、篩選規則與存取位置。
---

# 資料集

本頁追蹤 DEV-BT 研究流程中已出現的主要資料集版本、篩選規則與存放位置。

## 資料集清單

| 資料集 | 說明 | 位置 | 狀態 |
| --- | --- | --- | --- |
| 初始 txt | 454 個原始逐字稿 `.txt` | `#TXT_DATA/2. 文字稿－txt/` | 已載入比對器 |
| 刪除 20 份無人聲 dataset | 434 個 `.txt`，刪除無人聲或不適用文本後的版本 | `#TXT_DATA/05.24_txt-test_deleted(434)/` | 已載入比對器 |
| LLM 清理 del | 434 筆 Hugging Face Dataset；刪除廠商與款式名稱 | `Result/06.03_A02/R06.03_A02-pre_LLM(del)_dataset` | 已載入比對器 |
| LLM 清理 repl | 434 筆 Hugging Face Dataset；廠商與款式名稱替換為 `Brand`、`Model` | `Result/06.03_A02/R06.03_A02-pre_LLM(repl)_dataset` | 已載入比對器 |
| 年份切分 08-19 | 240 筆；以 2020 作為切分點的前段資料 | `Result/06.13_[A]/06.13_[A]-01-pre_LLM(orig)_08-19(240)_dataset` | 已載入比對器 |
| 年份切分 20-25 | 194 筆；以 2020 作為切分點的後段資料 | `Result/06.13_[A]/06.13_[A]-01-pre_LLM(orig)_20-25(194)_dataset` | 已載入比對器 |
| 驗證集1 08-17 | 177 筆；以 2018 作為切分點的前段資料 | `Result/06.13_[A]/06.13_[A]-02-pre_LLM(orig)_08-17(177)_dataset` | 已載入比對器 |
| 驗證集1 18-25 | 257 筆；以 2018 作為切分點的後段資料 | `Result/06.13_[A]/06.13_[A]-02-pre_LLM(orig)_18-25(257)_dataset` | 已載入比對器 |
| 驗證集1 08-18 | 221 筆；以 2019 作為切分點的前段資料 | `Result/06.13_[A]/06.13_[A]-03-pre_LLM(orig)_08-18(221)_dataset` | 已載入比對器 |
| 驗證集1 19-25 | 213 筆；以 2019 作為切分點的後段資料 | `Result/06.13_[A]/06.13_[A]-03-pre_LLM(orig)_19-25(213)_dataset` | 已載入比對器 |
| 驗證集1 08-20 | 288 筆；以 2021 作為切分點的前段資料 | `Result/06.13_[A]/06.13_[A]-04-pre_LLM(orig)_08-20(288)_dataset` | 已載入比對器 |
| 驗證集1 21-25 | 146 筆；以 2021 作為切分點的後段資料 | `Result/06.13_[A]/06.13_[A]-04-pre_LLM(orig)_21-25(146)_dataset` | 已載入比對器 |
| 驗證集2 1-35 分鐘 | 103 個 `.txt`，只使用 1-35 分鐘影片 | `#TXT_DATA/06.03_600-2159sec(103)/` | 已載入比對器 |
| 驗證集3 刪除頭尾各五家廠商 | 237 個 `.txt`，刪除頭尾各五家廠商後的資料 | `#TXT_DATA/06.03_廠商去頭尾各5家(237)/` | 已載入比對器 |

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

<script src="{{ '/assets/js/dataset-compare.js?v=20260618-full-datasets' | relative_url }}"></script>
