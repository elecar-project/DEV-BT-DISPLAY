---
title: A04 UMAP 整體比較
description: A04 UMAP 與 HDBSCAN 聯合搜尋結果。
---

# A04｜UMAP 整體比較

A04 階段同時探索 UMAP 降維與 HDBSCAN 分群設定；每個資料版本均保留最低雜訊、最多主題與最佳平衡三種候選策略。

## 最佳平衡跨資料集比較

此表將各資料版本的最佳平衡候選並列，便於比較資料處理策略與年份切分造成的差異；分數僅適合搭配 noise ratio、主題數與主題集中度共同解讀。

<div class="table-scroll"><table class="umap-overview-table"><thead><tr><th>資料版本</th><th>UMAP</th><th>HDBSCAN</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>balance score</th></tr></thead><tbody><tr><td><a href="{{ '/results/a04-2-del-tok.html' | relative_url }}">A04-2｜del + tok</a></td><td>neighbors 5 / components 5 / min dist 0.0</td><td>cluster 50 / samples 5.0 / eom / eps 0.0</td><td>148</td><td>34.16%</td><td>2.76%</td><td>0.8762121115841646</td></tr><tr><td><a href="{{ '/results/a04-3-del-tok-para12-80.html' | relative_url }}">A04-3｜del + tok + 段落 12-80</a></td><td>neighbors 5 / components 5 / min dist 0.0</td><td>cluster 50 / samples 5.0 / eom / eps 0.2</td><td>36</td><td>26.81%</td><td>6.67%</td><td>0.8626222019186842</td></tr><tr><td><a href="{{ '/results/a04-5-repl-tok.html' | relative_url }}">A04-5｜repl + tok</a></td><td>neighbors 5 / components 5 / min dist 0.0</td><td>cluster 50 / samples 5.0 / eom / eps 0.1</td><td>155</td><td>34.30%</td><td>2.61%</td><td>0.8759705424880171</td></tr><tr><td><a href="{{ '/results/a04-6-repl-tok-para12-80.html' | relative_url }}">A04-6｜repl + tok + 段落 12-80</a></td><td>neighbors 5 / components 5 / min dist 0.0</td><td>cluster 50 / samples 5.0 / eom / eps 0.2</td><td>40</td><td>28.38%</td><td>6.29%</td><td>0.8723902350154855</td></tr><tr><td><a href="{{ '/results/a04-7-orig-tok.html' | relative_url }}">A04-7｜orig + tok</a></td><td>neighbors 5 / components 10 / min dist 0.0</td><td>cluster 50 / samples 10.0 / leaf / eps 0.2</td><td>130</td><td>31.36%</td><td>3.01%</td><td>0.8815293416554277</td></tr><tr><td><a href="{{ '/results/a04-8-orig-tok-para12-80.html' | relative_url }}">A04-8｜orig + tok + 段落 12-80</a></td><td>neighbors 5 / components 5 / min dist 0.0</td><td>cluster 50 / samples 5.0 / eom / eps 0.2</td><td>62</td><td>27.68%</td><td>4.07%</td><td>0.8835308908045976</td></tr><tr><td><a href="{{ '/results/a04-b01-08-19.html' | relative_url }}">A04 B01｜2008-2019</a></td><td>neighbors 5 / components 15 / min dist 0.0</td><td>cluster 50 / samples 5.0 / leaf / eps 0.2</td><td>66</td><td>28.87%</td><td>3.24%</td><td>0.88584229390681</td></tr><tr><td><a href="{{ '/results/a04-b01-20-25.html' | relative_url }}">A04 B01｜2020-2025</a></td><td>neighbors 5 / components 15 / min dist 0.0</td><td>cluster 50 / samples 5.0 / eom / eps 0.2</td><td>59</td><td>21.60%</td><td>4.49%</td><td>0.8962359550561798</td></tr></tbody></table></div>

## 個別實驗

可直接查看：[A04-2｜del + tok]({{ '/results/a04-2-del-tok.html' | relative_url }})、[A04-3｜del + tok + 段落 12-80]({{ '/results/a04-3-del-tok-para12-80.html' | relative_url }})、[A04-5｜repl + tok]({{ '/results/a04-5-repl-tok.html' | relative_url }})、[A04-6｜repl + tok + 段落 12-80]({{ '/results/a04-6-repl-tok-para12-80.html' | relative_url }})、[A04-7｜orig + tok]({{ '/results/a04-7-orig-tok.html' | relative_url }})、[A04-8｜orig + tok + 段落 12-80]({{ '/results/a04-8-orig-tok-para12-80.html' | relative_url }})、[A04 B01｜2008-2019]({{ '/results/a04-b01-08-19.html' | relative_url }})、[A04 B01｜2020-2025]({{ '/results/a04-b01-20-25.html' | relative_url }})。
