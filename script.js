/* ==========================================
   WOOD'S WASTE - FINAL PRODUCTION JS
   ========================================== */

document.addEventListener("DOMContentLoaded", () => {
    initMobileNav();
    initNavbarScroll();
    initSmoothScrolling();
    initScrollReveal();
    initFormEnhancements();
    initCounterAnimations();
});

/* ==========================================
   MOBILE NAVIGATION
   ========================================== */

function initMobileNav() {
    const hamburger = document.getElementById("hamburger");
    const navLinks = document.getElementById("navLinks");

    if (!hamburger || !navLinks) return;

    hamburger.addEventListener("click", () => {
        navLinks.classList.toggle("mobile-open");
        hamburger.classList.toggle("active");
    });

    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", () => {
            navLinks.classList.remove("mobile-open");
            hamburger.classList.remove("active");
        });
    });

    document.addEventListener("click", (e) => {
        if (!navLinks.contains(e.target) && !hamburger.contains(e.target)) {
            navLinks.classList.remove("mobile-open");
            hamburger.classList.remove("active");
        }
    });
}

/* ==========================================
   NAVBAR SCROLL
   ========================================== */

function initNavbarScroll() {
    const navbar = document.querySelector(".navbar");
    if (!navbar) return;

    window.addEventListener("scroll", () => {
        navbar.classList.toggle("scrolled", window.scrollY > 30);
    });
}

/* ==========================================
   SMOOTH SCROLL
   ========================================== */

function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", (e) => {
            const target = document.querySelector(anchor.getAttribute("href"));
            if (!target) return;
            e.preventDefault();
            window.scrollTo({ top: target.offsetTop - 80, behavior: "smooth" });
        });
    });
}

/* ==========================================
   SCROLL REVEAL
   ========================================== */

function initScrollReveal() {
    const elements = document.querySelectorAll(
        ".service-card, .section-header, .process-step, .value-item, .about-content, .about-visual"
    );

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) entry.target.classList.add("in-view");
        });
    }, { threshold: 0.12 });

    elements.forEach(el => observer.observe(el));
}

/* ==========================================
   FORM UX
   ========================================== */

function initFormEnhancements() {
    const form = document.querySelector(".quote-form");
    if (!form) return;

    form.addEventListener("submit", () => {
        const btn = form.querySelector("button[type='submit']");
        if (!btn) return;
        btn.innerText = "Sending...";
        btn.disabled = true;
    });
}

/* ==========================================
   COUNTER ANIMATION
   — reads target from data-target attribute
   — writes only into a child .num span
   — never touches the .suffix span
   ========================================== */

function initCounterAnimations() {
    const counters = document.querySelectorAll(".stat-number");

    counters.forEach(el => {
        // Pull the numeric value out of the element's data attribute
        // (set below), then wrap the bare text node in a .num span
        // so we can update just the number without touching .suffix

        const suffixEl = el.querySelector(".suffix");
        const suffixText = suffixEl ? suffixEl.outerHTML : "";

        // Get the raw number — strip everything non-numeric
        const raw = el.innerText.replace(/\D/g, "");
        const target = parseInt(raw);
        if (!target) return;

        // Store target for the observer callback
        el.dataset.target = target;

        // Rebuild innerHTML: a .num span + the suffix span
        el.innerHTML = `<span class="num">0</span>${suffixText}`;
    });

    const animate = (el) => {
        const target = parseInt(el.dataset.target);
        const numEl = el.querySelector(".num");
        if (!numEl) return;

        let count = 0;
        const step = Math.max(1, Math.floor(target / 60));

        const update = () => {
            count = Math.min(count + step, target);
            numEl.innerText = count;
            if (count < target) requestAnimationFrame(update);
        };

        update();
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animate(entry.target);
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.6 });

    document.querySelectorAll(".stat-number").forEach(c => observer.observe(c));
}
function toggleAreas() {
    const extras = document.querySelectorAll('.area-card.extra');
    const btn = document.getElementById('areaToggle');
    const isHidden = extras[0].classList.contains('hidden');

    extras.forEach(card => card.classList.toggle('hidden'));
    btn.textContent = isHidden ? 'Show less ↑' : 'View all areas ↓';
}
document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
        const answer = btn.nextElementSibling;
        const isOpen = btn.getAttribute('aria-expanded') === 'true';
        document.querySelectorAll('.faq-question').forEach(b => {
            b.setAttribute('aria-expanded', 'false');
            b.nextElementSibling.classList.remove('open');
        });
        if (!isOpen) {
            btn.setAttribute('aria-expanded', 'true');
            answer.classList.add('open');
        }
    });
});

