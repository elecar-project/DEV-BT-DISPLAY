#!/usr/bin/env python3
"""Publish A05 stopword curation histories as GitHub Pages views."""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path


SOURCE = Path("/workspaces/Dev-BT/#運行BERTopic整理/#5. 停用詞")
ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs/results"
ASSETS = ROOT / "docs/assets/results"
EV_ANCHORS = "electric、EV、charging、battery、range、motor、torque、hybrid、plug"
OBSOLETE_SLUGS = (
    "a05-8-repl-stopwords",
    "a05-8-repl-1-stopwords",
    "a05-8-repl-2-stopwords",
    "a05-8-repl-3-stopwords",
)

TRACKS = [
    ("a05-6", "A05-6｜初步停用詞迭代", "repl + tok + 段落 12-80", "從一般車輛與逐字稿雜訊出發，逐輪壓低非 EV 核心的產品展示、車機、賽道與銷售語境。", [
        ("a05-6-stopwords", "A05-6", "A05-6(repl)_tok(para12-80)/A05-6_stopword.md", "基礎詞表", "建立 EV 核心詞保留與一般雜訊移除原則。"),
        ("a05-6-1-stopwords", "A05-6.1", "A05-6(repl)_tok(para12-80)/A05-6.1_stopword.md", "第一次增補", "加入車機、展演與非 EV 性能殘留詞。"),
        ("a05-6-2-stopwords", "A05-6.2", "A05-6(repl)_tok(para12-80)/A05-6.2_stopword.md", "第二次增補", "處理連線服務、銷售金融與賽道性能語境。"),
        ("a05-6-3-stopwords", "A05-6.3", "A05-6(repl)_tok(para12-80)/A05-6.3_stopword.md", "積極版本", "進一步移除舒適、設計、維修與聲學等非核心語境。"),
    ]),
    ("a05-8-orig-rev", "A05-8｜orig REV 詞表收斂", "orig REV + tok + 段落 12-80", "處理原始語料中重新出現的品牌、車款、年份與影片敘事殘留，最後分為完整彙整與人工精選兩版。", [
        ("a05-8-orig-rev-stopwords", "A05-8 REV", "A05-8(orig)REV_tok(para12-80)/A05-8_stopword.md", "基礎詞表", "以 A05-8 原則重新套用於 orig REV 語料。"),
        ("a05-8-orig-rev-1-stopwords", "A05-8.1 REV", "A05-8(orig)REV_tok(para12-80)/A05-8.1-REV_stopword.md", "第一次增補", "補入品牌車款、流程詞與外觀、車機、ADAS 殘留。"),
        ("a05-8-orig-rev-2-stopwords", "A05-8.2 REV", "A05-8(orig)REV_tok(para12-80)/A05-8.2-REV_stopword.md", "第二次增補", "補入駕乘、便利配備與市場展示殘留。"),
        ("a05-8-orig-rev-3-stopwords", "A05-8.3 REV", "A05-8(orig)REV_tok(para12-80)/A05-8.3-REV_stopword.md", "第三次增補", "僅依 default topic words 補入低解釋力殘留。"),
        ("a05-8-orig-rev-all-stopwords", "A05-8.4 all", "A05-8(orig)REV_tok(para12-80)/A05-8.4(all)_stopword.md", "完整彙整", "彙整各輪建議，保留完整的 36 類參考。"),
        ("a05-8-orig-rev-human-stopwords", "A05-8.4 human", "A05-8(orig)REV_tok(para12-80)/A05-8.4(human)_stopword.md", "人工精選", "人工收斂為較易維護的 12 類建議版。"),
    ]),
]


