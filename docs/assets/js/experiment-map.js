(function () {
  const map = document.querySelector('.experiment-map');
  if (!map) return;

  const splitFlows = (value) => (value || '').split(' ').filter(Boolean);
  const getFlows = (element) => splitFlows(element.dataset.flowTarget);

  function clearFlow() {
    map.querySelectorAll('.is-flow-source, .is-flow-arrow, .is-flow-target').forEach((element) => {
      element.classList.remove('is-flow-source', 'is-flow-arrow', 'is-flow-target');
    });
  }

  function highlightFlow(target) {
    const flows = getFlows(target);
    if (!flows.length) return;
    clearFlow();

    map.querySelectorAll('[data-flow-node]').forEach((element) => {
      if (splitFlows(element.dataset.flowNode).some((flow) => flows.includes(flow))) {
        element.classList.add('is-flow-source');
      }
    });
    map.querySelectorAll('[data-flow-arrows]').forEach((element) => {
      if (splitFlows(element.dataset.flowArrows).some((flow) => flows.includes(flow))) {
        element.classList.add('is-flow-arrow');
      }
    });
    target.classList.add('is-flow-target');
  }

  map.querySelectorAll('[data-flow-target]').forEach((target) => {
    target.addEventListener('mouseenter', () => highlightFlow(target));
    target.addEventListener('focus', () => highlightFlow(target));
    target.addEventListener('mouseleave', clearFlow);
    target.addEventListener('blur', clearFlow);
  });
})();
