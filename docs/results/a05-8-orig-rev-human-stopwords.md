---
title: A05-8.4 human 停用詞設計
description: A05-8｜orig REV 詞表收斂 的 A05-8.4 human 停用詞設計紀錄。
experiment_id: a05-8-orig-rev-human-stopwords
---

# A05-8.4 human｜停用詞設計

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
## 本版目的

人工收斂為較易維護的 12 類建議版。

<p class="section-intro">本版本依 BERTopic representation 的殘留詞調整客製停用詞。</p>

## 停用詞分類與理由

<h3>統整表格</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>逐字稿寒暄與影片流程詞</td><td>這些詞來自主持人開場、結尾、問候或訪談流程，與電動車主題無直接關聯，且已形成獨立 topic。</td><td>thank, thanks, welcome, bye, joining, today, doing, hope, good, great, gentlemen, questions</td></tr><tr><td>口語填充與對話慣用詞</td><td>don know、yeah、okay 等詞反映口語互動，不代表 EV 技術或產品語意，會稀釋 topic words。</td><td>okay, yeah, don, know, don know, know don, said, let, going, want, right, really, just, like, kind, sort, ve</td></tr><tr><td>人名、來源與辨識雜訊</td><td>topic words 中出現主持人/受訪者姓名、來源名稱或疑似轉寫/品牌殘留，對 EV 主題分類沒有穩定解釋力。</td><td>robin, chris, candy, k23</td></tr><tr><td>保固/數字片段雜訊</td><td>000、whichever comes 等通常來自保固條款句型，容易形成售後條款或數字噪音 topic；若研究不分析保固，建議停用。</td><td>000, 000 mile, 000 miles, whichever, whichever comes</td></tr><tr><td>輪圈/等級/尺寸詞</td><td>多出現在配備與車型等級介紹，與 EV 核心主題關聯弱。</td><td>wheels, wheel, alloy, alloy wheels, inch, grades, xse, xle, se</td></tr><tr><td>影片流程、寒暄與口語殘留</td><td>A06-8-REV 的 most_topics topic 0 顯示 subscribe/channel/video/guys 等影片流程詞仍形成 topic；其他泛用口語詞則集中在大 topic 或 MMR representation。</td><td>subscribe, channel, video, watching, guys, oh, ll, come, coming, invite, live, clips, pleasure, awesome, ready, glad, amazing, love, shoot, yes, wait, test, actually</td></tr><tr><td>英文功能詞與 MMR 漏網詞</td><td>MMR representation 中仍出現 and/to/we/on/your 等功能詞；雖然 sklearn stopwords 已作用於 vectorizer，但為了 representation 後處理也能濾除，補進客製清單。</td><td>and, to, we, us, me, our, your, on, an, as, at, are, be, can, do, re, here, there, all, one, more, very, which, will</td></tr><tr><td>泛用敘事與團隊流程詞</td><td>這些詞在 best_balance 的大型 topic 中高頻出現，但多反映敘事流程、團隊協作或年份/標配資訊，不是 EV 技術錨點。</td><td>think, people, team, work, focus, lot, say, time, way, year, company, built</td></tr><tr><td>外觀、車身與設計展示詞</td><td>A05-8 已建議停用 design/light/line 等詞；A06-8-REV 又看到 grill/front/headlamp/taillights 等同類詞。</td><td>grill, front, body, lower, effect, frame, sporty, vertical, running, nose, side, exterior, sleek, wider, headlamp, headlamps, headlight, horizontal, lamps, width, iconic</td></tr><tr><td>口語與泛用敘事殘留</td><td>A06-8.1 仍出現 right、going、want、make、years、important 等詞，會讓大型 topic 變成逐字稿互動或泛敘事，而不是 EV 子題。</td><td>right, going, want, make, years, important, comes, day, question, watch, videos, photos, hi, stage</td></tr><tr><td>其他非 EV 車評與展示殘留</td><td>車評細節或場景詞仍反覆出現，但與 EV 技術、能源、充電、電池、電驅關係弱。</td><td>pins, underneath, wheelbase, problems, pressure, launch, launched, shanghai, thomas, tom, italy, prix, turin, group, munich, europe, japanese, scandinavian, lincoln, andy</td></tr><tr><td>影片流程與口語殘留</td><td>A06-8.2 仍可見 ll、jump、soon、meet、photographers、morning、hear 等逐字稿或影片流程詞。</td><td>ll, jump, soon, meet, photographers, hear, hey, morning, join, york, detroit</td></tr></tbody></table></div>

## 使用原則

<div class="table-note" role="note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</div>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a05-8-orig-rev-human-stopwords/A05-8.4(human)_stopword.md' | relative_url }}">A05-8.4(human)_stopword.md</a></td><td>原始停用詞建議與完整 CountVectorizer 清單</td></tr><tr><td><a href="{{ '/assets/results/a05-8-orig-rev-human-stopwords/A05-8.4(human)_stopword.docx' | relative_url }}">A05-8.4(human)_stopword.docx</a></td><td>人工審閱用 Word 版本</td></tr></tbody></table>
</section>
</div>
