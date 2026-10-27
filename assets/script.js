/**
 * ContentHub — Core Shared Engine
 * Handles theme, feed loading, views counter, global search, update toast, bottom nav.
 */

(function () {
  'use strict';

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

  // 3. Global Feed Loader
  var cachedFeed = null;
  function loadFeed(cb) {
    if (cachedFeed) { cb(cachedFeed); return; }
    fetch('content.json?v=' + Date.now())
      .then(function (r) { return r.json(); })
      .then(function (data) {
        cachedFeed = data;
        cb(data);
        checkUpdateToast(data);
      })
      .catch(function () {
        // Fallback sample data if fetch fails (e.g. local offline preview)
        cachedFeed = {
          updated: new Date().toISOString(),
          blog: [
            { id: 'b1', title: 'The Future of Storytelling in an AI World', excerpt: 'How human creativity and machine assistance are rewriting narrative.', body: 'Full article content here...', tag: 'Technology', author: 'Maya Verma', date: '2026-10-24', read: '5 min' },
            { id: 'b2', title: 'Building a Morning Routine That Sticks', excerpt: 'Tiny habits, consistent wins — a practical guide to starting your day.', body: 'Full article content here...', tag: 'Lifestyle', author: 'Devon Cole', date: '2026-10-22', read: '4 min' },
            { id: 'b3', title: 'Why Curiosity Beats Talent', excerpt: 'A gentle argument for staying a beginner for as long as possible.', body: 'Full article content here...', tag: 'Mindset', author: 'Aisha Khan', date: '2026-10-20', read: '6 min' }
          ],
          news: [
            { id: 'n1', title: 'Global AI Summit Pledges Safety Standards', excerpt: 'Leaders agree on a shared framework for transparent AI development.', body: 'Full news text here...', tag: 'World', author: 'News Desk', date: '2026-10-26', read: '3 min' },
            { id: 'n2', title: 'Breakthrough in Renewable Storage Technology', excerpt: 'A new battery design promises cheaper, longer-lasting clean energy.', body: 'Full news text here...', tag: 'Science', author: 'News Desk', date: '2026-10-25', read: '4 min' }
          ],
          facts: [
            { id: 'f1', category: 'Nature', fact: 'Honey never spoils. Archaeologists have found pots of honey over 3,000 years old still edible.' },
            { id: 'f2', category: 'Space', fact: 'A day on Venus is longer than its year. It takes 243 Earth days to rotate once.' }
          ]
        };
        cb(cachedFeed);
      });
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
    // A. Add Search Button to Topbar Nav
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

    // B. Search Overlay Element
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

    // C. Mobile Bottom Nav
    if (!document.getElementById('bottomNav')) {
      var page = window.location.pathname.split('/').pop() || 'index.html';
      var bNav = document.createElement('nav');
      bNav.id = 'bottomNav';
      bNav.className = 'bottom-nav';
      bNav.innerHTML =
        '<a href="index.html" class="' + (page === 'index.html' ? 'on' : '') + '"><span class="bi">🏠</span>Home</a>' +
        '<a href="blog.html" class="' + (page === 'blog.html' ? 'on' : '') + '"><span class="bi">✍️</span>Blog</a>' +
        '<a href="news.html" class="' + (page === 'news.html' ? 'on' : '') + '"><span class="bi">📰</span>News</a>' +
        '<a href="facts.html" class="' + (page === 'facts.html' ? 'on' : '') + '"><span class="bi">💡</span>Facts</a>' +
        '<a href="categories.html" class="' + (page === 'categories.html' ? 'on' : '') + '"><span class="bi">🏷️</span>Explore</a>' +
        '<a href="games.html" class="' + (page === 'games.html' ? 'on' : '') + '"><span class="bi">🎮</span>Games</a>';
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
      if ((b.title + b.excerpt + b.tag).toLowerCase().indexOf(q) > -1) {
        items.push({ type: 'blog', title: b.title, tag: b.tag || 'Blog', url: 'article.html?type=blog&id=' + b.id });
      }
    });
    (cachedFeed.news || []).forEach(function (n) {
      if ((n.title + n.excerpt + n.tag).toLowerCase().indexOf(q) > -1) {
        items.push({ type: 'news', title: n.title, tag: n.tag || 'News', url: 'article.html?type=news&id=' + n.id });
      }
    });
    (cachedFeed.facts || []).forEach(function (f) {
      var text = f.fact || f.title || '';
      if (text.toLowerCase().indexOf(q) > -1) {
        items.push({ type: 'facts', title: text.substring(0, 70) + '…', tag: f.category || 'Fact', url: 'facts.html' });
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
  // ch_stats.best.<gameId> = best value ; ch_stats.plays.<gameId> = play count
  function record(game, value) {
    var s = load();
    s.best = s.best || {};
    s.plays = s.plays || {};
    s.plays[game] = (s.plays[game] || 0) + 1;
    var prev = s.best[game];
    if (prev === undefined || value < prev) s.best[game] = value; // lower = better for speed/moves
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