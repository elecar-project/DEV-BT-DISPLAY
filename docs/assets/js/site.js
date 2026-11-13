/* Shared progressive enhancements. Content and navigation work without JavaScript. */
(() => {
  const header = document.querySelector('.site-header');
  const nav = document.querySelector('.site-nav');
  const toggle = document.querySelector('.nav-toggle');
  const mobile = window.matchMedia('(max-width: 760px)');
  if (header && nav && toggle) {
    toggle.hidden = false;
    const close = () => {
      toggle.setAttribute('aria-expanded', 'false');
      toggle.innerHTML = '開啟導覽 <span aria-hidden="true">☰</span>';
      nav.hidden = mobile.matches;
    };
    close();
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      toggle.innerHTML = open ? '關閉導覽 <span aria-hidden="true">×</span>' : '開啟導覽 <span aria-hidden="true">☰</span>';
      nav.hidden = !open;
    });
    mobile.addEventListener('change', close);
    nav.addEventListener('click', (event) => { if (event.target.closest('a')) close(); });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && mobile.matches && !nav.hidden) { close(); toggle.focus(); }
    });
    new ResizeObserver(() => document.documentElement.style.setProperty('--header-height', `${header.offsetHeight}px`)).observe(header);
  }

  const compactSettings = window.matchMedia('(max-width: 900px)');
  document.querySelectorAll('.result-settings, .results-sidebar').forEach((aside) => {
    const disclosure = document.createElement('details');
    disclosure.className = 'settings-disclosure';
    const summary = document.createElement('summary');
    summary.textContent = aside.classList.contains('result-settings') ? '實驗設定與來源' : '相關結果導覽';
    aside.before(disclosure);
    disclosure.append(summary, aside);
    const adapt = () => { disclosure.open = !compactSettings.matches; };
    adapt();
    compactSettings.addEventListener('change', adapt);
  });

  function prepareTables() {
    document.querySelectorAll('main table').forEach((table) => {
      table.querySelectorAll('thead th').forEach((cell) => cell.setAttribute('scope', 'col'));
      if (table.closest('.result-settings') || table.closest('.table-scroll')) return;
      const wrapper = document.createElement('div');
      wrapper.className = 'table-scroll';
      table.before(wrapper);
      wrapper.append(table);
    });
    document.querySelectorAll('main .table-scroll').forEach((wrapper) => {
      const heading = wrapper.closest('section')?.querySelector('h2') || wrapper.previousElementSibling;
      wrapper.setAttribute('role', 'region');
      wrapper.setAttribute('aria-label', `${heading?.textContent?.trim()?.slice(0, 60) || '資料'}表格，可左右捲動`);
      const overflowing = wrapper.scrollWidth > wrapper.clientWidth + 2;
      wrapper.dataset.overflow = String(overflowing);
      wrapper.tabIndex = overflowing ? 0 : -1;
    });
    document.querySelectorAll('.result-figure-scroller').forEach((scroller) => {
      scroller.setAttribute('role', 'region');
      scroller.setAttribute('aria-label', '實驗圖表，可使用方向鍵或觸控左右捲動');
      scroller.tabIndex = scroller.scrollWidth > scroller.clientWidth + 2 ? 0 : -1;
    });
  }
  prepareTables();
  window.addEventListener('resize', prepareTables);
  document.addEventListener('toggle', prepareTables, true);
  // The dataset comparer inserts its tables after asynchronous text requests.
  const compareOutput = document.querySelector('#dataset-compare-output');
  if (compareOutput) new MutationObserver(prepareTables).observe(compareOutput, {childList: true});

  const title = document.querySelector('main > h1');
  const headings = [...document.querySelectorAll('main h2')].filter((heading) => !heading.closest('aside'));
  if (title && headings.length > 2) {
    const outline = document.createElement('details');
    outline.className = 'page-outline';
    const summary = document.createElement('summary');
    summary.textContent = '本頁目錄';
    outline.append(summary);
    const links = document.createElement('nav');
    links.setAttribute('aria-label', '本頁段落');
    headings.forEach((heading, index) => {
      if (!heading.id) heading.id = `section-${index + 1}`;
      const link = document.createElement('a');
      link.href = `#${heading.id}`;
      link.textContent = heading.textContent;
      links.append(link);
    });
    outline.append(links);
    title.after(outline);
  }

  const catalog = document.querySelector('[data-result-catalog]');
  const search = document.querySelector('#result-search');
  if (catalog && search) {
    const groups = [...catalog.querySelectorAll('[data-result-group]')];
    const rows = [...catalog.querySelectorAll('[data-result-item]')];
    search.addEventListener('input', () => {
      const query = search.value.trim().toLocaleLowerCase();
      let count = 0;
      rows.forEach((row) => {
        row.hidden = !row.textContent.toLocaleLowerCase().includes(query);
        if (!row.hidden) count += 1;
      });
      groups.forEach((group) => { group.hidden = ![...group.querySelectorAll('[data-result-item]')].some((row) => !row.hidden); });
      document.querySelector('#result-search-count').textContent = `顯示 ${count} / ${rows.length} 頁`;
      document.querySelector('#result-search-empty').hidden = count > 0;
    });
  }

  const map = document.querySelector('.experiment-map-full');
  if (map) {
    const viewport = map.closest('.experiment-map-scroll');
    const zoom = document.querySelector('#map-zoom');
    document.querySelector('#map-fit')?.addEventListener('click', () => {
      viewport.classList.add('map-fitted');
      map.style.width = '';
      if (zoom) zoom.value = 'fit';
    });
    zoom?.addEventListener('change', () => {
      viewport.classList.toggle('map-fitted', zoom.value === 'fit');
      map.style.width = zoom.value === 'fit' ? '' : `${Number(zoom.value)}px`;
    });
  }
})();
