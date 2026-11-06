(() => {
  const filters = document.querySelector('#filters');
  const count = document.querySelector('#result-count');
  let selectedDate = 'all';
  let selectedDirection = 'all';
  filters.hidden = false;
  filters.addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (!button) return;
    if (button.dataset.date) selectedDate = button.dataset.date;
    if (button.dataset.direction) selectedDirection = button.dataset.direction;
    filters.querySelectorAll('[data-date]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.date === selectedDate)));
    filters.querySelectorAll('[data-direction]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.direction === selectedDirection)));
    let matches = 0;
    document.querySelectorAll('.day-group').forEach(group => {
      group.hidden = selectedDate !== 'all' && group.dataset.day !== selectedDate;
      group.querySelectorAll('[data-direction]').forEach(card => {
        card.hidden = selectedDirection !== 'all' && card.dataset.direction !== selectedDirection;
        if (!group.hidden && !card.hidden && card.dataset.match) matches++;
      });
      const table = group.querySelector('.table-wrap');
      table.hidden = !Array.from(group.querySelectorAll('[data-match]')).some(row => !row.hidden);
    });
    count.textContent = `${matches} départ${matches === 1 ? '' : 's'}`;
  });
})();