// ── JOB ACTUAL & INSIGHTS ──
let actualJobId = null;

function openActual(jobId) {
  const job = jobHistory.find(j => j.id === jobId);
  if (!job) return;
  actualJobId = jobId;
  document.getElementById('actualQuotedPrice').textContent = job.price;
  const ll = {minimum:'Min Load',quarter:'Quarter Load',half:'Half Load',full:'Full Truck','ai-multi':'AI Photo Quote'};
  const parts = [ll[job.load]||job.load];
  if (job.specials && job.specials.length) parts.push(job.specials.join(', '));
  if (job.miles) parts.push(job.miles+' mi');
  document.getElementById('actualQuotedDetail').textContent = parts.join(' · ');
  document.getElementById('actualCharged').value = '';
  document.getElementById('actualHours').value = job.hours || '';
  document.getElementById('actualNotes').value = job.actual?.notes || '';
  document.getElementById('actualDiff').style.display = 'none';
  document.getElementById('actualPanel').classList.add('open');
}
function closeActual() { document.getElementById('actualPanel').classList.remove('open'); }
function closeActualOutside(e) { if (e.target === document.getElementById('actualPanel')) closeActual(); }

function onActualInput() {
  const charged = parseFloat(document.getElementById('actualCharged').value) || 0;
  const job = jobHistory.find(j => j.id === actualJobId);
  if (!job || !charged) { document.getElementById('actualDiff').style.display = 'none'; return; }
  const quotedMid = parseFloat(job.price.replace(/[^0-9.]/g,'')) || 0;
  const diff = charged - quotedMid;
  const diffEl = document.getElementById('actualDiff');
  diffEl.style.display = 'block';
  diffEl.className = 'actual-diff ' + (diff >= 0 ? 'over' : 'under');
  document.getElementById('actualDiffLabel').textContent = diff >= 0 ? 'Charged more than quoted' : 'Charged less than quoted';
  document.getElementById('actualDiffVal').textContent = (diff >= 0 ? '+' : '') + '$' + Math.abs(Math.round(diff));
  document.getElementById('actualDiffSub').textContent = diff >= 0 ? 'Good — you captured extra value' : 'You left money on the table';
}

function saveActual() {
  const job = jobHistory.find(j => j.id === actualJobId);
  if (!job) return;
  const charged = parseFloat(document.getElementById('actualCharged').value) || null;
  const hours = parseFloat(document.getElementById('actualHours').value) || null;
  const notes = document.getElementById('actualNotes').value.trim();
  job.actual = { charged, hours, notes, loggedAt: new Date().toISOString() };
  persistHistory(); renderHistory();
  closeActual();
  showToast('✓ Job outcome saved');
  refreshInsightsBtn();
}

function refreshInsightsBtn() {
  const hasActuals = jobHistory.some(j => j.actual?.charged);
  const btn = document.getElementById('insightsNavBtn');
  if (btn) btn.style.display = hasActuals ? 'inline-flex' : 'none';
}

function openInsights() {
  renderInsights();
  document.getElementById('insightsPanel').classList.add('open');
}
function closeInsights() { document.getElementById('insightsPanel').classList.remove('open'); }
function closeInsightsOutside(e) { if (e.target === document.getElementById('insightsPanel')) closeInsights(); }

