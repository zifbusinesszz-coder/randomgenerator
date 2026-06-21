/* ==========================================================
   WOOD'S WASTE — site behavior + motion
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {
  initNav();
  initReveal();
  initCounters();
  initReviewsDrag();
  initFAQ();
  initCityFAQ();
  initAreas();
  initDateTime();
  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
});

/* ── Nav: scroll state + mobile menu ── */
function initNav() {
  var nav = document.getElementById('nav');
  var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 24); };
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  var ham = document.getElementById('hamburger');
  var links = document.getElementById('navLinks');
  if (ham && links) {
    ham.addEventListener('click', function () { ham.classList.toggle('active'); links.classList.toggle('mobile-open'); });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { ham.classList.remove('active'); links.classList.remove('mobile-open'); });
    });
  }
}

/* ── Scroll reveal ── */
function initReveal() {
  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { els.forEach(function (e) { e.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  // light stagger within grids
  ['.feature-grid', '.steps', '.values'].forEach(function (sel) {
    document.querySelectorAll(sel).forEach(function (grid) {
      Array.prototype.forEach.call(grid.children, function (c, i) {
        if (c.classList.contains('reveal')) c.style.transitionDelay = (i % 3) * 70 + 'ms';
      });
    });
  });
  els.forEach(function (e) { io.observe(e); });
}

/* ── Count-up (.num[data-to]) ── */
function initCounters() {
  var nums = document.querySelectorAll('.num[data-to]');
  if (!nums.length) return;
  var ease = function (t) { return 1 - Math.pow(1 - t, 3); };
  var run = function (el) {
    var to = parseInt(el.getAttribute('data-to'), 10) || 0, dur = 1200, t0 = null;
    var tick = function (now) {
      if (!t0) t0 = now;
      var p = Math.min(1, (now - t0) / dur);
      el.textContent = Math.round(ease(p) * to).toLocaleString();
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if (!('IntersectionObserver' in window)) { nums.forEach(run); return; }
  var io = new IntersectionObserver(function (entries, obs) {
    entries.forEach(function (e) { if (e.isIntersecting) { run(e.target); obs.unobserve(e.target); } });
  }, { threshold: 0.6 });
  nums.forEach(function (n) { io.observe(n); });
}

/* ── Reviews drag-scroll ── */
function initReviewsDrag() {
  var el = document.getElementById('reviewCarousel');
  if (!el) return;
  var down = false, startX, sl;
  el.addEventListener('mousedown', function (e) { down = true; el.style.cursor = 'grabbing'; startX = e.pageX - el.offsetLeft; sl = el.scrollLeft; });
  el.addEventListener('mouseleave', function () { down = false; el.style.cursor = 'grab'; });
  el.addEventListener('mouseup', function () { down = false; el.style.cursor = 'grab'; });
  el.addEventListener('mousemove', function (e) { if (!down) return; e.preventDefault(); el.scrollLeft = sl - (e.pageX - el.offsetLeft - startX) * 1.4; });
}

/* ── FAQ accordion ── */
function initFAQ() {
  document.querySelectorAll('.faq-q').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.faq-item');
      var ans = item.querySelector('.faq-a');
      var isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(function (o) {
        o.classList.remove('open');
        o.querySelector('.faq-a').style.maxHeight = null;
        o.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
      });
      if (!isOpen) {
        item.classList.add('open');
        ans.style.maxHeight = ans.scrollHeight + 'px';
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });
}

/* ── City-page FAQ accordion (.faq-question / .faq-answer) ── */
function initCityFAQ() {
  document.querySelectorAll('.faq-question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var ans = btn.nextElementSibling;
      var open = btn.getAttribute('aria-expanded') === 'true';
      document.querySelectorAll('.faq-question').forEach(function (b) {
        b.setAttribute('aria-expanded', 'false');
        if (b.nextElementSibling) b.nextElementSibling.classList.remove('open');
      });
      if (!open) { btn.setAttribute('aria-expanded', 'true'); if (ans) ans.classList.add('open'); }
    });
  });
}

/* ── Service areas toggle ── */
function initAreas() {
  var btn = document.getElementById('areaToggle');
  if (!btn) return;
  btn.addEventListener('click', function () {
    var extras = document.querySelectorAll('#areaGrid .extra');
    var open = btn.getAttribute('data-open') === '1';
    extras.forEach(function (c) { c.classList.toggle('hidden', open); });
    btn.setAttribute('data-open', open ? '0' : '1');
    btn.textContent = open ? 'View all areas ↓' : 'Show fewer areas ↑';
  });
}

/* ── Date / Time picker (fetches booked slots from Apps Script) ── */
function initDateTime() {
  var GAS_URL = 'https://script.google.com/macros/s/AKfycbzGbctgjm5ekt7CFSVRzCHDxff_6X88b6mjY3yyb5gHXzTcGD5ZTtSWOYrP8-I4-IkQVw/exec';
  var ALL_TIMES = ['08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00'];
  var LABELS = {'08:00':'8:00 AM','09:00':'9:00 AM','10:00':'10:00 AM','11:00':'11:00 AM','12:00':'12:00 PM','13:00':'1:00 PM','14:00':'2:00 PM','15:00':'3:00 PM','16:00':'4:00 PM','17:00':'5:00 PM'};
  var dateEl = document.getElementById('bDate'), timeEl = document.getElementById('bTime');
  if (!dateEl || !timeEl) return;

  var today = new Date();
  for (var i = 1; i <= 14; i++) {
    var d = new Date(today); d.setDate(today.getDate() + i);
    var val = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
    var opt = document.createElement('option');
    opt.value = val;
    opt.textContent = d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
    dateEl.appendChild(opt);
  }

  function fill(booked) {
    timeEl.innerHTML = '<option value="">Select a time...</option>';
    ALL_TIMES.forEach(function (t) {
      var o = document.createElement('option');
      o.value = t;
      if (booked.indexOf(t) !== -1) { o.textContent = LABELS[t] + ' — Unavailable'; o.disabled = true; }
      else { o.textContent = LABELS[t]; }
      timeEl.appendChild(o);
    });
    timeEl.disabled = false;
  }

  dateEl.addEventListener('change', function () {
    if (!dateEl.value) return;
    timeEl.disabled = true; timeEl.innerHTML = '<option value="">Loading...</option>';
    fetch(GAS_URL + '?date=' + dateEl.value)
      .then(function (r) { return r.json(); })
      .then(function (data) { fill((data && data.booked) || []); })
      .catch(function () { fill([]); });
  });
}


/* ── File upload (called inline from the form) ── */
window._uploadedFiles = [];
function handleFiles(incoming) {
  Array.prototype.slice.call(incoming, 0, 10 - window._uploadedFiles.length).forEach(function (f) {
    if (!window._uploadedFiles.find(function (x) { return x.name === f.name && x.size === f.size; })) window._uploadedFiles.push(f);
  });
  renderFileList();
}
function removeFile(name, size) {
  window._uploadedFiles = window._uploadedFiles.filter(function (f) { return !(f.name === name && f.size === size); });
  renderFileList();
}
function renderFileList() {
  var list = document.getElementById('fileList'); if (!list) return;
  list.innerHTML = '';
  window._uploadedFiles.forEach(function (f) {
    var size = f.size < 1024 * 1024 ? Math.round(f.size / 1024) + 'KB' : (f.size / 1024 / 1024).toFixed(1) + 'MB';
    var row = document.createElement('div'); row.className = 'file-row';
    var thumb = document.createElement('div'); thumb.className = 'file-thumb';
    if (f.type.indexOf('image/') === 0) {
      var img = document.createElement('img'); img.style.cssText = 'width:34px;height:34px;object-fit:cover;border-radius:6px;';
      var r = new FileReader(); r.onload = function (e) { img.src = e.target.result; }; r.readAsDataURL(f);
      thumb.appendChild(img);
    } else { thumb.textContent = '📄'; }
    var info = document.createElement('div'); info.style.cssText = 'flex:1;min-width:0;';
    info.innerHTML = '<div style="font-size:13px;font-weight:500;color:#f7f8f8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + f.name + '</div><div style="font-size:11px;color:#8a8f98;">' + size + '</div>';
    var del = document.createElement('button'); del.type = 'button'; del.textContent = '✕';
    del.style.cssText = 'background:none;border:none;color:#8a8f98;font-size:14px;cursor:pointer;flex-shrink:0;padding:4px;';
    del.onclick = function (ev) { ev.stopPropagation(); removeFile(f.name, f.size); };
    row.append(thumb, info, del);
    list.appendChild(row);
  });
}
function readFileAsBase64(file) {
  return new Promise(function (resolve, reject) {
    var r = new FileReader();
    r.onload = function (e) { resolve(e.target.result.split(',')[1]); };
    r.onerror = reject;
    r.readAsDataURL(file);
  });
}

/* ── Form submit → Apps Script (no-cors, base64 files) ── */
document.addEventListener('DOMContentLoaded', function () {
  var form = document.getElementById('bookingForm');
  if (!form) return;
  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    var btn = document.getElementById('submitBtn'), status = document.getElementById('formStatus');
    btn.disabled = true; btn.textContent = 'Sending...';
    var files = [];
    try {
      files = await Promise.all(window._uploadedFiles.map(async function (f) {
        return { name: f.name, type: f.type, data: await readFileAsBase64(f) };
      }));
    } catch (err) {
      status.style.display = 'block'; status.style.background = 'rgba(239,68,68,.12)'; status.style.color = '#fca5a5';
      status.textContent = 'Error reading files. Please try again.';
      btn.disabled = false; btn.textContent = 'Book my free quote →'; return;
    }
    var payload = {
      name: document.getElementById('bName').value,
      phone: document.getElementById('bPhone').value,
      address: document.getElementById('bAddress').value,
      items: document.getElementById('bItems').value,
      date: document.getElementById('bDate').value,
      time: document.getElementById('bTime').value,
      files: files
    };
    try {
      await fetch('https://script.google.com/macros/s/AKfycbzGbctgjm5ekt7CFSVRzCHDxff_6X88b6mjY3yyb5gHXzTcGD5ZTtSWOYrP8-I4-IkQVw/exec', {
        method: 'POST', mode: 'no-cors', body: JSON.stringify(payload)
      });
      status.style.display = 'block'; status.style.background = 'rgba(16,185,129,.12)'; status.style.color = '#34d399';
      status.textContent = "✓ You're booked! We'll confirm shortly.";
      form.reset();
      window._uploadedFiles = []; renderFileList();
      var t = document.getElementById('bTime'); t.disabled = true; t.innerHTML = '<option value="">Select a date first...</option>';
    } catch (err) {
      status.style.display = 'block'; status.style.background = 'rgba(239,68,68,.12)'; status.style.color = '#fca5a5';
      status.textContent = 'Something went wrong. Please call (507) 298-1179.';
    }
    btn.disabled = false; btn.textContent = 'Book my free quote →';
  });
});
