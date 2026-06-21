---
title: A05-6 停用詞設計
description: A05-6｜初步停用詞迭代 的 A05-6 停用詞設計紀錄。
---

# A05-6｜停用詞設計

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 版本設定

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>版本線</td><td>A05-6｜初步停用詞迭代</td></tr>
<tr><td>資料版本</td><td>repl + tok + 段落 12-80</td></tr>
<tr><td>版本定位</td><td>基礎詞表</td></tr>
<tr><td>分類筆數</td><td>27 類</td></tr>
</tbody></table>

### 核心原則

<p>保留 EV 語意錨點：<code>electric、EV、charging、battery、range、motor、torque、hybrid、plug</code>。</p>

### 導覽

<p><a href="{{ '/results/a05-stopwords-overview.html' | relative_url }}">回到 A05 停用詞總覽</a></p>
</aside>

<section markdown="1">
## 本版目的

建立 EV 核心詞保留與一般雜訊移除原則。

<p class="section-intro">資料來源：Result/06.03_A04_min-test/A04-6(repl)_tok(para12-80)/</p>

## 停用詞分類與理由

<h3>建議停用詞表</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>資料匿名化替代詞</td><td>Brand、Model 是前處理替換後的佔位詞，會大量主導 topic words，但不能提供具體 EV 語意。</td><td>brand, model, brand model, brand brand, new brand, new model, model brand, brand new, model hybrid, model ev, model electric</td></tr><tr><td>過度泛化車輛詞</td><td>這些詞雖和汽車有關，但太泛用，會讓主題停留在「車」而不是 EV 技術、充電、電池或市場議題。建議先列為可選停用詞，若後續 topic 太碎可保留部分詞。</td><td>car, cars, vehicle, vehicles, auto, automotive</td></tr><tr><td>新品發表泛詞</td><td>常見於新車發表稿，不指向 EV 主題本身，容易把不同車型介紹混在一起。</td><td>new, all new, latest, generation, lineup, grade, grades, trim, trims, version, variants, package, packages, product, products</td></tr><tr><td>口語填充詞</td><td>來自逐字稿口語，對主題命名沒有貢獻，會產生 don/know/right/yeah/going 類型的無意義主題。</td><td>just, like, really, actually, basically, kind, kind of, sort, sort of, pretty, quite, little, lot, bit, maybe, probably, simply, certainly</td></tr><tr><td>對話與認知動詞</td><td>多出現在試駕、訪談或主持人講話中，與 EV 主題無關。</td><td>know, think, want, going, gonna, don, dont, don know, let, let me, see, look, looking, feel, feels, get, got, make, made, makes, come, comes, came</td></tr><tr><td>方向與操作泛詞</td><td>在車內功能示範中高頻出現，但多是操作步驟，不是 EV 研究核心。</td><td>right, left, front, back, inside, outside, open, close, press, push, pull, turn, release, button, buttons, cover, tab, place, use, using</td></tr><tr><td>發表會寒暄詞</td><td>形成 thank/good/bye/welcome 等獨立主題，與車輛技術或 EV 市場無關。</td><td>thank, thanks, thank you, good, morning, afternoon, evening, bye, goodbye, welcome, joining, join, joined, doing, hope, great, today, tonight</td></tr><tr><td>舞台與媒體流程詞</td><td>來自車展、發表會、拍照流程，會把語料切成活動流程主題，而不是 EV 主題。</td><td>stage, invite, like invite, photo, photos, photographer, photographers, gentlemen, ladies, everyone, audience, applause, presentation, show, unveil, reveal</td></tr><tr><td>人名與稱謂</td><td>這類詞通常代表主持人、設計師或主管名字，對 EV 主題分類沒有穩定意義。</td><td>mr, mrs, ms, mark, chris, robin, jeff</td></tr><tr><td>時間與年份泛詞</td><td>年份與時間單位本身通常不構成 EV 主題，除非研究問題特別要分析年份演進。</td><td>year, years, day, days, month, months, week, weeks, spring, summer, fall, winter, 2010, 2015, 2020, 2021, 2022, 2023, 2024, 2025</td></tr><tr><td>數字與保固模板詞</td><td>000、whichever comes 等來自保固/里程模板，容易產生低價值 topic。保留 mile/miles 可視研究是否分析續航；若續航主題受影響，不建議刪除 miles。</td><td>000, 100 000, 000 mile, 000 miles, whichever, whichever comes, comes first, unlimited mileage, scheduled maintenance, roadside assistance</td></tr><tr><td>市場與銷售泛詞</td><td>可描述品牌營運，但不直接對應 EV 技術；若研究包含市場策略，可改列為可選停用詞。</td><td>market, markets, sales, sell, selling, sold, customers, customer, people, owner, owners, buyer, buyers</td></tr><tr><td>價格購買泛詞</td><td>價格可作為市場議題，但目前 topic words 中常與口語購買建議混雜，若主題目標是 EV 技術，建議移除。</td><td>price, cost, affordable, buy, buying, pay, paid, value</td></tr><tr><td>地名與車展詞</td><td>多反映發表地點或車展場景，不是 EV 主題本身。</td><td>detroit, la, los, angeles, los angeles, america, china, us, u s, motor city, auto show, auto season</td></tr><tr><td>影片與頻道詞</td><td>來源於 YouTube/媒體語境，會干擾車輛主題。</td><td>video, videos, channel, subscribe, youtube, stream, streaming, clip, episode</td></tr><tr><td>一般評價形容詞</td><td>情緒或評價詞太泛化，不能區分 EV 子議題。</td><td>beautiful, nice, exciting, excited, impressive, amazing, perfect, strong, better, best, important, successful</td></tr><tr><td>內裝舒適泛詞</td><td>若研究主題聚焦 EV，這類座椅/內裝詞會形成與電動車無關的舒適配備主題；若要保留完整汽車產品分析，則可不刪。</td><td>seats, seat, interior, space, leather, heated, ventilated, cargo, cabin, comfort</td></tr><tr><td>車身外觀泛詞</td><td>外觀設計可形成非 EV 主題；若目標是電動車技術與市場，建議刪除或降權。</td><td>grille, rear, led, light, lights, headlights, tail, beam, signature, look, design, sketch, sketches, clay</td></tr><tr><td>一般資訊娛樂詞</td><td>Apple CarPlay/Android Auto 是車機配備，不直接代表 EV；若研究包含智慧座艙，則可保留。</td><td>audio, apple, carplay, apple carplay, android, android auto, touchscreen, screen, display, displays, information, navigation, functions</td></tr><tr><td>車門與空調操作詞</td><td>多是使用手冊或功能示範語言，不構成 EV 子題。</td><td>door, doors, tailgate, hood, temperature, climate control, key fob, footwell</td></tr><tr><td>非研究核心品牌/車系詞</td><td>A04 topic words 中出現部分品牌/車系或展演詞，若研究已用 Brand/Model 匿名化，殘留專名會造成偏移。</td><td>toyotacare, siriusxm, mymazda, mazda, mbux, amg, quattro, tnga, egmp, xse, xle, se, gt, gt3, k23, candy</td></tr></tbody></table></div><h3>建議保留的 EV 核心詞</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>類型</th><th>建議保留詞</th></tr></thead><tbody><tr><td>電動化核心</td><td>electric, ev, electrification, electrified, electric vehicle, electric car, battery electric</td></tr><tr><td>充電與補能</td><td>charging, charge, charger, charging station, charging stations, dc, fast charging, level 1, level 2, level 3</td></tr><tr><td>電池與能源</td><td>battery, battery pack, lithium, lithium ion, cells, kilowatt, kilowatt hour, kwh, volt</td></tr><tr><td>續航與效率</td><td>range, miles, kilometers, mpge, fuel economy, efficiency</td></tr><tr><td>動力與控制</td><td>motor, torque, regenerative, regenerative braking, regen, brake, braking, pedal</td></tr><tr><td>環境與政策語意</td><td>emissions, zero, co2, sustainable, climate, environment</td></tr></tbody></table></div>

## 使用原則

<aside class="table-note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</aside>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a05-6-stopwords/A05-6_stopword.md' | relative_url }}">A05-6_stopword.md</a></td><td>原始停用詞建議與完整 CountVectorizer 清單</td></tr></tbody></table>
</section>
</div>