function renderInsights() {
  const body = document.getElementById('insightsBody');
  const logged = jobHistory.filter(j => j.actual?.charged);
  if (logged.length < 2) {
    body.innerHTML = '<div class="insights-empty">Log at least 2 job outcomes to see insights.<br><br>After saving a quote, tap "How\'d it go?" in history to record what actually happened.</div>';
    return;
  }
  const diffs = logged.map(j => {
    const quoted = parseFloat(j.price.replace(/[^0-9.]/g,'')) || 0;
    return j.actual.charged - quoted;
  });
  const avgDiff = diffs.reduce((a,b) => a+b, 0) / diffs.length;
  const totalLeft = diffs.filter(d => d < 0).reduce((a,b) => a+b, 0);
  const winRate = Math.round((diffs.filter(d => d >= 0).length / diffs.length) * 100);

  const loadKeys = ['minimum','quarter','half','full'];
  const loadLabels = {minimum:'Min Load',quarter:'Quarter Load',half:'Half Load',full:'Full Truck'};
  const loadStats = {};
  loadKeys.forEach(k => {
    const jobs = logged.filter(j => j.load === k);
    if (!jobs.length) return;
    const d = jobs.map(j => j.actual.charged - (parseFloat(j.price.replace(/[^0-9.]/g,''))||0));
    loadStats[k] = { count: jobs.length, avgDiff: d.reduce((a,b)=>a+b,0)/d.length };
  });

  const alerts = [];
  Object.entries(loadStats).forEach(([k,s]) => {
    if (s.count >= 2 && s.avgDiff < -30) alerts.push(`Your <strong>${loadLabels[k]}</strong> quotes are averaging <strong>$${Math.abs(Math.round(s.avgDiff))} under</strong> what you charge. Consider raising that load rate.`);
  });
  const timeLogged = logged.filter(j => j.actual?.hours && j.hours);
  if (timeLogged.length >= 2) {
    const avgOver = timeLogged.map(j => j.actual.hours - j.hours).reduce((a,b)=>a+b,0) / timeLogged.length;
    if (avgOver > 0.4) alerts.push(`Jobs are taking <strong>${avgOver.toFixed(1)} hours longer</strong> on average than you quote. Your labor cost may be underestimated.`);
  }

  let html = '';
  if (alerts.length) {
    html += '<div class="insights-alert"><div class="insights-alert-label">⚡ Heads up</div>' + alerts.map(a => `<div class="insights-alert-text">${a}</div>`).join('<br>') + '</div>';
  }
  html += `<div class="insights-stat-grid">
    <div class="insights-stat ${avgDiff >= 0 ? 'positive' : 'negative'}">
      <div class="insights-stat-label">Avg vs quoted</div>
      <div class="insights-stat-val">${avgDiff >= 0 ? '+' : ''}$${Math.abs(Math.round(avgDiff))}</div>
      <div class="insights-stat-sub">${logged.length} jobs logged</div>
    </div>
    <div class="insights-stat ${winRate >= 50 ? 'positive' : 'negative'}">
      <div class="insights-stat-label">Quoted right</div>
      <div class="insights-stat-val">${winRate}%</div>
      <div class="insights-stat-sub">charged ≥ quoted</div>
    </div>
    <div class="insights-stat negative">
      <div class="insights-stat-label">Left on table</div>
      <div class="insights-stat-val">$${Math.abs(Math.round(totalLeft))}</div>
      <div class="insights-stat-sub">total undercharges</div>
    </div>
    <div class="insights-stat">
      <div class="insights-stat-label">Jobs tracked</div>
      <div class="insights-stat-val">${logged.length}</div>
      <div class="insights-stat-sub">of ${jobHistory.length} total</div>
    </div>
  </div>`;

  if (Object.keys(loadStats).length) {
    html += '<div class="insights-section-title">By load size</div>';
    Object.entries(loadStats).forEach(([k,s]) => {
      const cls = s.avgDiff > 10 ? 'pos' : s.avgDiff < -10 ? 'neg' : 'neu';
      const sign = s.avgDiff >= 0 ? '+' : '';
      html += `<div class="insights-load-row"><div class="insights-load-name">${loadLabels[k]}</div><div class="insights-load-stats"><div class="insights-load-avg">${sign}$${Math.abs(Math.round(s.avgDiff))} avg</div><div class="insights-load-diff ${cls}">${s.count} job${s.count>1?'s':''} · ${s.avgDiff > 10 ? 'charging well' : s.avgDiff < -10 ? 'undercharging' : 'on track'}</div></div></div>`;
    });
  }
  body.innerHTML = html;
}
