---
title: A05-8.2 停用詞設計
description: A05-8｜repl 詞表迭代 的 A05-8.2 停用詞設計紀錄。
---

# A05-8.2｜停用詞設計

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 版本設定

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>版本線</td><td>A05-8｜repl 詞表迭代</td></tr>
<tr><td>資料版本</td><td>repl + tok + 段落 12-80</td></tr>
<tr><td>版本定位</td><td>第二次增補</td></tr>
<tr><td>分類筆數</td><td>9 類</td></tr>
</tbody></table>

### 核心原則

<p>保留 EV 語意錨點：<code>electric、EV、charging、battery、range、motor、torque、hybrid、plug</code>。</p>

### 導覽

<p><a href="{{ '/results/a05-stopwords-overview.html' | relative_url }}">回到 A05 停用詞總覽</a></p>
</aside>

<section markdown="1">
## 本版目的

補入功能詞、車款 trim 與市場展示殘留。

<p class="section-intro">本檔是 A05-8 與 A05-8.1 之後的第二次增補檔，不重複列出前兩版已經收錄的停用詞。後續若要重跑 BERTopic，建議合併 A05-8_stopword.md、A05-8.1_stopword.md 與本檔的單字清單。</p>

## 停用詞分類與理由

<h3>新增建議停用詞</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>英文功能詞與代名詞</td><td>MMR/POS 仍會把 we、our、will 等一般英文功能詞帶回 topic words；這些詞無主題辨識力，且會污染 representation。</td><td>we, our, more, will, first, at, us, show, one, to, can, about, and, it, its, is, be, an, do, take, on, you, also</td></tr><tr><td>泛用敘述與低區分力詞</td><td>features、system、class、feel 等過於泛用，容易讓 topic label 變成一般車評語氣，而不是 EV 子主題。</td><td>feature, features, system, class, feel, general, company, business, industry, production, sold, selling, generation, automotive, show, shows, chief, mr, pilot, scheduled, work, long, question, ready, come, tell, love</td></tr><tr><td>影片、頻道與口語互動詞</td><td>A06-8.1 後仍有影片開場、訂閱、互動語氣與口語片段，會形成非內容主題。</td><td>hey, guys, video, episode, live, watching, soon, subscribe, oh, forget, join, closer</td></tr><tr><td>車機、連線與操作詞</td><td>這些詞多來自車機功能、手機連線、操作示範或 UI 輔助，不是 EV 技術本體。</td><td>infotainment, multimedia, premium, including, start, access, center, compatibility, mobile, device, speakers, connects, qi, card, route, view, mode, modes, gear, manual, turning, pull, push, degrees</td></tr><tr><td>外觀、內裝與配備細節</td><td>這些詞會把 topic 帶到外觀線條、內裝縫線、車身細節、尺寸或輪圈，不是 EV 核心語意。</td><td>cabin, stitching, legroom, split, fit, lower, lamps, running, high, end, kidney, bumper, character, chrome, sporty, side, color, colors, material, elements, top, grade, limited, tires, rims, size, radius, handling, felt, look, looks</td></tr><tr><td>設計、素材與製程詞</td><td>這些詞來自設計靈感、草圖、材料、製程或外觀修辭，會讓 topic 偏向設計敘事。</td><td>designer, inspiration, started, sketching, process, details, futuristic, innovations, innovative, carbon, fibre, steel, construction, ultra</td></tr><tr><td>活動、年份、地名與商務詞</td><td>這些詞多是發表活動、年份、地點、購買/庫存與市場資訊，容易形成活動或商務 topic。</td><td>price, buy, pre, inventory, international, europe, northpoint, la, 2015, 18, 20, stage, photo, photographers, photos</td></tr><tr><td>車款、trim 與級距殘留</td><td>這些詞多是特定車款、trim、車型級距或品牌技術命名；若目標是跨車款 EV 主題，建議移除。</td><td>xrt, gt4, gtr, sl, 4matic, tnga, le, nightshade, cabriolet, series, crossover, ev9, gtr, crest, mountains, test</td></tr><tr><td>NVH、保固與售後詞</td><td>這些詞會形成隔音、聲學、保固或售後條款 topic；若研究聚焦 EV 技術與能源，建議停用。</td><td>acoustic, quietest, quietness, silent, unlimited, mileage</td></tr></tbody></table></div>

## 使用原則

<aside class="table-note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</aside>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a05-8-repl-2-stopwords/A05-8.2_stopword.md' | relative_url }}">A05-8.2_stopword.md</a></td><td>原始停用詞建議與完整 CountVectorizer 清單</td></tr></tbody></table>
</section>
</div>
