// Global API + player layer for the music site
(function () {
  const API = (window.API_BASE || '') + '/api';

  // Username (no auth - just a local handle for posting/comments)
  function getUser() {
    let u = localStorage.getItem('mw_user');
    if (!u) {
      u = '碳基-' + Math.floor(Math.random() * 9000 + 1000);
      localStorage.setItem('mw_user', u);
    }
    return u;
  }
  function setUser(name) {
    localStorage.setItem('mw_user', name);
  }

  // Tiny fetch wrapper
  async function api(path, opts = {}) {
    const init = Object.assign({ headers: { 'Content-Type': 'application/json' } }, opts);
    if (init.body && typeof init.body !== 'string') init.body = JSON.stringify(init.body);
    const res = await fetch(API + path, init);
    if (!res.ok) throw new Error('API ' + res.status + ': ' + (await res.text()));
    if (res.status === 204) return null;
    return res.json();
  }

  // ---- Audio player (global, singleton) ----
  const audio = new Audio();
  audio.preload = 'metadata';
  let queue = [];
  let qIdx = -1;

  const player = {
    audio,
    play(song, list) {
      if (list && Array.isArray(list)) {
        queue = list;
        qIdx = list.findIndex(s => s.id === song.id);
        if (qIdx < 0) { queue = [song]; qIdx = 0; }
      } else if (!queue.length || queue[qIdx]?.id !== song.id) {
        queue = [song]; qIdx = 0;
      }
      audio.src = song.audioUrl;
      audio.play().catch(e => console.warn('Play failed:', e));
      api('/songs/' + song.id + '/play', { method: 'POST' }).catch(() => {});
      renderPlayerBar();
    },
    toggle() {
      if (!audio.src) return;
      if (audio.paused) audio.play(); else audio.pause();
    },
    next() {
      if (!queue.length) return;
      qIdx = (qIdx + 1) % queue.length;
      this.play(queue[qIdx], queue);
    },
    prev() {
      if (!queue.length) return;
      qIdx = (qIdx - 1 + queue.length) % queue.length;
      this.play(queue[qIdx], queue);
    },
    current() { return queue[qIdx]; }
  };

  audio.addEventListener('ended', () => player.next());
  audio.addEventListener('play', renderPlayerBar);
  audio.addEventListener('pause', renderPlayerBar);
  audio.addEventListener('timeupdate', updateProgress);

  function fmtTime(sec) {
    if (!sec || isNaN(sec)) return '0:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60).toString().padStart(2, '0');
    return m + ':' + s;
  }

  function updateProgress() {
    const fill = document.querySelector('.player-bar .fill');
    const cur = document.querySelector('.player-bar .cur');
    const tot = document.querySelector('.player-bar .tot');
    if (!fill) return;
    const ratio = audio.duration ? (audio.currentTime / audio.duration) * 100 : 0;
    fill.style.width = ratio + '%';
    if (cur) cur.textContent = fmtTime(audio.currentTime);
    if (tot) tot.textContent = fmtTime(audio.duration);
  }

  function renderPlayerBar() {
    let bar = document.querySelector('.player-bar');
    if (!bar) {
      bar = document.createElement('div');
      bar.className = 'player-bar';
      document.body.appendChild(bar);
    }
    const s = player.current();
    const cover = s ? (s.coverUrl || 'https://picsum.photos/seed/x/80') : '';
    const title = s ? s.title : '未在播放';
    const artist = s ? s.artist : '选一首歌开始';
    const playIcon = audio.paused ? '▶' : '❚❚';
    bar.innerHTML = `
      <div class="now">
        ${s ? `<img src="${cover}" alt="">` : '<div style="width:48px;height:48px;border-radius:8px;background:#222"></div>'}
        <div style="min-width:0">
          <div class="t">${escapeHtml(title)}</div>
          <div class="a">${escapeHtml(artist)}</div>
        </div>
      </div>
      <div class="controls">
        <div class="ctrl-row">
          <button title="上一首" data-act="prev">⏮</button>
          <button class="play-btn" data-act="toggle">${playIcon}</button>
          <button title="下一首" data-act="next">⏭</button>
        </div>
        <div class="progress">
          <span class="cur">0:00</span>
          <div class="progress-bar"><div class="fill"></div></div>
          <span class="tot">0:00</span>
        </div>
      </div>
      <div class="right">
        <div class="volume">
          <span>🔊</span>
          <input type="range" min="0" max="100" value="${Math.round(audio.volume*100)}" style="flex:1">
        </div>
      </div>
    `;
    bar.querySelector('[data-act=prev]').onclick = () => player.prev();
    bar.querySelector('[data-act=next]').onclick = () => player.next();
    bar.querySelector('[data-act=toggle]').onclick = () => player.toggle();
    bar.querySelector('.progress-bar').onclick = (ev) => {
      const r = ev.currentTarget.getBoundingClientRect();
      const ratio = (ev.clientX - r.left) / r.width;
      if (audio.duration) audio.currentTime = ratio * audio.duration;
    };
    const vol = bar.querySelector('input[type=range]');
    if (vol) vol.oninput = (ev) => audio.volume = ev.target.value / 100;
    updateProgress();
  }

  function escapeHtml(s) {
    if (s == null) return '';
    return String(s).replace(/[&<>"']/g, c => ({
      '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
    }[c]));
  }

  function fmtCount(n) {
    if (n == null) return '0';
    if (n >= 10000) return (n/10000).toFixed(1) + 'w';
    if (n >= 1000) return (n/1000).toFixed(1) + 'k';
    return String(n);
  }

  // ---- Top nav (rendered into <div id="nav-mount">) ----
  function renderNav(active) {
    const mount = document.getElementById('nav-mount');
    if (!mount) return;
    mount.innerHTML = `
      <nav class="nav">
        <div class="nav-inner">
          <a href="index.html" class="logo">🎵 碳基音浪</a>
          <div class="nav-links">
            <a href="index.html" class="nav-link ${active==='home'?'active':''}">首页</a>
            <a href="discover.html" class="nav-link ${active==='discover'?'active':''}">发现</a>
            <a href="playlists.html" class="nav-link ${active==='playlists'?'active':''}">歌单</a>
            <a href="ai.html" class="nav-link ${active==='ai'?'active':''}">教父AI音乐<span class="badge">NEW</span></a>
            <a href="feed.html" class="nav-link ${active==='feed'?'active':''}">碳基圈</a>
          </div>
          <div class="nav-search">
            <span>🔍</span>
            <input id="nav-search-input" placeholder="搜索歌曲、歌手..." />
          </div>
          <div class="user-pill" id="user-pill" title="点击修改昵称">👤 ${escapeHtml(getUser())}</div>
        </div>
      </nav>
    `;
    document.getElementById('user-pill').onclick = () => {
      const v = prompt('请输入你的昵称', getUser());
      if (v && v.trim()) { setUser(v.trim()); renderNav(active); }
    };
    const si = document.getElementById('nav-search-input');
    si.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && si.value.trim()) {
        location.href = 'discover.html?q=' + encodeURIComponent(si.value.trim());
      }
    });
  }

  window.MW = {
    api, player, getUser, setUser, escapeHtml, fmtTime, fmtCount, renderNav
  };
})();
