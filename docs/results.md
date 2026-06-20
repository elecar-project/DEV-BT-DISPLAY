---
title: 結果
description: 以實驗路徑瀏覽 DEV-BT 的 BERTopic 結果與驗證分支。
---

# 結果

本頁依實驗的資料血緣與處理順序呈現。可點擊的綠色節點已有完整結果與設定摘要；灰色節點保留在地圖中，待後續整理後開放。

<div class="experiment-map-scroll" aria-label="DEV-BT 完整實驗地圖">
  <object class="experiment-map-full" type="image/svg+xml" data="{{ '/assets/img/experiment-map-full.svg?v=20260620-full-map' | relative_url }}">
    <img src="{{ '/assets/img/experiment-map-full.svg?v=20260620-full-map' | relative_url }}" alt="DEV-BT 完整實驗運行架構圖">
  </object>
</div>

## 如何閱讀

`A03-A05` 是資料版本、UMAP 與停用詞處理的探索階段；`M01-M03` 是選定設定後的主要模型運行；`T01-T04` 則用不同資料處理、年份切分與資料篩選條件檢驗結果是否穩定。

## 已整理結果

| 終點 | 實驗意義 | 目前狀態 |
| --- | --- | --- |
| 8New-LLM30 | 最佳參數模型，LLM 命名 30 次驗證 | 可檢視 |
| 8New-LLM50 | 同一路徑以 50 次命名驗證，資料夾名稱歷史上誤標為 tp-30 | 可檢視 |
| 2020 前 | 年份切分後的 2008-2019 主題模型 | 可檢視 |
| 其他 T01-T04 節點 | 驗證與敏感度分析 | 待整理 |
