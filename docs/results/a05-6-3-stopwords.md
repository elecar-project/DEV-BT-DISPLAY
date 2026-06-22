---
title: A05-6.3 停用詞設計
description: A05-6｜初步停用詞迭代 的 A05-6.3 停用詞設計紀錄。
experiment_id: a05-6-3-stopwords
---

# A05-6.3｜停用詞設計

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
## 本版目的

進一步移除舒適、設計、維修與聲學等非核心語境。

<p class="section-intro">資料來源：</p>

## 停用詞分類與理由

<h3>新增停用詞表</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>討論、訪談與來源人物殘留詞</td><td>A06-6.2 仍出現 excitement/discussions、interviews、presentation、auto show 類主題，這些較像文本來源語境。</td><td>yes, hear, doesn, doesn doesn, stephen, bet, mentioned, did, ask, speak, dinner, dinner julia, subject, journalists, excitement, peter, happening, interviews, worst case, scenarios, worst, case, gm, north american, american, photography, presentations, presentation, premiere, world premiere</td></tr><tr><td>車機連線、智慧鑰匙與介面詞</td><td>A06-6.2 仍有 In-Car Technology、Smart Key、Digital Instrument Clusters、Driver Interface 等非電動化核心主題。</td><td>in car, in-car, connectivity, google, subscriptions, subscription, smart key, key, access, settings, controls, instrument, clusters, instrument clusters, digital instrument, intuitive, remote control, smart</td></tr><tr><td>內裝舒適、材質與控制細節詞</td><td>A06-6.2 仍有 Interior Comfort and Control、seat/console/material 類主題，與 EV 技術、能源或充電關聯較弱。</td><td>split, stitching, fit, center, material, offer, touch, plenty, position, backrest, sitting, lumbar, convenience, bench, dual, headroom, trimmed, 60 split, color, upholstery, quality, premium</td></tr><tr><td>外觀、美學、燈具與輪圈詞</td><td>A06-6.2 仍有 Design Aesthetics、Lighting Features、Wheel/Rim Designs 等外觀展示主題。</td><td>rim, rims, wheel design, rim designs, lighting features, aesthetics, aesthetic, sleek, distinctive, logo, designs, designed, aerodynamic, aerodynamics, dynamic, lower, futuristic, customization</td></tr><tr><td>銷售、合作、產業與管理詞</td><td>這類詞會形成 market/leadership/partnership/ownership 類商業敘事，而非 EV 技術主題。</td><td>financing, partnerships, partnership, ownership, evolution, management, leadership, commitment, committed, business, industry, market expansion</td></tr><tr><td>保養服務殘留詞</td><td>A06-6.2 仍有 Hybrid Vehicle Maintenance Plans，因此補入殘留服務模板詞。</td><td>scheduled, term, backed, 36 miles, 150, 24, 100, 10, plans</td></tr><tr><td>非 EV 高性能、賽道與試駕詞</td><td>這些詞會讓主題偏向燃油性能、賽道、底盤或試駕體驗，而非電動化核心。</td><td>v8, engines, manual transmission, transmission, gear, mode, mode mode, drive mode, race, gt4, traction, axle, corners, stability, maneuverability, pickup, truck, texas, conditions, test drive, test drives</td></tr><tr><td>聲學與安靜體驗詞</td><td>A06-6.2 仍出現 quiet/silence 類主題，若研究不分析 EV NVH，可作為停用詞。</td><td>quiet, quietest, quietness, silence, silent, ear</td></tr><tr><td>設計敘事與抽象評價詞</td><td>殘留的 storytelling/creative/product-design 詞會形成抽象美學主題，對 EV 子題辨識幫助有限。</td><td>thing, introduce, said, talk, media, series, eyes, spyder, success, work, movies, challenge, super, passionate, trd, style, factory 56, factory, pilot</td></tr></tbody></table></div><h3>仍建議保留的 EV 核心詞</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>類型</th><th>建議保留詞</th></tr></thead><tbody><tr><td>電動化核心</td><td>electric, ev, electrification, electrified, electric vehicle, electric car, battery electric</td></tr><tr><td>充電與補能</td><td>charging, charge, charger, charging station, charging stations, dc, fast charging, level 1, level 2, level 3</td></tr><tr><td>電池與能源</td><td>battery, battery pack, lithium, lithium ion, cells, kilowatt, kilowatt hour, kwh, volt</td></tr><tr><td>續航與效率</td><td>range, miles, kilometers, mpge, fuel economy, efficiency</td></tr><tr><td>動力與控制</td><td>motor, torque, regenerative, regenerative braking, regen, brake, braking, pedal</td></tr><tr><td>環境與政策語意</td><td>emissions, zero, co2, sustainable, sustainability, climate policy, environment, carbon</td></tr></tbody></table></div>

## 使用原則

<div class="table-note" role="note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</div>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a05-6-3-stopwords/A05-6.3_stopword.md' | relative_url }}">A05-6.3_stopword.md</a></td><td>原始停用詞建議與完整 CountVectorizer 清單</td></tr></tbody></table>
</section>
</div>
