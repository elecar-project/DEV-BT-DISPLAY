---
title: A05-8.1 REV 停用詞設計
description: A05-8｜orig REV 詞表收斂 的 A05-8.1 REV 停用詞設計紀錄。
---

# A05-8.1 REV｜停用詞設計

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 版本設定

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>版本線</td><td>A05-8｜orig REV 詞表收斂</td></tr>
<tr><td>資料版本</td><td>orig REV + tok + 段落 12-80</td></tr>
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

補入品牌車款、流程詞與外觀、車機、ADAS 殘留。

<p class="section-intro">判斷原則：沿用 A05-8 對 EV 核心詞的保留原則，仍不移除 electric、ev、charging、battery、range、motor、torque、hybrid、plug 等 EV 主題錨點。這一版主要補上 orig 語料未替換品牌/車款後重新浮出的品牌車型詞、影片流程詞、MMR 漏出的英文功能詞，以及會形成非 EV 主題的內裝、車機、外觀、ADAS、安全與賽道展示詞。</p>

## 停用詞分類與理由

<h3>A05-8.1-REV 新增停用詞</h3><div class="table-scroll"><table class="stopword-table"><thead><tr><th>停用詞類型</th><th>原因</th><th>停用詞</th></tr></thead><tbody><tr><td>orig 品牌與車款詞</td><td>orig 語料未把品牌/車款替換成 brand、model，因此 BMW、Hyundai、Kia、Nissan、Audi、Toyota 等品牌車款重新形成獨立 topic，會降低 EV 子主題可解釋性。</td><td>bmw, hyundai, kia, nissan, nissanusa, toyota, lexus, audi, volvo, mercedes, benz, tesla, polestar, porsche, ferrari, fiat, acura, chrysler, ford, infiniti, infinity, mclaren, ioniq, ev6, ev9, ev4, e6, leaf, aria, ariya, altima, prius, sonata, elantra, camry, corolla, rav4, highlander, crown, xc40, xc90, ex90, s60, s90, v60, v90, i3, i4, q5, q8, a3, a6, a7, a8, tron, quattro, eq, eqe, eqs, glb, amg, gt, gt3, taycan, panamera, mustang, mach, pacifica, rogue, nsx, ilx, lc, lc500, nx, ux, rx, ls, hs, accord, cayenne, id4, xrt, trd</td></tr><tr><td>影片流程、寒暄與口語殘留</td><td>A06-8-REV 的 most_topics topic 0 顯示 subscribe/channel/video/guys 等影片流程詞仍形成 topic；其他泛用口語詞則集中在大 topic 或 MMR representation。</td><td>subscribe, channel, video, watching, guys, oh, ll, come, coming, invite, live, clips, pleasure, awesome, ready, glad, amazing, love, shoot, yes, wait, test, actually</td></tr><tr><td>英文功能詞與 MMR 漏網詞</td><td>MMR representation 中仍出現 and/to/we/on/your 等功能詞；雖然 sklearn stopwords 已作用於 vectorizer，但為了 representation 後處理也能濾除，補進客製清單。</td><td>and, to, we, us, me, our, your, on, an, as, at, are, be, can, do, re, here, there, all, one, more, very, which, will</td></tr><tr><td>泛用敘事與團隊流程詞</td><td>這些詞在 best_balance 的大型 topic 中高頻出現，但多反映敘事流程、團隊協作或年份/標配資訊，不是 EV 技術錨點。</td><td>think, people, team, work, focus, lot, say, time, way, first, standard, year, company, built</td></tr><tr><td>內裝、空間與車機資訊</td><td>這些詞形成內裝、車機、影音、導航或操作介面 topic，與 EV 能源、電池、充電、電驅主題關聯較弱。</td><td>materials, material, upholstery, cabin, passengers, panel, storage, trunk, console, center, central, control, controls, buttons, screens, climate, air, cockpit, hyperscreen, alexa, amazon, app, apps, iphone, mobile, devices, mmi, music, compatibility, services, touch, connect, sound, speaker, speakers, navigator, route, view, voice, settings, guidance, wood, nice</td></tr><tr><td>外觀、車身與設計展示詞</td><td>A05-8 已建議停用 design/light/line 等詞；A06-8-REV 又看到 grill/front/headlamp/taillights 等同類詞。</td><td>grill, front, body, lower, effect, frame, sporty, vertical, running, nose, side, exterior, sleek, wider, headlamp, headlamps, headlight, horizontal, lamps, width, iconic</td></tr><tr><td>ADAS、安全與一般駕輔詞</td><td>assist/parking/lane/blind/safety 形成獨立 ADAS/安全 topic；若研究目標聚焦 EV 技術與能源敘事，建議停用。</td><td>safety, assist, parking, lane, blind, alert, traffic, emergency, pedestrian, pedestrians, radar, detection, detect, detects</td></tr><tr><td>賽道、性能展示與非 EV 車評詞</td><td>這些詞偏向跑車、賽道、底盤、燃油經濟或一般車評性能展示，容易形成非 EV 主題。</td><td>racing, race, racetrack, track, sports, supercar, chassis, suspension, cornering, corners, roadster, spyder, road, steering, fuel, gallon, economy, litre, liters, exhaust, midnight, edition, platinum, limited, generation, compact, grand, series, kidney, meters, sweden</td></tr></tbody></table></div>

## 使用原則

<aside class="table-note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</aside>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a05-8-orig-rev-1-stopwords/A05-8.1-REV_stopword.md' | relative_url }}">A05-8.1-REV_stopword.md</a></td><td>原始停用詞建議與完整 CountVectorizer 清單</td></tr></tbody></table>
</section>
</div>
