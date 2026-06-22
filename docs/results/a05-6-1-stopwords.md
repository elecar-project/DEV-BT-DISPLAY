---
title: A05-6.1 停用詞設計
description: A05-6｜初步停用詞迭代 的 A05-6.1 停用詞設計紀錄。
experiment_id: a05-6-1-stopwords
---

# A05-6.1｜停用詞設計

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
## 本版目的

加入車機、展演與非 EV 性能殘留詞。

<p class="section-intro">資料來源：</p>

## 停用詞分類與理由

<h3>新增停用詞表</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>一般產品與配備泛詞</td><td>A06-6 中仍反覆出現 available、standard、features，但這些詞通常描述配備有無，不能區分 EV 子題。</td><td>available, standard, features, feature, class, segment, line, lines, models</td></tr><tr><td>逐字稿與直播殘留詞</td><td>多來自主持人、直播問答、發表會互動，會形成「Audience Engagement」類非 EV 主題。</td><td>time, way, ll, ve, questions, question, hey, watching, watch, soon, guys, pleasure, live, hi, conference, ready, glad, hashtag, talking, coming, enjoy, enjoyed, appreciate, happy, moment, guests, guest, event, events, shows</td></tr><tr><td>車機與裝置配備詞</td><td>A06-6 中形成 Wireless Multimedia Connectivity 等主題；若研究核心不是智慧座艙，建議移除以避免偏離 EV 技術。</td><td>wireless, inch, music, maps, compatibility, multimedia, iphone, smartphone, mobile, mobile devices, devices, device, apps, speaker, jbl, connects, alexa</td></tr><tr><td>內裝空間與展示詞</td><td>room/passengers/seating/trunk 類詞會形成內裝舒適或置物主題，與 EV 研究核心關聯較弱。</td><td>room, passengers, passenger, seating, materials, row, second row, trunk, compartment, cubic feet, storage, comfortable, spacious, air, degrees, pins</td></tr><tr><td>外觀、車型與設計流程詞</td><td>wheel/steering/headlamps/sedan/suv/designer 類詞會讓主題偏向外觀、車型或設計流程，而非電動化。</td><td>wheel, wheels, steering, steering wheel, alloy wheels, inch wheels, headlamps, lamps, exterior, roof, coupe, sedan, sedans, suv, designer, designers, inspiration, sketching, modern, convertible</td></tr><tr><td>公司職稱與發表流程詞</td><td>president/vice/company/launch 多反映發表者或公司敘事，不是穩定的 EV 技術主題。</td><td>president, vice, vice president, general, general manager, chief, ceo, company, team, launch, global</td></tr><tr><td>保固與服務模板詞</td><td>A06-6 最低 noise 設定仍產生保固/維修服務主題；這些通常是銷售模板，不是 EV 技術或市場實質主題。</td><td>warranty, limited warranty, backed warranty, maintenance plan, mileage, 100 mile, 150 miles, mile powertrain, assistance, hour, long term</td></tr><tr><td>非 EV 性能與展演詞</td><td>engine/sound/racing/racetrack 容易形成燃油性能或展演主題；若聚焦 EV，建議移除。</td><td>engine, sound, noise, racing, racetrack, sports</td></tr></tbody></table></div><h3>仍建議保留的 EV 核心詞</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>類型</th><th>建議保留詞</th></tr></thead><tbody><tr><td>電動化核心</td><td>electric, ev, electrification, electrified, electric vehicle, electric car, battery electric</td></tr><tr><td>充電與補能</td><td>charging, charge, charger, charging station, charging stations, dc, fast charging, level 1, level 2, level 3</td></tr><tr><td>電池與能源</td><td>battery, battery pack, lithium, lithium ion, cells, kilowatt, kilowatt hour, kwh, volt</td></tr><tr><td>續航與效率</td><td>range, miles, kilometers, mpge, fuel economy, efficiency</td></tr><tr><td>動力與控制</td><td>motor, torque, regenerative, regenerative braking, regen, brake, braking, pedal</td></tr><tr><td>環境與政策語意</td><td>emissions, zero, co2, sustainable, climate, environment, carbon</td></tr></tbody></table></div>

## 使用原則

<aside class="table-note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</aside>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a05-6-1-stopwords/A05-6.1_stopword.md' | relative_url }}">A05-6.1_stopword.md</a></td><td>原始停用詞建議與完整 CountVectorizer 清單</td></tr></tbody></table>
</section>
</div>
