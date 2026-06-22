---
title: A05-8 REV 停用詞設計
description: A05-8｜orig REV 詞表收斂 的 A05-8 REV 停用詞設計紀錄。
experiment_id: a05-8-orig-rev-stopwords
---

# A05-8 REV｜停用詞設計

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
## 本版目的

以 A05-8 原則重新套用於 orig REV 語料。

<p class="section-intro">判斷原則：保留與電動車技術、能源、充電、電池、續航、電驅、再生煞車、混合動力直接相關的詞；移除逐字稿口語填充詞、品牌/車款替換佔位詞、影片寒暄、泛用汽車詞，以及會讓 BERTopic 產生非 EV 主題的外觀、內裝、車機、操作示範詞。</p>

## 停用詞分類與理由

<h3>核心建議停用詞</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>repl 佔位詞與衍生片語</td><td>repl 語料把品牌/車款替換成 brand、model 後，這些詞在 topic words 中高頻出現，但不提供可解釋的 EV 語意，會形成「品牌/車款佔位」主題。</td><td>brand, model, brand model, brand brand, new brand, new model, brand charge</td></tr><tr><td>逐字稿寒暄與影片流程詞</td><td>這些詞來自主持人開場、結尾、問候或訪談流程，與電動車主題無直接關聯，且已形成獨立 topic。</td><td>thank, thanks, welcome, bye, joining, today, doing, hope, good, great, gentlemen, questions</td></tr><tr><td>口語填充與對話慣用詞</td><td>don know、yeah、okay 等詞反映口語互動，不代表 EV 技術或產品語意，會稀釋 topic words。</td><td>okay, yeah, don, know, don know, know don, said, let, going, want, right, really, just, like, kind, sort, ve</td></tr><tr><td>過度泛用汽車詞</td><td>car、vehicle、new 在幾乎所有汽車文本都會出現，區分力低；若保留，容易讓 topic words 變成泛汽車描述，而不是 EV 子主題。</td><td>car, cars, vehicle, vehicles, new, available</td></tr><tr><td>人名、來源與辨識雜訊</td><td>topic words 中出現主持人/受訪者姓名、來源名稱或疑似轉寫/品牌殘留，對 EV 主題分類沒有穩定解釋力。</td><td>robin, chris, auto evolution, candy, k23</td></tr><tr><td>保固/數字片段雜訊</td><td>000、whichever comes 等通常來自保固條款句型，容易形成售後條款或數字噪音 topic；若研究不分析保固，建議停用。</td><td>000, 000 mile, 000 miles, whichever, whichever comes</td></tr></tbody></table></div><h3>可選擇停用詞</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>外觀/設計主題詞</td><td>這些詞會讓 BERTopic 分出外觀、燈具、車身線條、設計流程等主題，但它們多半不是 EV 專屬語意。</td><td>design, look, beautiful, grille, rear, led, light, lights, headlights, signature, laser, tail, beam, line, lines, shape, stance, hood, sketch, sketches, clay, designers, black</td></tr><tr><td>輪圈/等級/尺寸詞</td><td>多出現在配備與車型等級介紹，與 EV 核心主題關聯弱。</td><td>wheels, wheel, alloy, alloy wheels, inch, grades, xse, xle, se</td></tr><tr><td>內裝/座椅/空間詞</td><td>這些詞會產生內裝舒適性或行李空間主題；若目標是 EV 技術主題，可視為非核心。</td><td>seats, seat, seating, leather, comfort, interior, massage, driver seat, comfort seat, trimmed, inside, space, room, cargo, cubic, cubic feet, feet, luggage, row</td></tr><tr><td>車機/娛樂/連線詞</td><td>topic words 中已形成 Apple CarPlay、Android Auto、MBUX、Blue Link 等車機主題；這些不是 EV 技術本體。</td><td>audio, apple, carplay, apple carplay, android, android auto, wireless, touchscreen, mbux, display, displays, screen, navigation, functions, head display, information, blue link, link, google, profile, smartphone, phone, connected, remote</td></tr><tr><td>操作示範詞</td><td>這些詞多來自車評影片中示範按鍵、尾門、門把或介面操作，不代表 EV 主題。</td><td>door, temperature, tailgate, button, open, press, turn, release, cover, key, digital key, digital</td></tr><tr><td>ICE 或非 EV 車型語境</td><td>若研究只看純 EV/電動化敘事，傳統燃油引擎、變速箱、汽缸等詞會引入 ICE 主題；但若要比較 hybrid/ICE，請不要停用整組。</td><td>engine, liter, cylinder, transmission, turbo, gas</td></tr><tr><td>車身級距與市場定位詞</td><td>sedan、coupe、SUV、luxury 等會形成車型級距/市場定位主題；若 EV 主題要更聚焦，建議停用。</td><td>sedan, coupe, midsize, segment, suv, fleet, luxury</td></tr><tr><td>市場/商業泛詞</td><td>這些詞可解釋為市場或品牌策略，但不是 EV 技術語意；若研究不做市場策略分析，建議停用。</td><td>product, products, customer, customers, sales, market, markets, global, world, china, america</td></tr></tbody></table></div>

## 使用原則

<aside class="table-note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</aside>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a05-8-orig-rev-stopwords/A05-8_stopword.md' | relative_url }}">A05-8_stopword.md</a></td><td>原始停用詞建議與完整 CountVectorizer 清單</td></tr></tbody></table>
</section>
</div>
