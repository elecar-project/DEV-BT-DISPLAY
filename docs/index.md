---
title: 研究總覽
description: 從逐字稿到主題模型，探索電動車產業的論述與變化。
---

<section class="hero">
  <div class="hero-copy">
    <p class="eyebrow"><span class="status-dot" aria-hidden="true"></span> EV INDUSTRY · TEXT & TOPIC RESEARCH</p>
    <h1>從文本出發，<br>理解產業的變化。</h1>
    <p class="hero-description">整理電動車產業的影片逐字稿、資料處理流程與 BERTopic 實驗。讓每一個主題，都能回到它的資料與方法。</p>
    <div class="hero-actions">
      <a class="button button-primary" href="{{ '/results.html' | relative_url }}">探索實驗結果 <span aria-hidden="true">↗</span></a>
      <a class="button button-secondary" href="{{ '/datasets.html' | relative_url }}">查看資料與原文 <span aria-hidden="true">→</span></a>
    </div>
    <p class="hero-footnote">DEV-BT 研究檔案館 <span aria-hidden="true">／</span> 方法、資料、結果，一起閱讀。</p>
  </div>
  <aside class="hero-panel" aria-label="研究資料規模">
    <p class="panel-label">THE CORPUS <span aria-hidden="true">↗</span></p>
    <div class="metric"><strong>434<small>份</small></strong><span>主要清理後逐字稿</span><small>由 454 份原始文本篩選而來</small></div>
    <div class="metric-pair">
      <div class="metric"><strong>14</strong><span>可比對資料版本</span></div>
      <div class="metric"><strong>64</strong><span>歷史結果與比較頁</span></div>
    </div>
    <a class="panel-source" href="{{ '/data-notes.html' | relative_url }}">查看統計範圍與資料核對 <span aria-hidden="true">→</span></a>
  </aside>
</section>

<div class="section-heading"><div><p class="eyebrow">START EXPLORING</p><h2 id="explore">依照你的問題，選一個入口。</h2></div><span class="section-number" aria-hidden="true">01 / EXPLORE</span></div>

<div class="research-grid">
  <a class="research-card" href="{{ '/results.html' | relative_url }}"><span class="card-index">01 <span aria-hidden="true">↗</span></span><h3>模型說了什麼？</h3><p>沿著實驗地圖，瀏覽主題語意、離群比例與不同參數的比較。</p><span class="card-link">實驗結果</span></a>
  <a class="research-card" href="{{ '/datasets.html' | relative_url }}"><span class="card-index">02 <span aria-hidden="true">↗</span></span><h3>資料如何改變？</h3><p>選擇兩個資料版本，搜尋原文，逐段檢查清理前後的差異。</p><span class="card-link">資料集與文本比對</span></a>
  <a class="research-card" href="{{ '/method.html' | relative_url }}"><span class="card-index">03 <span aria-hidden="true">↗</span></span><h3>結果怎麼產生？</h3><p>從逐字稿整理、品牌處理到分群，理解不同階段的研究選擇。</p><span class="card-link">方法與分析流程</span></a>
</div>

<section class="research-reading" aria-labelledby="reading-title">
  <div><p class="eyebrow">READ WITH CONTEXT</p><h2 id="reading-title">數字相同，<br>單位未必相同。</h2></div>
  <div><p>一份逐字稿可能切成許多句子或小段；不同前處理與篩選條件，也會得到不同的輸入筆數。比較模型前，先確認樣本、分段方式與統計分母。</p><a class="text-link" href="{{ '/data-notes.html' | relative_url }}">了解影片、段落、主題的差別 <span aria-hidden="true">→</span></a></div>
</section>

<div class="section-heading"><div><p class="eyebrow">RESEARCH PATH</p><h2 id="research-path">沿著資料，回看研究流程。</h2></div><span class="section-number" aria-hidden="true">02 / PROCESS</span></div>

<ol class="process-steps">
  <li><span>01 / COLLECT</span><strong>收集與篩選</strong><p>454 份原始逐字稿，保留 434 份主要分析文本。</p><a href="{{ '/datasets.html' | relative_url }}">資料版本 →</a></li>
  <li><span>02 / PREPARE</span><strong>清理與分段</strong><p>比較原文、刪除品牌與替換品牌等處理版本。</p><a href="{{ '/method.html' | relative_url }}">研究方法 →</a></li>
  <li><span>03 / MODEL</span><strong>探索與建模</strong><p>A03–A05 參數探索，接續 M01–M03 主程式。</p><a href="{{ '/results.html' | relative_url }}">實驗地圖 →</a></li>
  <li><span>04 / COMPARE</span><strong>驗證與解讀</strong><p>透過品牌處理、年代切分與樣本篩選比較結果。</p><a href="{{ '/results/t01-overview.html' | relative_url }}">驗證分支 →</a></li>
</ol>
