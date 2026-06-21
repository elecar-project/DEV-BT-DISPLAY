---
title: A05-8.3 停用詞設計
description: A05-8｜repl 詞表迭代 的 A05-8.3 停用詞設計紀錄。
---

# A05-8.3｜停用詞設計

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 版本設定

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>版本線</td><td>A05-8｜repl 詞表迭代</td></tr>
<tr><td>資料版本</td><td>repl + tok + 段落 12-80</td></tr>
<tr><td>版本定位</td><td>第三次增補</td></tr>
<tr><td>分類筆數</td><td>9 類</td></tr>
</tbody></table>

### 核心原則

<p>保留 EV 語意錨點：<code>electric、EV、charging、battery、range、motor、torque、hybrid、plug</code>。</p>

### 導覽

<p><a href="{{ '/results/a05-stopwords-overview.html' | relative_url }}">回到 A05 停用詞總覽</a></p>
</aside>

<section markdown="1">
## 本版目的

處理代名詞、媒體語氣、UI 與一般車評語境。

<p class="section-intro">本檔是 A05-8、A05-8.1 與 A05-8.2 之後的第三次增補檔，不重複列出前版已收錄的停用詞。後續若要重跑 BERTopic，建議合併四份檔案的單字清單。</p>

## 停用詞分類與理由

<h3>新增建議停用詞</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>英文功能詞與代名詞</td><td>KeyBERT/MMR 仍會把英文停用詞帶回 representation；這些詞沒有主題辨識力，但會佔據短 topic words。</td><td>all, as, because, did, does, for, from, he, here, how, in, into, me, my, off, per, re, that, the, up, very, was, were, would, your</td></tr><tr><td>口語、情緒與泛用敘述詞</td><td>這些詞多來自車評口語、直播回覆或泛用評價，會形成非 EV 內容的描述型 topic。</td><td>able, amazing, anymore, answer, awesome, big, case, confident, coming, decided, eat, enjoy, extremely, fact, feels, feeling, go, having, hungry, life, little, looked, looking, mean, minutes, need, restaurant, same, scenario, simply, something, talk, things, thoughtfulness, wanted, warm, worst, yaw</td></tr><tr><td>影片、媒體與發表會詞</td><td>多屬影片操作、媒體活動、現場簡報或人物致詞，不是電動車技術或消費議題本身。</td><td>attention, behalf, broadcast, check, click, coverage, evening, executive, exhibit, final, guests, invite, launch, listen, media, moment, passion, passionate, photographs, presenters, presentation, robert, session, shoot, stream, tonight, visit</td></tr><tr><td>外觀、內裝與設計細節</td><td>這些詞會讓主題被車身外觀、內裝配備、材質或設計修辭吸走，與跨車款 EV 主題關聯較弱。</td><td>accents, adjustable, aggressive, appearance, blacked, bronze, capacity, clamshell, combinations, core, curtains, daytime, designs, diffuser, double, elegance, elegant, exclusive, exposed, fabric, flat, folded, forged, frame, glass, headlamp, headroom, iconic, lamp, lightweight, logo, low, matte, metal, middle, oled, outside, overhang, painted, panels, platinum, plenty, radiator, red, relaxed, seamlessly, silhouette, single, slim, spoke, surfaces, taillight, tow, upholstery, vertical, visuals, widescreen, wider</td></tr><tr><td>車機、UI 與操作詞</td><td>殘留詞多描述儀表、選單、語音、連線或操作介面，容易把 topic 推向車機展示而非 EV 議題。</td><td>augmented, bose, box, cluster, control, controls, data, destination, fi, hotspot, hmi, includes, instrument, interface, intuitive, iphones, keys, left, menu, menus, ports, settings, status, subscriptions, voice, watts</td></tr><tr><td>商務、市場與組織詞</td><td>這些詞多是銷售、訂單、企業職銜、工廠、品質或市場敘事，會形成商務/新聞 topic。</td><td>american, automobile, bank, chairman, ceo, change, consumer, competitive, cook, create, demand, electronic, factory, footprint, friendly, gives, growth, initiative, listed, marketing, million, north, officer, order, orders, ownership, pricing, produce, promotional, quality, starting, standards, successful, systems, tax, theme, value, variants, wrench</td></tr><tr><td>品牌、車款、人名與地名殘留</td><td>若研究目標是跨品牌的 EV 主題平衡，這些專名容易把主題吸到特定發表會、車款或人物。</td><td>berlin, bruce, burt, carman, cascada, chevy, conrad, folgore, gm, gt2, gtb, gts, jeff, neon, nick, nürburgring, peter, q3, rc, sf, spyder, st, stuttgart, texas</td></tr><tr><td>數字與年份殘留</td><td>這些孤立數字在 topic words 中多來自型號、年份、保固或比例片段，缺乏穩定主題意義。</td><td>10, 21, 24, 25, 40, 53, 56, 100, 150, 2050</td></tr><tr><td>其他非 EV 場景詞</td><td>這些詞來自遊艇、職銜或命名片段，與電動車核心主題無直接關聯。</td><td>sailing, yachts, senior, manager, name, drivers</td></tr></tbody></table></div>

## 使用原則

<aside class="table-note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</aside>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a05-8-repl-3-stopwords/A05-8.3_stopword.md' | relative_url }}">A05-8.3_stopword.md</a></td><td>原始停用詞建議與完整 CountVectorizer 清單</td></tr></tbody></table>
</section>
</div>
