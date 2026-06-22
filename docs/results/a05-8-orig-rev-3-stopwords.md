---
title: A05-8.3 REV 停用詞設計
description: A05-8｜orig REV 詞表收斂 的 A05-8.3 REV 停用詞設計紀錄。
experiment_id: a05-8-orig-rev-3-stopwords
---

# A05-8.3 REV｜停用詞設計

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
## 本版目的

僅依 default topic words 補入低解釋力殘留。

<p class="section-intro">判斷原則：這一輪只依據 default BERTopic c-TF-IDF topic words 補停用詞；不參考 LLM、KeyBERT、POS、MMR。新增詞主要是 A06-8.2 後仍殘留的影片流程詞、品牌/車款與年份代碼、一般車評/設計/生產敘事、車機介面、非 EV 性能展示與市場行政詞。仍保留 EV 核心語意錨點，例如 electric、ev、battery、charging、range、motor、torque、hybrid、plug。</p>

## 停用詞分類與理由

<h3>A05-8.3-REV 新增停用詞</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>影片流程與口語殘留</td><td>A06-8.2 仍可見 ll、jump、soon、meet、photographers、morning、hear 等逐字稿或影片流程詞。</td><td>ll, jump, soon, meet, photographers, hear, hey, morning, join, york, detroit</td></tr><tr><td>品牌、車款、年份與代碼</td><td>A06-8.2 仍出現 Honda、Cadillac、Buick、Renault、K27、Kix、Q50/Q60 類型殘留；這些會讓 topic 偏向車款來源而非 EV 子題。</td><td>honda, cadillac, buick, renault, k27, kix, q50, q60, m35h, 2014, 2015, 2016, 2017, 911, 918, 999</td></tr><tr><td>車機、介面與影音</td><td>multimedia、instrument、interface、usb、ports、controller 等仍形成介面或影音操作詞。</td><td>multimedia, instrument, interface, usb, ports, controller, input, data, cloud, heads, eyes, 360</td></tr><tr><td>一般設計、生產與品牌敘事</td><td>設計、生產、人物、公司活動與市場敘事詞仍殘留，但不直接代表 EV 技術。</td><td>production, plant, development, process, business, testing, designer, designs, sketching, craftsmanship, studio, director, president, officer, division, ceo, vice</td></tr><tr><td>非 EV 車評/展示細節</td><td>外觀、跑車、賽道、車評性能與場景詞仍分散出現，建議停用以聚焦 EV 技術與能源主題。</td><td>racing, season, formula, champion, spider, laferrari, frankfurt, zuffenhausen, cabriolet, beauty, tire, lateral, stiff, agility</td></tr><tr><td>雜訊與低解釋力詞</td><td>number、broken、favorite、interesting、fun、noise 等對 topic 命名幫助低，容易形成片段化 topic words。</td><td>number, broken, favorite, interesting, fun, noise, quiet, silence, silent, gut, cancer</td></tr></tbody></table></div>

## 使用原則

<aside class="table-note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</aside>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a05-8-orig-rev-3-stopwords/A05-8.3-REV_stopword.md' | relative_url }}">A05-8.3-REV_stopword.md</a></td><td>原始停用詞建議與完整 CountVectorizer 清單</td></tr></tbody></table>
</section>
</div>
