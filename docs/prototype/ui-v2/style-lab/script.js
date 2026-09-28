/* Switching visual tokens is the only Style Lab interaction. */
const picker = document.querySelector('.direction-picker');
const params = new URLSearchParams(location.search);
const initial = params.get('direction');
if (['a', 'b', 'c'].includes(initial)) {
  document.documentElement.dataset.direction = initial;
  picker.querySelector(`input[value="${initial}"]`).checked = true;
}
picker.addEventListener('change', (event) => {
  if (event.target.name !== 'direction') return;
  const direction = event.target.value;
  document.documentElement.dataset.direction = direction;
  const url = new URL(location.href);
  url.searchParams.set('direction', direction);
  history.replaceState(null, '', url);
});
document.querySelector('.filter-grid').addEventListener('submit', (event) => event.preventDefault());