def clean(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    return html.escape(value.strip())


def table_sections(text: str) -> list[tuple[str, list[list[str]]]]:
    heading = "詞表分類"
    sections: list[tuple[str, list[list[str]]]] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        if lines[index].startswith(("## ", "### ")):
            heading = lines[index].lstrip("# ").strip()
        if not lines[index].startswith("|"):
            index += 1
            continue
        table: list[list[str]] = []
        while index < len(lines) and lines[index].startswith("|"):
            cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
            if not all(re.fullmatch(r"[: -]+", cell) for cell in cells):
                table.append(cells)
            index += 1
        if len(table) > 1 and any("停用詞" in cell or "類型" in cell for cell in table[0]):
            sections.append((heading, table))
    return sections


def first_paragraph(text: str) -> str:
    for item in re.split(r"\n\s*\n", text):
        value = item.strip()
        if value and not value.startswith(("#", "-", "|", "```", "custom_stopwords")):
            return re.sub(r"`([^`]+)`", r"\1", value.replace("\n", " "))
    return "本版本依 BERTopic representation 的殘留詞調整客製停用詞。"


def sections_html(sections: list[tuple[str, list[list[str]]]]) -> str:
    blocks = []
    for title, table in sections:
        header = "".join(f"<th>{clean(cell)}</th>" for cell in table[0])
        rows = "".join("<tr>" + "".join(f"<td>{clean(cell)}</td>" for cell in row) + "</tr>" for row in table[1:])
        blocks.append(f'<h3>{html.escape(title)}</h3><div class="table-scroll"><table class="stopword-table"><thead><tr>{header}</tr></thead><tbody>{rows}</tbody></table></div>')
    return "".join(blocks) or '<p class="result-empty">原始檔未包含可辨識的停用詞分類表。</p>'


def write_detail(track: tuple, version: tuple) -> None:
    track_id, track_title, dataset, _, _ = track
    slug, label, relative, stage, summary = version
    source = SOURCE / relative
    text = source.read_text(encoding="utf-8")
    sections = table_sections(text)
    categories = sum(len(table) - 1 for _, table in sections)
    asset_dir = ASSETS / slug
    asset_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, asset_dir / source.name)
    files = [(source.name, "原始停用詞建議與完整 CountVectorizer 清單")]
    if label == "A05-8.4 human":
        docx = source.with_suffix(".docx")
        if docx.is_file():
            shutil.copy2(docx, asset_dir / docx.name)
            files.append((docx.name, "人工審閱用 Word 版本"))
    downloads = "".join(f'<tr><td><a href="{{{{ \'/assets/results/{slug}/{name}\' | relative_url }}}}">{html.escape(name)}</a></td><td>{purpose}</td></tr>' for name, purpose in files)
    page = f'''---
title: {label} 停用詞設計
description: {track_title} 的 {label} 停用詞設計紀錄。
---

# {label}｜停用詞設計

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 版本設定

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>版本線</td><td>{html.escape(track_title)}</td></tr>
<tr><td>資料版本</td><td>{html.escape(dataset)}</td></tr>
<tr><td>版本定位</td><td>{html.escape(stage)}</td></tr>
<tr><td>分類筆數</td><td>{categories} 類</td></tr>
</tbody></table>

### 核心原則

<p>保留 EV 語意錨點：<code>{EV_ANCHORS}</code>。</p>

### 導覽

<p><a href="{{{{ '/results/a05-stopwords-overview.html' | relative_url }}}}">回到 A05 停用詞總覽</a></p>
</aside>

<section markdown="1">
## 本版目的

{html.escape(summary)}

<p class="section-intro">{html.escape(first_paragraph(text))}</p>

## 停用詞分類與理由

{sections_html(sections)}

## 使用原則

<aside class="table-note">此詞表用於降低逐字稿、產品展示與一般車評語境對主題表示的干擾；加入前應依研究問題確認是否仍需要保留智慧座艙、ADAS、設計、銷售或 NVH 等主題。完整單字清單保留在原始輸出檔。</aside>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody>{downloads}</tbody></table>
</section>
</div>
'''
    (PAGES / f"{slug}.md").write_text(page, encoding="utf-8")
    print(f"Published {label}")


def track_html(track: tuple) -> str:
    track_id, title, _, description, versions = track
    steps = []
    for slug, label, _, stage, summary in versions:
        final = " is-final" if label.endswith("human") else ""
        steps.append(f'<a class="stopword-step{final}" href="{{{{ \'/results/{slug}.html\' | relative_url }}}}"><strong>{html.escape(label)}</strong><span>{html.escape(stage)}</span><small>{html.escape(summary)}</small></a>')
    return f'<section class="stopword-track" aria-labelledby="{track_id}"><header><h2 id="{track_id}">{html.escape(title)}</h2><p>{html.escape(description)}</p></header><div class="stopword-line">{"".join(steps)}</div></section>'


def write_branch_overview(track: tuple) -> None:
    track_id, title, dataset, description, _ = track
    page = f'''---
title: {title}
description: {title} 的停用詞版本線。
---

# {title}

{description}

<aside class="table-note"><strong>資料版本：</strong><code>{dataset}</code>。每個節點均可查看停用詞分類、加入理由與原始檔。</aside>

{track_html(track)}

<p><a href="{{{{ '/results/a05-stopwords-overview.html' | relative_url }}}}">回到 A05 停用詞總覽</a></p>
'''
    (PAGES / f"{track_id}-overview.md").write_text(page, encoding="utf-8")


def run() -> None:
    for slug in OBSOLETE_SLUGS:
        (PAGES / f"{slug}.md").unlink(missing_ok=True)
        shutil.rmtree(ASSETS / slug, ignore_errors=True)
    for track in TRACKS:
        for version in track[4]:
            write_detail(track, version)
        write_branch_overview(track)
    overview = '''---
title: A05 停用詞設計
description: A05-6 與 A05-8 orig REV 的客製停用詞版本線。
---

# A05｜停用詞設計

A05 依 A06 BERTopic representation 的殘留詞反覆修訂客製停用詞。本站僅保留 A05-6 與 A05-8 orig REV 兩條正確資料分支；A05-8 repl 為錯誤運行產生的資料，不納入呈現。

<aside class="table-note"><strong>共同保留原則：</strong>不將 <code>electric</code>、<code>EV</code>、<code>charging</code>、<code>battery</code>、<code>range</code>、<code>motor</code>、<code>torque</code>、<code>hybrid</code>、<code>plug</code> 等 EV 語意錨點納入停用詞。</aside>

## 版本線

每個節點均可點入查看新增的停用詞分類、原因與原始檔。版本線依資料處理策略分開呈現，避免將不同語料的詞表混為同一份設定。

''' + "\n".join(track_html(track) for track in TRACKS) + '''

## 建議採用方式

<div class="card-grid">
<section class="section-card"><h3>探索與比較</h3><p>先從各分支的基礎版開始，逐輪對照 A06 的 topic words，確認雜訊是否持續降低。</p></section>
<section class="section-card"><h3>正式重跑</h3><p>依資料版本使用同一條版本線的累積詞表；A05-6 與 A05-8 orig REV 應分開使用。</p></section>
<section class="section-card"><h3>人工收斂</h3><p><a href="{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}">A05-8.4 human</a> 是目前人工精選的建議版；all 版則保留為完整參考。</p></section>
</div>

## 原始資料

所有完整 Markdown 詞表與 A05-8.4 human 的 Word 檔都保留於對應詳細頁的「原始輸出」區。
'''
    (PAGES / "a05-stopwords-overview.md").write_text(overview, encoding="utf-8")


if __name__ == "__main__":
    run()
