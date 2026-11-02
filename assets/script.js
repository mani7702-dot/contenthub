/**
 * ContentHub — Core Shared Engine
 * Handles theme, feed loading, views counter, global search, update toast, bottom nav.
 *
 * Every internal link is built from BASE, the site root derived from this
 * script's own URL — so the same file works on /index.html and on
 * /articles/<slug>.html without any relative-path guesswork.
 */

(function () {
  'use strict';

  // 0. Site root, derived from this script's own <script src>
  var BASE = (function () {
    var s = (document.currentScript && document.currentScript.src) || '';
    return s ? s.replace(/assets\/script\.js.*$/, '') : '';
  })();

  // 1. Theme Manager
  var themeToggle = document.getElementById('themeToggle');
  function getTheme() {
    return localStorage.getItem('ch_theme') ||
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }
  function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('ch_theme', t);
    if (themeToggle) themeToggle.textContent = t === 'dark' ? '☀️' : '🌙';
  }
  setTheme(getTheme());
  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      setTheme(getTheme() === 'dark' ? 'light' : 'dark');
    });
  }

  // 2. View Count Tracker (localStorage based)
  function getViews(id) {
    try {
      var store = JSON.parse(localStorage.getItem('ch_views') || '{}');
      return store[id] || 0;
    } catch (e) { return 0; }
  }
  function incViews(id) {
    try {
      var store = JSON.parse(localStorage.getItem('ch_views') || '{}');
      store[id] = (store[id] || 0) + 1;
      localStorage.setItem('ch_views', JSON.stringify(store));
      return store[id];
    } catch (e) { return 1; }
  }

  // 3. Global Feed Loader (only used by the search overlay now)
  var cachedFeed = null;
  function loadFeed(cb) {
    if (cachedFeed) { cb(cachedFeed); return; }
    fetch(BASE + 'content.json?v=' + Date.now())
      .then(function (r) { return r.json(); })
      .then(function (data) {
        cachedFeed = data;
        cb(data);
        checkUpdateToast(data);
      })
      .catch(function () { cb({ blog: [], news: [], facts: [] }); });
  }

  // 4. Update Toast notification when feed timestamp changes
  function checkUpdateToast(data) {
    if (!data.updated) return;
    var lastSeen = localStorage.getItem('ch_last_updated');
    if (lastSeen && lastSeen !== data.updated) {
      var toast = document.createElement('div');
      toast.className = 'toast show';
      toast.innerHTML = '<span>⚡ <b>New stories</b> just arrived!</span><button onclick="location.reload()">Refresh</button>';
      document.body.appendChild(toast);
    }
    localStorage.setItem('ch_last_updated', data.updated);
  }

  // 5. Build Global Search Modal + Bottom Navigation Site-Wide
  function initGlobalUI() {
    var nav = document.querySelector('.topbar .nav');
    if (nav && !document.getElementById('navSearchBtn')) {
      var sBtn = document.createElement('button');
      sBtn.id = 'navSearchBtn';
      sBtn.className = 'search-btn';
      sBtn.setAttribute('aria-label', 'Search site');
      sBtn.innerHTML = '🔍';
      sBtn.onclick = openGlobalSearch;
      var toggle = document.getElementById('themeToggle');
      if (toggle) nav.insertBefore(sBtn, toggle);
      else nav.appendChild(sBtn);
    }

    if (!document.getElementById('globalSearchOverlay')) {
      var overlay = document.createElement('div');
      overlay.id = 'globalSearchOverlay';
      overlay.className = 'search-overlay';
      overlay.innerHTML =
        '<div class="search-box">' +
          '<input id="gSearchInput" type="text" placeholder="Search blogs, news, and facts... (Press Esc to exit)">' +
          '<div id="gSearchResults" class="search-results"></div>' +
        '</div>';
      document.body.appendChild(overlay);

      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeGlobalSearch();
      });
      document.addEventListener('keydown', function (e) {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
          e.preventDefault(); openGlobalSearch();
        }
        if (e.key === 'Escape') closeGlobalSearch();
      });
      document.getElementById('gSearchInput').addEventListener('input', runGlobalSearch);
    }

    if (!document.getElementById('bottomNav')) {
      var page = window.location.pathname.split('/').pop() || 'index.html';
      var bNav = document.createElement('nav');
      bNav.id = 'bottomNav';
      bNav.className = 'bottom-nav';
      bNav.innerHTML =
        '<a href="' + BASE + 'index.html" class="' + (page === 'index.html' ? 'on' : '') + '"><span class="bi">🏠</span>Home</a>' +
        '<a href="' + BASE + 'blog.html" class="' + (page === 'blog.html' ? 'on' : '') + '"><span class="bi">✍️</span>Blog</a>' +
        '<a href="' + BASE + 'news.html" class="' + (page === 'news.html' ? 'on' : '') + '"><span class="bi">📰</span>News</a>' +
        '<a href="' + BASE + 'facts.html" class="' + (page === 'facts.html' ? 'on' : '') + '"><span class="bi">💡</span>Facts</a>' +
        '<a href="' + BASE + 'categories.html" class="' + (page === 'categories.html' ? 'on' : '') + '"><span class="bi">🏷️</span>Explore</a>' +
        '<a href="' + BASE + 'games.html" class="' + (page === 'games.html' ? 'on' : '') + '"><span class="bi">🎮</span>Games</a>';
      document.body.appendChild(bNav);
    }
  }

  function openGlobalSearch() {
    var overlay = document.getElementById('globalSearchOverlay');
    if (overlay) {
      overlay.classList.add('open');
      var input = document.getElementById('gSearchInput');
      input.value = '';
      input.focus();
      runGlobalSearch();
    }
  }
  function closeGlobalSearch() {
    var overlay = document.getElementById('globalSearchOverlay');
    if (overlay) overlay.classList.remove('open');
  }

  function runGlobalSearch() {
    var q = (document.getElementById('gSearchInput').value || '').trim().toLowerCase();
    var res = document.getElementById('gSearchResults');
    if (!res) return;
    if (!cachedFeed) { loadFeed(runGlobalSearch); return; }

    if (!q) {
      res.innerHTML = '<div class="sr-empty">Type to search across all blogs, news headlines, and facts.</div>';
      return;
    }

    var items = [];
    (cachedFeed.blog || []).forEach(function (b) {
      if ((b.title + ' ' + b.excerpt + ' ' + b.tag).toLowerCase().indexOf(q) > -1) {
        items.push({ type: 'blog', title: b.title, tag: b.tag || 'Blog', url: BASE + 'articles/' + b.id + '.html' });
      }
    });
    (cachedFeed.news || []).forEach(function (n) {
      if ((n.title + ' ' + n.excerpt + ' ' + n.tag).toLowerCase().indexOf(q) > -1) {
        items.push({ type: 'news', title: n.title, tag: n.tag || 'News', url: BASE + 'articles/' + n.id + '.html' });
      }
    });
    (cachedFeed.facts || []).forEach(function (f) {
      var text = f.fact || f.title || '';
      if (text.toLowerCase().indexOf(q) > -1) {
        items.push({ type: 'facts', title: text.substring(0, 70) + '…', tag: f.category || 'Fact', url: BASE + 'facts.html' });
      }
    });

    if (!items.length) {
      res.innerHTML = '<div class="sr-empty">No results found for "' + q + '".</div>';
      return;
    }

    res.innerHTML = items.slice(0, 8).map(function (it) {
      return '<a class="sr-item" href="' + it.url + '">' +
        '<span class="tag tag-' + it.type + '">' + it.tag + '</span>' +
        '<div><h4>' + it.title + '</h4><span>Type: ' + it.type.toUpperCase() + '</span></div>' +
        '</a>';
    }).join('');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGlobalUI);
  } else {
    initGlobalUI();
  }

  // Export window API
  window.CH = {
    loadFeed: loadFeed,
    getViews: getViews,
    incViews: incViews,
    openSearch: openGlobalSearch
  };
})();

/* ---------- Game progress + repeat-visit persistence ---------- */
(function () {
  'use strict';
  function load() {
    try { return JSON.parse(localStorage.getItem('ch_game_stats') || '{}'); } catch (e) { return {}; }
  }
  function save(stats) {
    try { localStorage.setItem('ch_game_stats', JSON.stringify(stats)); } catch (e) {}
  }
  function record(game, value) {
    var s = load();
    s.best = s.best || {};
    s.plays = s.plays || {};
    s.plays[game] = (s.plays[game] || 0) + 1;
    var prev = s.best[game];
    if (prev === undefined || value < prev) s.best[game] = value;
    s.lastGame = game;
    s.lastPlay = Date.now();
    save(s);
    return s;
  }
  function best(game) {
    var s = load();
    return (s.best && s.best[game]) || null;
  }
  function plays(game) {
    var s = load();
    return (s.plays && s.plays[game]) || 0;
  }
  function summary() {
    return load();
  }
  window.CH.stats = {
    record: record,
    best: best,
    plays: plays,
    summary: summary
  };
})();
