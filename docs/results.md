---
title: 結果
description: 以實驗路徑瀏覽 DEV-BT 的 BERTopic 結果與驗證分支。
---

# 結果

本頁依實驗的資料血緣與處理順序呈現。可點擊的綠色節點已有完整結果與設定摘要；灰色節點保留在地圖中，待後續整理後開放。

<div class="experiment-map-scroll" aria-label="DEV-BT 實驗地圖">
  <div class="experiment-map">
    <section class="map-stage map-stage-source">
      <h2>A03｜min_cluster_size</h2>
      <div class="map-node source">1｜del</div>
      <div class="map-node source">2｜del + tok</div>
      <div class="map-node source linked">3｜del + tok<br>para 12-80</div>
      <div class="map-node source">4｜repl</div>
      <div class="map-node source">5｜repl + tok</div>
      <div class="map-node source linked">6｜repl + tok<br>para 12-80</div>
      <div class="map-node source">5.1｜repl-y + tok</div>
      <div class="map-node source">6.1｜repl-y + tok<br>para 12-80</div>
      <div class="map-node source">7｜orig + tok</div>
      <div class="map-node source selected">8｜orig + tok<br>para 12-80</div>
    </section>

    <div class="map-arrow-column">
      <span>資料版本比較</span>
      <i></i><i></i><i></i><i></i>
    </div>

    <section class="map-stage map-stage-process">
      <h2>A04｜UMAP</h2>
      <div class="map-node process">2</div>
      <div class="map-node process">3</div>
      <div class="map-node process">5</div>
      <div class="map-node process">6</div>
      <div class="map-node process">7</div>
      <div class="map-node process selected">8</div>
      <h2 class="second-heading">A05｜停用詞</h2>
      <div class="map-node process selected">8</div>
    </section>

    <div class="map-arrow-column map-arrow-wide"><span>候選模型</span><i></i><i></i><i></i></div>

    <section class="map-stage map-stage-main">
      <h2>M01｜主程式<br>全參數</h2>
      <div class="map-node main">8</div>
      <h2 class="second-heading">M02｜主程式<br>單一參數</h2>
      <a class="map-node result" href="{{ '/results/m02-llm30.html' | relative_url }}">8New-LLM30<br><small>命名 30 次</small></a>
      <a class="map-node result" href="{{ '/results/m02-llm50.html' | relative_url }}">8New-LLM50<br><small>命名 50 次</small></a>
      <h2 class="second-heading">M03｜主程式<br>年份切分</h2>
      <a class="map-node result" href="{{ '/results/m03-2020-before.html' | relative_url }}">2020 前<br><small>08-19</small></a>
      <div class="map-node pending">2020 後<br><small>20-25</small></div>
    </section>

    <div class="map-arrow-column map-arrow-wide"><span>驗證分支</span><i></i><i></i><i></i></div>

    <section class="map-stage map-stage-validation">
      <h2>T01｜廠商／款式處理</h2>
      <div class="map-node pending">3｜del 比較</div>
      <div class="map-node pending">6｜repl 比較</div>
      <h2 class="second-heading">T02｜年份切分</h2>
      <div class="map-node pending">2018／2019／2021<br>前後比較</div>
      <h2 class="second-heading">T03｜資料篩選驗證</h2>
      <div class="map-node pending">影長 1-35 分鐘</div>
      <div class="map-node pending">去頭尾各 5 廠</div>
      <h2 class="second-heading">T04｜repl 停用詞</h2>
      <div class="map-node pending">5.1 / 6.1<br>Brand、Model 停用詞</div>
    </section>
  </div>
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
