---
title: A05-8.2 REV 停用詞設計
description: A05-8｜orig REV 詞表收斂 的 A05-8.2 REV 停用詞設計紀錄。
---

# A05-8.2 REV｜停用詞設計

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 版本設定

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>版本線</td><td>A05-8｜orig REV 詞表收斂</td></tr>
<tr><td>資料版本</td><td>orig REV + tok + 段落 12-80</td></tr>
<tr><td>版本定位</td><td>第二次增補</td></tr>
<tr><td>分類筆數</td><td>8 類</td></tr>
</tbody></table>

### 核心原則

<p>保留 EV 語意錨點：<code>electric、EV、charging、battery、range、motor、torque、hybrid、plug</code>。</p>

### 導覽

<p><a href="{{ '/results/a05-stopwords-overview.html' | relative_url }}">回到 A05 停用詞總覽</a></p>
</aside>

<section markdown="1">
## 本版目的

補入駕乘、便利配備與市場展示殘留。

<p class="section-intro">判斷原則：A05-8.2-REV 沿用 A05-8.1-REV 的品牌/車款、影片流程、功能詞、內裝車機、外觀、ADAS、安全與賽道展示停用方向。這一輪新增 A06-8.1 後仍殘留的口語泛詞、駕駛者敘事詞、內裝空間與車機細項、更多 ADAS/便利配備詞，以及更細的車款/年份/市場展示詞。仍不建議停用 electric、ev、evs、charging、battery、range、motor、torque、horsepower、hybrid、plug 等 EV 或電驅語意錨點。</p>

## 停用詞分類與理由

<h3>A05-8.2-REV 新增停用詞</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>口語與泛用敘事殘留</td><td>A06-8.1 仍出現 right、going、want、make、years、important 等詞，會讓大型 topic 變成逐字稿互動或泛敘事，而不是 EV 子題。</td><td>right, going, want, make, years, important, comes, day, question, watch, videos, photos, hi, stage</td></tr><tr><td>駕駛者與一般駕乘敘事</td><td>driver、drivers、drive 相關 topic 中有大量一般試駕敘事；保留 EV drivetrain 相關詞，但補掉泛用駕駛者與非技術駕乘詞。</td><td>driver, drivers, ride, roads, take, no</td></tr><tr><td>內裝空間、舒適與便利配備</td><td>A06-8.1 仍分出 comfort、cargo、passenger、legroom、heated、moonroof、trim 等內裝與便利配備 topic，非 EV 技術核心。</td><td>comfort, comfortable, cargo, passenger, legroom, little, modern, heated, moonroof, trim, convenience, outlet, cord, cable, qi, keyless, fob</td></tr><tr><td>車機、導航、影音與介面</td><td>auto、radio、infotainment、maps、tablet、jbl、bose 等仍形成車機/影音 topic。</td><td>auto, radio, connectivity, infotainment, access, remotely, user, tablet, maps, jbl, bose, watts, wi, fi, menu, camera, destination, directions, sensors, head</td></tr><tr><td>ADAS、停車與安全細項</td><td>A05-8.1 已移除 broad ADAS 詞，但 A06-8.1 仍保留 spot、park、monitor、cross、cruise、collision、airbags 等細項。</td><td>spot, park, monitor, cross, distance, cruise, collision, airbags, brake, oncoming, avoid, safest</td></tr><tr><td>外觀、套件與展示語境</td><td>仍有外觀細節、套件、年份、上市展示與非 EV 產品敘事詞。</td><td>2018, 2019, 2020, 2021, 2025, 328, 580, 918, a4, i5, i7, x6, byd, sentra, kicks, avalon, niro, sportage, optima, sportback, v8, turbocharged, minivans, hatchback, segment, mode, modes, grade, premium, flagship, le</td></tr><tr><td>設計流程、品牌文化與市場展示</td><td>prototype/prototypes、student/culture、program/proposals、heritage 等讓 topic 偏向品牌敘事或設計流程。</td><td>prototype, prototypes, culture, student, doubt, trust, program, proposals, proportions, heritage, art, fiction, vr, studio, started, deliver, promotional, leader, inventory, manufacturing, market</td></tr><tr><td>其他非 EV 車評與展示殘留</td><td>車評細節或場景詞仍反覆出現，但與 EV 技術、能源、充電、電池、電驅關係弱。</td><td>top, soft, pins, underneath, wheelbase, problems, pressure, launch, launched, powerful, hassle, shanghai, thomas, tom, italy, prix, turin, group, munich, factory, europe, japanese, scandinavian, lincoln, andy</td></tr></tbody></table></div>

## 使用原則

<aside class="table-note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</aside>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a05-8-orig-rev-2-stopwords/A05-8.2-REV_stopword.md' | relative_url }}">A05-8.2-REV_stopword.md</a></td><td>原始停用詞建議與完整 CountVectorizer 清單</td></tr></tbody></table>
</section>
</div>
