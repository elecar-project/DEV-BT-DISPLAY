---
title: A05-8.1 停用詞設計
description: A05-8｜repl 詞表迭代 的 A05-8.1 停用詞設計紀錄。
---

# A05-8.1｜停用詞設計

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 版本設定

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>版本線</td><td>A05-8｜repl 詞表迭代</td></tr>
<tr><td>資料版本</td><td>repl + tok + 段落 12-80</td></tr>
<tr><td>版本定位</td><td>第一次增補</td></tr>
<tr><td>分類筆數</td><td>8 類</td></tr>
</tbody></table>

### 核心原則

<p>保留 EV 語意錨點：<code>electric、EV、charging、battery、range、motor、torque、hybrid、plug</code>。</p>

### 導覽

<p><a href="{{ '/results/a05-stopwords-overview.html' | relative_url }}">回到 A05 停用詞總覽</a></p>
</aside>

<section markdown="1">
## 本版目的

補入車機、影音、連線與產品展示殘留。

<p class="section-intro">本檔是 A05-8_stopword.md 的增補檔，不重複列出 A05-8 已收錄的停用詞。後續若要重跑 BERTopic，建議把 A05-8 與 A05-8.1 的單字清單合併使用。</p>

## 停用詞分類與理由

<h3>新增建議停用詞</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>口語泛詞與時間詞</td><td>time、think、year 等在多組 A06-8 representation 中反覆出現，但主要是逐字稿語氣、泛用敘述或年份資訊，對 EV 子主題區分力低。</td><td>time, think, year, years, ll, way, use, people, best, lot, say, make, got, different, better, thing, makes, important, easy, course, experience, offer, joy, progress, fun, addition</td></tr><tr><td>影片、會議與頻道寒暄詞</td><td>這些詞多來自主持、訪談、會議、頻道互動或發表會開場，容易形成「影片流程/會議寒暄」topic。</td><td>day, hi, yes, ladies, pleasure, channel, talking, meet, conference, appreciate, everybody, hello, glad, morning, share, introduce, excited, exciting, reveal, event</td></tr><tr><td>車機、影音與連線詞</td><td>A06-8 仍有 topic 被音響、手機、地圖、連線、遠端服務與螢幕操作吸走；若研究不分析 connected car，建議移除。</td><td>sound, music, maps, app, apps, devices, iphone, connect, compatible, services, service, connectivity, lock, unlock, remotely, fob, wi, hyperscreen, cockpit, screens, assistant, touch, speaker, usb, messages, alexa, jbl</td></tr><tr><td>外觀、燈具與造型詞</td><td>這些詞會讓 topic 偏向外觀、燈具、車身比例與設計風格，而不是 EV 技術或能源議題。</td><td>front, air, exterior, headlamps, body, dynamic, lighting, grill, roof, proportions, face, sleek, strong, modern, distinctive, spoiler, taillights, headlight, matrix, graphic, horizontal, pixels</td></tr><tr><td>內裝、空間與操作展示詞</td><td>這些詞多來自座艙、舒適性、行李廂、按鍵與操作示範，會形成一般車評內裝 topic。</td><td>trunk, buttons, comfortable, climate, heated, passengers, passenger, materials, trim, second, fold, storage, panel, spacious, compartment, soft, pressure, blow, hot, hands, handle, kit, removed</td></tr><tr><td>ICE、賽道與車型級距詞</td><td>A06-8 仍出現燃油引擎、賽道、性能車、sedan/sport 等語境，會把 topic 導向非 EV 或一般車型定位。</td><td>v6, turbocharged, sedans, sport, sports, racing, racetrack, race, track, motorsport, gt, gt3, amg, quattro, trd, edition, virtual, concept, compact, unique, perfect, touring, lifestyle, midsized</td></tr><tr><td>商務、市場、活動與售後詞</td><td>這些詞多來自企業發表、售價、保固、救援、活動地點或年份，不是穩定 EV 主題語意。</td><td>standard, models, president, vice, team, affordable, cost, warranty, maintenance, roadside, assistance, toyotacare, detroit, season, los, angeles, 12, 16, 17, 19, 2017, 2025, 999, york, munich, nevada</td></tr><tr><td>材料、尺寸與 NVH 詞</td><td>carbon fiber、wheelbase、noise、wind tunnel 等會形成材料、尺寸、隔音或舒適性 topic；若研究聚焦 EV 技術與能源，建議停用。</td><td>fiber, weight, wheelbase, structure, meters, aluminum, inches, noise, quiet, hear, wind, whisper, silence, ear, actually, tunnel, exhaust</td></tr></tbody></table></div>

## 使用原則

<aside class="table-note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</aside>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a05-8-repl-1-stopwords/A05-8.1_stopword.md' | relative_url }}">A05-8.1_stopword.md</a></td><td>原始停用詞建議與完整 CountVectorizer 清單</td></tr></tbody></table>
</section>
</div>
