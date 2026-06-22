(() => {
  const selector = '.table-scroll, .experiment-map-scroll, .result-figure-scroller, .stopword-line';

  function headingFor(element) {
    const tableHeaders = [...element.querySelectorAll('thead th')]
      .slice(0, 3)
      .map((header) => header.textContent.trim())
      .filter(Boolean);
    if (tableHeaders.length) return tableHeaders.join('、');

    const caption = element.querySelector('figcaption');
    if (caption?.textContent.trim()) return caption.textContent.trim();

    let previous = element.previousElementSibling;
    while (previous) {
      if (previous.matches('h2, h3, h4, summary')) return previous.textContent.trim();
      previous = previous.previousElementSibling;
    }
    return '可捲動內容';
  }

  function makeScrollableRegionsFocusable() {
    document.querySelectorAll(selector).forEach((element) => {
      const canScroll = element.scrollWidth > element.clientWidth + 1
        || element.scrollHeight > element.clientHeight + 1;
      if (!canScroll || element.dataset.scrollA11yReady) return;

      element.dataset.scrollA11yReady = 'true';
      element.tabIndex = 0;
      element.setAttribute('role', 'group');
      if (!element.hasAttribute('aria-label') && !element.hasAttribute('aria-labelledby')) {
        element.setAttribute('aria-label', `${headingFor(element)}，可使用方向鍵捲動`);
      }
      element.addEventListener('keydown', (event) => {
        const step = Math.max(80, Math.round(element.clientWidth * 0.65));
        if (event.key === 'ArrowRight') {
          event.preventDefault();
          element.scrollBy({ left: step, behavior: 'smooth' });
        } else if (event.key === 'ArrowLeft') {
          event.preventDefault();
          element.scrollBy({ left: -step, behavior: 'smooth' });
        } else if (event.key === 'Home') {
          event.preventDefault();
          element.scrollTo({ left: 0, behavior: 'smooth' });
        } else if (event.key === 'End') {
          event.preventDefault();
          element.scrollTo({ left: element.scrollWidth, behavior: 'smooth' });
        }
      });
    });
  }

  requestAnimationFrame(makeScrollableRegionsFocusable);
  window.addEventListener('resize', makeScrollableRegionsFocusable);
  document.addEventListener('toggle', () => requestAnimationFrame(makeScrollableRegionsFocusable), true);
})();
