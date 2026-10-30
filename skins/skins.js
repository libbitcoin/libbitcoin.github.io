(function () {
  'use strict';
  var SKINS = [['moon', 'Moon'], ['spec', 'Spec'], ['classic', 'Classic']];
  var DEFAULT = 'classic';
  var base = document.currentScript.src.replace(/[^\/]*$/, '');

  // A skin given in the query (?skin=name) is remembered and enables the
  // selector; ?skin=off forgets it.
  var skin = new URLSearchParams(location.search).get('skin');
  try {
    if (skin === 'off') localStorage.removeItem('skin');
    else if (skin === null) skin = localStorage.getItem('skin');
    else localStorage.setItem('skin', skin);
  } catch (_) {}
  var known = SKINS.some(function (s) { return s[0] === skin; });
  var selectable = known;
  if (!known) skin = DEFAULT;

  // A chosen skin other than the default is kept in the address so that a
  // copied link carries it.
  function mark(name) {
    try {
      var url = new URL(location.href);
      if (name && name !== DEFAULT) url.searchParams.set('skin', name);
      else url.searchParams.delete('skin');
      if (url.href !== location.href) history.replaceState(history.state, '', url.href);
    } catch (_) {}
  }
  mark(skin);

  document.write('<style>' +
    '.menu .skin { margin-left: auto; font: inherit; letter-spacing: inherit; ' +
    'text-transform: inherit; color: var(--ink-2); background: transparent; ' +
    'border: 1px solid var(--rule); border-radius: 3px; padding: 2px 6px; cursor: pointer; }' +
    '.menu .skin:hover, .menu .skin:focus { color: var(--heading); }' +
    '.menu .skin option { background: var(--surface); color: var(--ink); }' +
    '.doc p, .lede { text-align: justify; -webkit-hyphens: auto; hyphens: auto; }' +
    '@media (max-width: 760px) { .doc p, .lede { text-align: left; } }' +
    'a { -webkit-user-drag: none; }' +
    '</style>');

  // A mouse drag selects text; the click that ends it does not follow a link
  // or open an image.
  var down = null;
  document.addEventListener('mousedown', function (e) { down = { x: e.clientX, y: e.clientY }; }, true);
  document.addEventListener('click', function (e) {
    var moved = down && Math.abs(e.clientX - down.x) + Math.abs(e.clientY - down.y) > 4;
    down = null;
    if (moved && !e.target.closest('.lightbox')) {
      e.preventDefault();
      e.stopPropagation();
    }
  }, true);

  // Classic is the page's own style; each other skin is a stylesheet over it.
  SKINS.forEach(function (s) {
    if (s[0] === 'classic') return;
    document.write('<link rel="stylesheet" data-skin="' + s[0] + '" href="' +
      base + s[0] + '.css"' + (s[0] === skin ? '' : ' media="not all"') + '>');
  });

  function apply(name) {
    try { localStorage.setItem('skin', name); } catch (_) {}
    mark(name);
    var links = document.querySelectorAll('link[data-skin]');
    for (var i = 0; i < links.length; i++)
      links[i].media = links[i].getAttribute('data-skin') === name ? 'all' : 'not all';
  }

  document.addEventListener('DOMContentLoaded', function () {
    var menu = document.querySelector('.menu.site');
    if (!menu || !selectable) return;
    var select = document.createElement('select');
    select.className = 'skin';
    select.setAttribute('aria-label', 'Skin');
    SKINS.forEach(function (s) {
      select.add(new Option(s[1], s[0], false, s[0] === skin));
    });
    select.addEventListener('change', function () { apply(select.value); });
    menu.appendChild(select);
  });
})();
