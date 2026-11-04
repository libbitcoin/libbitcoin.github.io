(function () {
  'use strict';
  var base = document.currentScript.src.replace(/[^\/]*$/, '');
  var LIMIT = 12;
  var BEFORE = 60;
  var AFTER = 140;

  document.write('<style>' +
    '.mast { position: relative; }' +
    '.menu .search { position: absolute; top: 56px; right: 0; width: min(340px, calc(100% - 152px)); }' +
    '.menu .search input { box-sizing: border-box; width: 100%; font: inherit; font-size: 13px; ' +
    'letter-spacing: normal; color: var(--ink); background: transparent; ' +
    'border: 1px solid var(--rule); border-radius: 3px; padding: 6px 10px; }' +
    '.menu .search input::placeholder { color: var(--ink-3); text-transform: uppercase; letter-spacing: .08em; }' +
    '.menu .search input:focus { outline: none; border-color: var(--accent); }' +
    '.menu .search .results { position: absolute; top: calc(100% + 10px); right: 0; z-index: 20; ' +
    'width: min(600px, calc(100vw - 48px)); max-height: 70vh; overflow-y: auto; ' +
    'background: var(--surface); border: 1px solid var(--rule); border-radius: 3px; box-shadow: var(--shadow); ' +
    'text-transform: none; letter-spacing: normal; }' +
    '.menu .search .results a { display: block; padding: 10px 14px; border-bottom: 1px solid var(--rule-soft); }' +
    '.menu .search .results a:last-child { border-bottom: 0; }' +
    '.menu .search .results a:hover, .menu .search .results a:focus, .menu .search .results a.on { ' +
    'color: inherit; background: color-mix(in srgb, var(--ink) 8%, transparent); }' +
    '.menu .search .results b { display: block; color: var(--heading); font-weight: 600; }' +
    '.menu .search .results span { display: block; margin-top: 3px; color: var(--ink-2); ' +
    'font-family: var(--sans); font-size: 13px; line-height: 1.45; }' +
    '.menu .search .results mark { background: transparent; color: var(--heading); }' +
    '.menu .search .results p { margin: 0; padding: 10px 14px; color: var(--ink-3); }' +
    '</style>');

  var index = null;
  var loading = null;

  function load() {
    loading = loading || fetch(base + 'search.json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        index = [];
        data.forEach(function (page) {
          page.s.forEach(function (s) {
            index.push({ url: page.u + (s[0] ? '#' + s[0] : ''), page: page.t, head: s[1],
              text: s[2], low: (page.t + ' ' + s[1] + ' ' + s[2]).toLowerCase(),
              top: (page.t + ' ' + s[1]).toLowerCase() });
          });
        });
      });
    return loading;
  }

  function escape(text) {
    return text.replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function pattern(terms) {
    return new RegExp('(' + terms.map(function (t) {
      return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }).join('|') + ')', 'gi');
  }

  function count(text, term) {
    var n = 0;
    for (var i = text.indexOf(term); i >= 0 && n < 5; i = text.indexOf(term, i + term.length)) n++;
    return n;
  }

  function score(entry, terms) {
    var total = 0;
    for (var i = 0; i < terms.length; i++) {
      if (entry.low.indexOf(terms[i]) < 0) return 0;
      total += (entry.top.indexOf(terms[i]) >= 0 ? 10 : 0) + count(entry.low, terms[i]);
    }
    return total;
  }

  function snippet(text, terms, marks) {
    var at = text.toLowerCase().indexOf(terms[0]);
    if (at < 0) at = 0;
    var start = Math.max(0, text.lastIndexOf(' ', Math.max(0, at - BEFORE)));
    var end = text.indexOf(' ', at + AFTER);
    if (end < 0) end = text.length;
    var cut = text.slice(start, end).trim();
    return (start > 0 ? '… ' : '') + escape(cut).replace(marks, '<mark>$1</mark>') +
      (end < text.length ? ' …' : '');
  }

  function search(query) {
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    return index.map(function (entry) { return { entry: entry, score: score(entry, terms) }; })
      .filter(function (r) { return r.score > 0; })
      .sort(function (a, b) { return b.score - a.score; })
      .slice(0, LIMIT)
      .map(function (r) { return r.entry; });
  }

  function attach(box) {
    var input = box.querySelector('input');
    var panel = document.createElement('div');
    panel.className = 'results';
    panel.hidden = true;
    box.appendChild(panel);

    function links() { return panel.querySelectorAll('a'); }

    function move(step) {
      var all = links();
      if (!all.length) return;
      var current = panel.querySelector('a.on');
      var i = Array.prototype.indexOf.call(all, current) + step;
      if (current) current.classList.remove('on');
      all[(i + all.length) % all.length].classList.add('on');
      all[(i + all.length) % all.length].scrollIntoView({ block: 'nearest' });
    }

    function show() {
      var query = input.value.trim();
      if (!query) { panel.hidden = true; return; }
      load().then(function () {
        if (input.value.trim() !== query) return;
        var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
        var marks = pattern(terms);
        var found = search(query);
        panel.innerHTML = found.length ? found.map(function (e) {
          var title = e.head && e.head !== e.page ? e.page + ' › ' + e.head : e.page;
          return '<a href="' + base + e.url + '"><b>' + escape(title).replace(marks, '<mark>$1</mark>') +
            '</b><span>' + snippet(e.text, terms, marks) + '</span></a>';
        }).join('') : '<p>No results</p>';
        panel.hidden = false;
      }, function () {
        panel.innerHTML = '<p>Search is unavailable</p>';
        panel.hidden = false;
      });
    }

    input.addEventListener('focus', load);
    input.addEventListener('input', show);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
      else if (e.key === 'Escape') { panel.hidden = true; input.blur(); }
      else if (e.key === 'Enter') {
        var target = panel.querySelector('a.on') || links()[0];
        if (target) location.href = target.href;
      }
    });
    input.addEventListener('focus', function () { if (input.value.trim()) show(); });
    document.addEventListener('click', function (e) {
      if (!box.contains(e.target) || e.target.closest('.results a')) panel.hidden = true;
    });
    document.addEventListener('keydown', function (e) {
      var tag = document.activeElement && document.activeElement.tagName;
      if (e.key === '/' && tag !== 'INPUT' && tag !== 'TEXTAREA' && tag !== 'SELECT') {
        e.preventDefault();
        input.focus();
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var box = document.querySelector('.menu.site .search');
    if (box) attach(box);
  });
})();
