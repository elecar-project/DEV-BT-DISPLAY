(function () {
  const ASSET_VERSION = "20260618-full-datasets";

  const state = {
    manifest: null,
    left: null,
    right: null,
    rows: [],
    selectedKey: null,
  };

  const els = {};

  function $(id) {
    return document.getElementById(id);
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function normalizeBase(path) {
    const base = document.querySelector("meta[name='site-baseurl']")?.content || "";
    return `${base.replace(/\/$/, "")}/${path.replace(/^\//, "")}`;
  }

  function fileMap(dataset) {
    const map = new Map();
    dataset.files.forEach((file) => {
      if (!map.has(file.key)) map.set(file.key, file);
    });
    return map;
  }

  function statusLabel(row) {
    if (row.left && row.right && row.left.sha1 === row.right.sha1) return "兩邊相同";
    if (row.left && row.right) return "兩邊都有，內容不同";
    if (row.left) return "只在左側";
    return "只在右側";
  }

  function statusClass(row) {
    if (row.left && row.right && row.left.sha1 === row.right.sha1) return "same";
    if (row.left && row.right) return "different";
    return "missing";
  }

  function getDataset(id) {
    return state.manifest.datasets.find((dataset) => dataset.id === id);
  }

  function buildRows() {
    const leftMap = fileMap(state.left);
    const rightMap = fileMap(state.right);
    const keys = Array.from(new Set([...leftMap.keys(), ...rightMap.keys()])).sort();
    state.rows = keys.map((key) => {
      const left = leftMap.get(key) || null;
      const right = rightMap.get(key) || null;
      return {
        key,
        left,
        right,
        displayName: left?.name || right?.name || key,
      };
    });
  }

  function renderDatasetOptions() {
    state.manifest.datasets.forEach((dataset) => {
      [els.leftSelect, els.rightSelect].forEach((select) => {
        const option = document.createElement("option");
        option.value = dataset.id;
        option.textContent = `${dataset.label} (${dataset.count})`;
        select.appendChild(option);
      });
    });
    els.leftSelect.value = state.manifest.datasets[0].id;
    els.rightSelect.value = state.manifest.datasets[1]?.id || state.manifest.datasets[0].id;
  }

  function renderSummary() {
    const same = state.rows.filter((row) => row.left && row.right && row.left.sha1 === row.right.sha1).length;
    const different = state.rows.filter((row) => row.left && row.right && row.left.sha1 !== row.right.sha1).length;
    const onlyLeft = state.rows.filter((row) => row.left && !row.right).length;
    const onlyRight = state.rows.filter((row) => !row.left && row.right).length;

    els.summary.innerHTML = `
      <div class="compare-stat"><strong>${state.rows.length}</strong><span>檔案鍵總數</span></div>
      <div class="compare-stat"><strong>${same}</strong><span>兩邊相同</span></div>
      <div class="compare-stat"><strong>${different}</strong><span>兩邊都有但不同</span></div>
      <div class="compare-stat"><strong>${onlyLeft + onlyRight}</strong><span>單側缺少</span></div>
    `;
  }

  function filteredRows() {
    const query = els.search.value.trim().toLowerCase();
    const filter = els.statusFilter.value;
    return state.rows.filter((row) => {
      const status = statusClass(row);
      const matchesFilter = filter === "all" || status === filter;
      const matchesQuery =
        !query ||
        row.displayName.toLowerCase().includes(query) ||
        row.key.toLowerCase().includes(query);
      return matchesFilter && matchesQuery;
    });
  }

  function renderFileList() {
    const rows = filteredRows();
    els.fileList.innerHTML = rows
      .map((row) => {
        const active = row.key === state.selectedKey ? " active" : "";
        return `
          <button class="file-row${active}" data-key="${escapeHtml(row.key)}">
            <span>
              <strong>${escapeHtml(row.displayName)}</strong>
              <small>${escapeHtml(row.key)}</small>
            </span>
            <em class="${statusClass(row)}">${statusLabel(row)}</em>
          </button>
        `;
      })
      .join("");
    els.fileCount.textContent = `顯示 ${rows.length} / ${state.rows.length} 筆`;
  }

  async function loadText(file) {
    if (!file) return null;
    const response = await fetch(normalizeBase(file.url));
    if (!response.ok) throw new Error(`無法載入 ${file.name}`);
    return response.text();
  }

  function isPunctuation(value) {
    return /^[^\p{L}\p{N}\s]+$/u.test(value);
  }

  function normalizeToken(value) {
    let token = value.normalize("NFKC");
    if (els.ignorePunctuation.checked && isPunctuation(token)) return "";
    if (els.ignoreCase.checked) token = token.toLocaleLowerCase();
    return token;
  }

  function tokenize(text) {
    const matches = String(text || "").match(/[\p{L}\p{N}]+(?:[’'\-][\p{L}\p{N}]+)*|[^\p{L}\p{N}\s]/gu) || [];
    return matches
      .map((raw) => ({ text: raw, norm: normalizeToken(raw) }))
      .filter((token) => token.norm);
  }

  function smartJoin(tokens) {
    const noSpaceBefore = new Set([",", ".", "!", "?", ";", ":", "%", ")", "]", "}", "”", "’"]);
    const noSpaceAfter = new Set(["(", "[", "{", "“", "‘"]);
    return tokens.reduce((output, token) => {
      const value = typeof token === "string" ? token : token.text;
      if (!output) return value;
      const last = output[output.length - 1];
      if (noSpaceBefore.has(value) || noSpaceAfter.has(last)) return output + value;
      return `${output} ${value}`;
    }, "");
  }

  function buildIndex(tokens) {
    const index = new Map();
    tokens.forEach((token, position) => {
      if (!index.has(token.norm)) index.set(token.norm, []);
      index.get(token.norm).push(position);
    });
    return index;
  }

  function findLongestMatch(a, b, alo, ahi, blo, bhi, bIndex) {
    let bestI = alo;
    let bestJ = blo;
    let bestSize = 0;
    let previous = new Map();
    for (let i = alo; i < ahi; i += 1) {
      const current = new Map();
      const positions = bIndex.get(a[i].norm) || [];
      positions.forEach((j) => {
        if (j < blo || j >= bhi) return;
        const k = (previous.get(j - 1) || 0) + 1;
        current.set(j, k);
        if (k > bestSize) {
          bestI = i - k + 1;
          bestJ = j - k + 1;
          bestSize = k;
        }
      });
      previous = current;
    }
    return { i: bestI, j: bestJ, size: bestSize };
  }

  function matchingBlocks(a, b) {
    const bIndex = buildIndex(b);
    const queue = [[0, a.length, 0, b.length]];
    const blocks = [];
    while (queue.length) {
      const [alo, ahi, blo, bhi] = queue.pop();
      const match = findLongestMatch(a, b, alo, ahi, blo, bhi, bIndex);
      if (!match.size) continue;
      blocks.push(match);
      if (alo < match.i && blo < match.j) queue.push([alo, match.i, blo, match.j]);
      if (match.i + match.size < ahi && match.j + match.size < bhi) {
        queue.push([match.i + match.size, ahi, match.j + match.size, bhi]);
      }
    }
    blocks.sort((left, right) => left.i - right.i || left.j - right.j);
    blocks.push({ i: a.length, j: b.length, size: 0 });
    return blocks;
  }

  function opcodes(a, b) {
    let i = 0;
    let j = 0;
    const ops = [];
    matchingBlocks(a, b).forEach((block) => {
      let tag = "";
      if (i < block.i && j < block.j) tag = "replace";
      else if (i < block.i) tag = "delete";
      else if (j < block.j) tag = "insert";
      if (tag) ops.push([tag, i, block.i, j, block.j]);
      if (block.size) ops.push(["equal", block.i, block.i + block.size, block.j, block.j + block.size]);
      i = block.i + block.size;
      j = block.j + block.size;
    });
    return ops;
  }

  function chunkTokens(left, right, maxTokens) {
    const maxLength = Math.max(left.length, right.length, 1);
    const chunks = [];
    for (let start = 0; start < maxLength; start += maxTokens) {
      chunks.push([left.slice(start, start + maxTokens), right.slice(start, start + maxTokens)]);
    }
    return chunks;
  }

  function buildDiffRows(aTokens, bTokens) {
    const rows = [];
    opcodes(aTokens, bTokens).forEach(([kind, i1, i2, j1, j2]) => {
      const left = aTokens.slice(i1, i2);
      const right = bTokens.slice(j1, j2);
      chunkTokens(left, right, 80).forEach(([leftChunk, rightChunk]) => {
        rows.push({
          kind,
          aText: smartJoin(leftChunk),
          bText: smartJoin(rightChunk),
          aCount: leftChunk.length,
          bCount: rightChunk.length,
        });
      });
    });
    return rows;
  }

  function compactRows(rows, contextTokens) {
    const compact = [];
    let pending = null;
    function flush(before) {
      if (!pending) return;
      const left = pending.aText.split(/\s+/).filter(Boolean);
      const right = pending.bText.split(/\s+/).filter(Boolean);
      compact.push({
        kind: "context",
        aText: smartJoin(before ? left.slice(-contextTokens) : left.slice(0, contextTokens)),
        bText: smartJoin(before ? right.slice(-contextTokens) : right.slice(0, contextTokens)),
        aCount: Math.min(left.length, contextTokens),
        bCount: Math.min(right.length, contextTokens),
      });
      pending = null;
    }
    rows.forEach((row) => {
      if (row.kind === "equal") {
        pending = row;
        return;
      }
      flush(true);
      compact.push(row);
    });
    flush(false);
    return compact;
  }

  function statsFromRows(rows, aTokens, bTokens) {
    const equal = rows.filter((row) => row.kind === "equal").reduce((sum, row) => sum + row.aCount, 0);
    const insert = rows.filter((row) => row.kind === "insert").reduce((sum, row) => sum + row.bCount, 0);
    const del = rows.filter((row) => row.kind === "delete").reduce((sum, row) => sum + row.aCount, 0);
    const replaceA = rows.filter((row) => row.kind === "replace").reduce((sum, row) => sum + row.aCount, 0);
    const replaceB = rows.filter((row) => row.kind === "replace").reduce((sum, row) => sum + row.bCount, 0);
    const denominator = Math.max(aTokens.length, bTokens.length, 1);
    const changed = insert + del + Math.max(replaceA, replaceB);
    return {
      aTokens: aTokens.length,
      bTokens: bTokens.length,
      equal,
      insert,
      delete: del,
      replaceA,
      replaceB,
      similarity: equal / denominator,
      changeRate: changed / denominator,
    };
  }

  function classifyLabel(kind) {
    return {
      equal: "相同",
      context: "前後文",
      delete: "A 有、B 沒有",
      insert: "B 有、A 沒有",
      replace: "替換/不一致",
    }[kind] || kind;
  }

  function inlineSpan(text, className) {
    if (!text) return "";
    const cls = className ? ` class="mark ${className}"` : "";
    return `<span${cls}>${escapeHtml(text)}</span> `;
  }

  function inlineColumn(rows, side) {
    return rows
      .map((row) => {
        const text = side === "a" ? row.aText : row.bText;
        if (row.kind === "equal") return inlineSpan(text, "");
        if (row.kind === "context") return `<span class="diff-gap">...</span>${inlineSpan(text, "mark-context")}`;
        if (row.kind === "delete" && side === "a") return inlineSpan(text, "mark-delete");
        if (row.kind === "insert" && side === "b") return inlineSpan(text, "mark-insert");
        if (row.kind === "replace" && side === "a") return inlineSpan(text, "mark-replace-a");
        if (row.kind === "replace" && side === "b") return inlineSpan(text, "mark-replace-b");
        return "";
      })
      .join("");
  }

  function splitRows(rows, paragraphTokens) {
    const paragraphs = [];
    let current = [];
    let count = 0;
    rows.forEach((row) => {
      current.push(row);
      count += Math.max(row.aCount, row.bCount, 1);
      const text = (row.aText || row.bText || "").trim();
      const canBreak = row.kind === "equal" || row.kind === "context" || /[.!?。？！]$/.test(text);
      if (count >= paragraphTokens && canBreak) {
        paragraphs.push(current);
        current = [];
        count = 0;
      }
    });
    if (current.length) paragraphs.push(current);
    return paragraphs;
  }

  function diffReport(row, leftText, rightText) {
    const aTokens = tokenize(leftText);
    const bTokens = tokenize(rightText);
    const rows = buildDiffRows(aTokens, bTokens);
    const shownRows = els.previewMode.value === "diff" ? compactRows(rows, 18) : rows;
    const stats = statsFromRows(rows, aTokens, bTokens);
    const paragraphs = splitRows(shownRows, 140)
      .map((paragraph, index) => `
        <section class="diff-paragraph">
          <div class="paragraph-label">段落 ${index + 1}</div>
          <div class="diff-columns">
            <div class="diff-text">${inlineColumn(paragraph, "a")}</div>
            <div class="diff-text">${inlineColumn(paragraph, "b")}</div>
          </div>
        </section>
      `)
      .join("");

    const tableRows = shownRows
      .filter((item) => els.previewMode.value === "full" || item.kind !== "equal")
      .map((item) => `
        <tr class="${item.kind}">
          <td>${classifyLabel(item.kind)}</td>
          <td>${escapeHtml(item.aText)}</td>
          <td>${escapeHtml(item.bText)}</td>
        </tr>
      `)
      .join("");

    return `
      <section class="diff-report">
        <div class="diff-source-grid">
          ${sourceCard(row.left, state.left.label)}
          ${sourceCard(row.right, state.right.label)}
        </div>
        <div class="diff-metrics">
          <div class="compare-stat"><strong>${stats.aTokens.toLocaleString()}</strong><span>A tokens</span></div>
          <div class="compare-stat"><strong>${stats.bTokens.toLocaleString()}</strong><span>B tokens</span></div>
          <div class="compare-stat"><strong>${(stats.similarity * 100).toFixed(2)}%</strong><span>Similarity</span></div>
          <div class="compare-stat"><strong>${(stats.changeRate * 100).toFixed(2)}%</strong><span>Change rate</span></div>
          <div class="compare-stat"><strong>${stats.insert.toLocaleString()} / ${stats.delete.toLocaleString()}</strong><span>Insert / Delete</span></div>
          <div class="compare-stat"><strong>${stats.replaceA.toLocaleString()} / ${stats.replaceB.toLocaleString()}</strong><span>Replace A/B</span></div>
        </div>
        <div class="diff-legend">
          <span class="mark mark-delete">A 有、B 沒有</span>
          <span class="mark mark-insert">B 有、A 沒有</span>
          <span class="mark mark-replace-a">A 替換前</span>
          <span class="mark mark-replace-b">B 替換後</span>
        </div>
        <div class="diff-header">
          <div>A | ${escapeHtml(state.left.label)}</div>
          <div>B | ${escapeHtml(state.right.label)}</div>
        </div>
        ${paragraphs}
        <details class="diff-table-wrap">
          <summary>差異摘要表</summary>
          <table class="diff-table">
            <thead><tr><th>類型</th><th>A</th><th>B</th></tr></thead>
            <tbody>${tableRows}</tbody>
          </table>
        </details>
      </section>
    `;
  }

  function sourceCard(file, side) {
    if (!file) {
      return `
        <section class="compare-pane is-missing">
          <h3>${side}</h3>
          <p>此資料集中沒有這個檔案。</p>
        </section>
      `;
    }
    return `
      <section class="compare-pane">
        <h3>${side}</h3>
        <dl>
          <dt>檔名</dt><dd>${escapeHtml(file.name)}</dd>
          <dt>字元</dt><dd>${file.chars.toLocaleString()}</dd>
          <dt>來源</dt><dd><code>${escapeHtml(file.source_path)}</code></dd>
        </dl>
      </section>
    `;
  }

  async function selectFile(key) {
    state.selectedKey = key;
    renderFileList();
    const row = state.rows.find((item) => item.key === key);
    if (!row) return;
    els.compareOutput.innerHTML = "<p class=\"loading-text\">載入文字內容中...</p>";
    try {
      const [leftText, rightText] = await Promise.all([loadText(row.left), loadText(row.right)]);
      if (!row.left || !row.right) {
        els.compareOutput.innerHTML = `${sourceCard(row.left, state.left.label)}${sourceCard(row.right, state.right.label)}`;
        return;
      }
      els.compareOutput.innerHTML = diffReport(row, leftText, rightText);
    } catch (error) {
      els.compareOutput.innerHTML = `<p class="error-text">${escapeHtml(error.message)}</p>`;
    }
  }

  function refreshComparison() {
    state.left = getDataset(els.leftSelect.value);
    state.right = getDataset(els.rightSelect.value);
    state.selectedKey = null;
    buildRows();
    renderSummary();
    renderFileList();
    els.compareOutput.innerHTML = "<p class=\"loading-text\">請從上方清單選擇一個檔案進行左右對比。</p>";
  }

  async function init() {
    els.leftSelect = $("dataset-left");
    els.rightSelect = $("dataset-right");
    els.search = $("dataset-search");
    els.statusFilter = $("dataset-status");
    els.previewMode = $("dataset-preview");
    els.ignoreCase = $("dataset-ignore-case");
    els.ignorePunctuation = $("dataset-ignore-punctuation");
    els.summary = $("dataset-summary");
    els.fileList = $("dataset-file-list");
    els.fileCount = $("dataset-file-count");
    els.compareOutput = $("dataset-compare-output");

    if (!els.leftSelect) return;

    const response = await fetch(normalizeBase(`assets/datasets/manifest.json?v=${ASSET_VERSION}`));
    state.manifest = await response.json();
    renderDatasetOptions();
    refreshComparison();

    els.leftSelect.addEventListener("change", refreshComparison);
    els.rightSelect.addEventListener("change", refreshComparison);
    els.search.addEventListener("input", renderFileList);
    els.statusFilter.addEventListener("change", renderFileList);
    els.previewMode.addEventListener("change", () => {
      if (state.selectedKey) selectFile(state.selectedKey);
    });
    els.ignoreCase.addEventListener("change", () => {
      if (state.selectedKey) selectFile(state.selectedKey);
    });
    els.ignorePunctuation.addEventListener("change", () => {
      if (state.selectedKey) selectFile(state.selectedKey);
    });
    els.fileList.addEventListener("click", (event) => {
      const button = event.target.closest("[data-key]");
      if (button) selectFile(button.dataset.key);
    });
  }

  init().catch((error) => {
    const output = $("dataset-compare-output");
    if (output) output.innerHTML = `<p class="error-text">${escapeHtml(error.message)}</p>`;
  });
})();
