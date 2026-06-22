---
title: 結果
description: DEV-BT 實驗資料血緣、處理順序與已整理結果。
---

# 結果

本頁依實驗的資料血緣與處理順序呈現。可點擊的節點已有完整結果與設定摘要；其他節點保留在地圖中，待後續整理後開放。

<div class="experiment-map-scroll" aria-label="DEV-BT 完整實驗地圖">
  <object class="experiment-map-full" type="image/svg+xml" data="{{ '/assets/img/experiment-map-full.svg?v=registry-v1' | relative_url }}" aria-label="DEV-BT 完整實驗運行架構圖">
    <img src="{{ '/assets/img/experiment-map-full.svg?v=registry-v1' | relative_url }}" alt="DEV-BT 完整實驗運行架構圖">
  </object>
</div>

## 如何閱讀

A03-A05 是資料版本、UMAP 與停用詞處理的探索階段；M01-M03 是選定設定後的主要模型運行；T01-T04 則用不同資料處理、年份切分與資料篩選條件檢驗結果是否穩定。

{% assign registry = site.data.experiments %}

## 已整理結果

| 終點 | 實驗意義 | 目前狀態 |
| --- | --- | --- |
{% for item in registry.experiments %}{% if item.featured %}
| [{{ item.title }}]({{ item.page | relative_url }}) | {{ item.description }} | {{ item.status }} |
{% endif %}{% endfor %}
{% for item in registry.pending %}
| {{ item.label }} | {{ item.description }} | {{ item.status }} |
{% endfor %}

{% for group in registry.groups %}
## {{ group.title }}

{{ group.description }}

| 節點 | 實驗意義 | 目前狀態 |
| --- | --- | --- |
{% for item in registry.experiments %}{% if item.group == group.id %}
| [{{ item.title }}]({{ item.page | relative_url }}) | {{ item.description }} | {{ item.status }} |
{% endif %}{% endfor %}
{% endfor %}
