(function () {
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

  function textBlock(file, text, side) {
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
        <pre>${escapeHtml(text || "")}</pre>
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
      els.compareOutput.innerHTML = `
        ${textBlock(row.left, leftText, state.left.label)}
        ${textBlock(row.right, rightText, state.right.label)}
      `;
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
    els.summary = $("dataset-summary");
    els.fileList = $("dataset-file-list");
    els.fileCount = $("dataset-file-count");
    els.compareOutput = $("dataset-compare-output");

    if (!els.leftSelect) return;

    const response = await fetch(normalizeBase("assets/datasets/manifest.json"));
    state.manifest = await response.json();
    renderDatasetOptions();
    refreshComparison();

    els.leftSelect.addEventListener("change", refreshComparison);
    els.rightSelect.addEventListener("change", refreshComparison);
    els.search.addEventListener("input", renderFileList);
    els.statusFilter.addEventListener("change", renderFileList);
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
