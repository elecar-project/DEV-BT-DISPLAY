(() => {
  const tables = document.querySelectorAll('.page-shell > table, table[data-mobile-cards]');

  tables.forEach((table) => {
    const labels = [...table.querySelectorAll('thead th')].map((header) => header.textContent.trim());
    if (!labels.length) return;

    table.classList.add('mobile-card-table');
    table.querySelectorAll('tbody tr').forEach((row) => {
      [...row.children].forEach((cell, index) => {
        if (cell.tagName === 'TD') cell.dataset.label = labels[index] || '';
      });
    });
  });
})();
