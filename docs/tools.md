---
title: 工具
description: Release 檔案、工作流程分組與流程圖展示。
---

# 工具

本頁保留 DEV-BT 研究流程中最常用的工具入口與流程概覽。

## Release 檔案

可下載工具目前發布在母倉庫的 Release：

<https://github.com/elecar-project/DEV-BT/releases>

## 工作流程分組

| 階段 | 對應工具 | 研究用途 |
| --- | --- | --- |
| A. 音檔與 ASR 處理 | Audio V2A、Audio-tran、ASR-result、ASR-analysis、TXT Compare、TXT Delete | 取得逐字稿、檢查 ASR 品質、整理可用文本 |
| B. 資料清理與切分 | LLM Clean、TXTcp-2、TXT Filter、TXT Tokenizer、Pre-process Workbench | 清理逐字稿、建立資料集版本、切成 BERTopic 可用句子 |
| C. BERTopic 處理 | BERTopic Workbench、BERTopic Deploy、Min & Elbow、Batch | 訓練 topic model、調整參數、匯出主題結果 |

## 流程圖展示

<div class="figure-gallery">
  <figure>
    <img src="{{ '/assets/img/115.06.05_資料蒐集架構圖（詳細）_ver.3.drawio.png' | relative_url }}" alt="資料蒐集架構圖">
    <figcaption>
      <strong>圖 1｜資料蒐集架構圖（詳細）ver.3</strong>
      <span>資料來源、篩選、轉錄與前處理流程</span>
    </figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/img/115.06.05_BERTopic流程_ver.4_新增(產業與管理論壇).drawio.png' | relative_url }}" alt="BERTopic流程">
    <figcaption>
      <strong>圖 2｜BERTopic 主題建模流程</strong>
      <span>語意向量化、降維、分群、權重計算與主題命名</span>
    </figcaption>
  </figure>
</div>
