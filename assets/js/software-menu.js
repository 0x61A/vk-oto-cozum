// Use the site's existing mobile navigation without changing its links.
(() => {
  const button = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');
  if (!button || !menu) return;

  button.setAttribute('aria-controls', menu.id);
  button.setAttribute('aria-expanded', 'false');
  const setOpen = (open) => {
    menu.classList.toggle('hidden', !open);
    button.setAttribute('aria-expanded', String(open));
  };

  button.addEventListener('click', () => setOpen(menu.classList.contains('hidden')));
  menu.addEventListener('click', (event) => {
    if (event.target.closest('a')) setOpen(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !menu.classList.contains('hidden')) {
      setOpen(false);
      button.focus();
    }
  });
})();
