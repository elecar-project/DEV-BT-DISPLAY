---
title: A05-6.2 停用詞設計
description: A05-6｜初步停用詞迭代 的 A05-6.2 停用詞設計紀錄。
experiment_id: a05-6-2-stopwords
---

# A05-6.2｜停用詞設計

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
## 本版目的

處理連線服務、銷售金融與賽道性能語境。

<p class="section-intro">資料來源：</p>

## 停用詞分類與理由

<h3>新增停用詞表</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>逐字稿、會議與線上互動殘留詞</td><td>A06-6.1 的 LLM label 仍出現 Online Engagement and Interaction、Meeting Discussions、Audience Engagement in EV Content，這些反映資料來源互動語境，不是 EV 子題。</td><td>meet, everybody, hello, liked, yeah, oh, forget, shoot, mike, able, answer, comments, comment, text, rest, fine, okay, stay, stay tuned, end, seeing, forward seeing, jim, chad, kurt, broadcast, online, interaction, meeting, discussions, discussion, big deal, careful, opportunity</td></tr><tr><td>車機連線與數位服務詞</td><td>A06-6.1 仍出現 connected services、digital key、cockpit display 等非電動化主題；若本研究不分析智慧座艙，建議移除。</td><td>connected, connect, services, phone, speakers, messages, drivers, infotainment, blue link, blue, digital, digital key, remote, compatible, cockpit, augmented reality, reality, interface</td></tr><tr><td>內裝舒適與置物細節詞</td><td>cubic feet、legroom、console、climate 等會讓主題偏向內裝規格，不是 EV 技術或能源議題。</td><td>cubic, feet, climate, second, panel, fold, folded, console, center console, luggage, legroom, lumbar support, capacity, sit, adjustable, automatic climate, zone, 40</td></tr><tr><td>外觀、車身形式與設計細節詞</td><td>A06-6.1 仍有 sporty design、front design、wheel design、crossover design 等外觀/車型主題，與 EV 核心議題關聯較弱。</td><td>body, shape, grill, headlight, taillights, lighting, laser, stance, alloy, black, midsize, midsized, cabriolet, crossover, flagship, touring</td></tr><tr><td>情緒、創作與設計流程詞</td><td>這類詞形成 Passion、Creative Design、Breathtaking Design 等抽象主題，對研究型 topic label 穩定性幫助有限。</td><td>love, passion, attention, joy, special, elegant, details, process, science fiction, artists, creative, breathtaking</td></tr><tr><td>銷售、金融與行銷詞</td><td>pricing/financing/inventory/dealers/marketing 反映銷售流程或商業敘事，若研究焦點是 EV 技術與環境語意，建議移除。</td><td>pricing, inventory, bank, pre, dealers, dealer, marketing, business strategy</td></tr><tr><td>發表活動與高階主管殘留詞</td><td>executive、international coverage、event highlights 類詞仍把主題推向發表會或媒體報導流程。</td><td>executive, international, coverage, highlights, auto coverage</td></tr><tr><td>保固與服務殘留詞</td><td>A06-6.1 仍出現 EV Maintenance and Roadside Assistance，多屬服務模板，不是 EV 技術核心。</td><td>roadside, unlimited, limited, maintenance, warranties, mile limited, hybrid 10, 25 miles</td></tr><tr><td>非 EV 性能、賽道與聲學詞</td><td>turbo/exhaust/motorsport/suspension/chassis 等偏向燃油性能、底盤或展演敘事；若只分析電動化，建議移除。</td><td>turbo, exhaust, acoustic, whisper, track, motorsport, sport, suspension, chassis, handling, dynamics, agile</td></tr></tbody></table></div><h3>仍建議保留的 EV 核心詞</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>類型</th><th>建議保留詞</th></tr></thead><tbody><tr><td>電動化核心</td><td>electric, ev, electrification, electrified, electric vehicle, electric car, battery electric</td></tr><tr><td>充電與補能</td><td>charging, charge, charger, charging station, charging stations, dc, fast charging, level 1, level 2, level 3</td></tr><tr><td>電池與能源</td><td>battery, battery pack, lithium, lithium ion, cells, kilowatt, kilowatt hour, kwh, volt</td></tr><tr><td>續航與效率</td><td>range, miles, kilometers, mpge, fuel economy, efficiency</td></tr><tr><td>動力與控制</td><td>motor, torque, regenerative, regenerative braking, regen, brake, braking, pedal</td></tr><tr><td>環境與政策語意</td><td>emissions, zero, co2, sustainable, climate policy, environment, carbon</td></tr></tbody></table></div>

## 使用原則

<div class="table-note" role="note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</div>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a05-6-2-stopwords/A05-6.2_stopword.md' | relative_url }}">A05-6.2_stopword.md</a></td><td>原始停用詞建議與完整 CountVectorizer 清單</td></tr></tbody></table>
</section>
</div>
