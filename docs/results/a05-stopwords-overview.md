---
title: A05 停用詞設計
description: A05 客製停用詞的三條版本線與人工收斂紀錄。
---

# A05｜停用詞設計

A05 依 A06 BERTopic representation 的殘留詞反覆修訂客製停用詞。目標是減少逐字稿口語、品牌／車款、產品展示與一般車評語境的干擾，同時保留電動化的關鍵語意。

<aside class="table-note"><strong>共同保留原則：</strong>不將 <code>electric</code>、<code>EV</code>、<code>charging</code>、<code>battery</code>、<code>range</code>、<code>motor</code>、<code>torque</code>、<code>hybrid</code>、<code>plug</code> 等 EV 語意錨點納入停用詞。</aside>

## 版本線

每個節點均可點入查看新增的停用詞分類、原因與原始檔。版本線依資料處理策略分開呈現，避免將不同語料的詞表混為同一份設定。

<section class="stopword-track" aria-labelledby="a05-6"><header><h2 id="a05-6">A05-6｜初步停用詞迭代</h2><p>從一般車輛與逐字稿雜訊出發，逐輪壓低非 EV 核心的產品展示、車機、賽道與銷售語境。</p></header><div class="stopword-line"><a class="stopword-step" href="{{ '/results/a05-6-stopwords.html' | relative_url }}"><strong>A05-6</strong><span>基礎詞表</span><small>建立 EV 核心詞保留與一般雜訊移除原則。</small></a><a class="stopword-step" href="{{ '/results/a05-6-1-stopwords.html' | relative_url }}"><strong>A05-6.1</strong><span>第一次增補</span><small>加入車機、展演與非 EV 性能殘留詞。</small></a><a class="stopword-step" href="{{ '/results/a05-6-2-stopwords.html' | relative_url }}"><strong>A05-6.2</strong><span>第二次增補</span><small>處理連線服務、銷售金融與賽道性能語境。</small></a><a class="stopword-step" href="{{ '/results/a05-6-3-stopwords.html' | relative_url }}"><strong>A05-6.3</strong><span>積極版本</span><small>進一步移除舒適、設計、維修與聲學等非核心語境。</small></a></div></section>
<section class="stopword-track" aria-labelledby="a05-8-repl"><header><h2 id="a05-8-repl">A05-8｜repl 詞表迭代</h2><p>以品牌／車款已替換為 Brand、Model 的語料為基礎，逐輪依 A06 representation 殘留詞增補。</p></header><div class="stopword-line"><a class="stopword-step" href="{{ '/results/a05-8-repl-stopwords.html' | relative_url }}"><strong>A05-8</strong><span>基礎詞表</span><small>先區分核心建議與可選擇停用詞。</small></a><a class="stopword-step" href="{{ '/results/a05-8-repl-1-stopwords.html' | relative_url }}"><strong>A05-8.1</strong><span>第一次增補</span><small>補入車機、影音、連線與產品展示殘留。</small></a><a class="stopword-step" href="{{ '/results/a05-8-repl-2-stopwords.html' | relative_url }}"><strong>A05-8.2</strong><span>第二次增補</span><small>補入功能詞、車款 trim 與市場展示殘留。</small></a><a class="stopword-step" href="{{ '/results/a05-8-repl-3-stopwords.html' | relative_url }}"><strong>A05-8.3</strong><span>第三次增補</span><small>處理代名詞、媒體語氣、UI 與一般車評語境。</small></a></div></section>
<section class="stopword-track" aria-labelledby="a05-8-orig-rev"><header><h2 id="a05-8-orig-rev">A05-8｜orig REV 詞表收斂</h2><p>處理原始語料中重新出現的品牌、車款、年份與影片敘事殘留，最後分為完整彙整與人工精選兩版。</p></header><div class="stopword-line"><a class="stopword-step" href="{{ '/results/a05-8-orig-rev-stopwords.html' | relative_url }}"><strong>A05-8 REV</strong><span>基礎詞表</span><small>以 A05-8 原則重新套用於 orig REV 語料。</small></a><a class="stopword-step" href="{{ '/results/a05-8-orig-rev-1-stopwords.html' | relative_url }}"><strong>A05-8.1 REV</strong><span>第一次增補</span><small>補入品牌車款、流程詞與外觀、車機、ADAS 殘留。</small></a><a class="stopword-step" href="{{ '/results/a05-8-orig-rev-2-stopwords.html' | relative_url }}"><strong>A05-8.2 REV</strong><span>第二次增補</span><small>補入駕乘、便利配備與市場展示殘留。</small></a><a class="stopword-step" href="{{ '/results/a05-8-orig-rev-3-stopwords.html' | relative_url }}"><strong>A05-8.3 REV</strong><span>第三次增補</span><small>僅依 default topic words 補入低解釋力殘留。</small></a><a class="stopword-step" href="{{ '/results/a05-8-orig-rev-all-stopwords.html' | relative_url }}"><strong>A05-8.4 all</strong><span>完整彙整</span><small>彙整各輪建議，保留完整的 36 類參考。</small></a><a class="stopword-step is-final" href="{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}"><strong>A05-8.4 human</strong><span>人工精選</span><small>人工收斂為較易維護的 12 類建議版。</small></a></div></section>

## 建議採用方式

<div class="card-grid">
<section class="section-card"><h3>探索與比較</h3><p>先從各分支的基礎版開始，逐輪對照 A06 的 topic words，確認雜訊是否持續降低。</p></section>
<section class="section-card"><h3>正式重跑</h3><p>依資料版本使用同一條版本線的累積詞表；不要混用 repl 與 orig REV 分支的詞表。</p></section>
<section class="section-card"><h3>人工收斂</h3><p><a href="{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}">A05-8.4 human</a> 是目前人工精選的建議版；all 版則保留為完整參考。</p></section>
</div>

## 原始資料

所有完整 Markdown 詞表與 A05-8.4 human 的 Word 檔都保留於對應詳細頁的「原始輸出」區。
