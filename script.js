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
var SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxzTav7WDX-QBwfc0fqDvp6flDi66dkyED0Gx-5o10ERs5o3VbgxpRyFcn3tSsYV0Pk0A/exec';

var HOURS = ['9:00 AM','10:00 AM','11:00 AM','12:00 PM',
             '1:00 PM','2:00 PM','3:00 PM','4:00 PM','5:00 PM'];
var HOUR_VALUES = ['09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00'];

// Populate date dropdown (next 30 days)
(function() {
  var select = document.getElementById('bDate');
  var days   = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  for (var i = 1; i <= 30; i++) {
    var d = new Date();
    d.setDate(d.getDate() + i);
    var label = days[d.getDay()] + ', ' + months[d.getMonth()] + ' ' + d.getDate();
    var value = d.getFullYear() + '-' +
      String(d.getMonth() + 1).padStart(2,'0') + '-' +
      String(d.getDate()).padStart(2,'0');
    var opt = document.createElement('option');
    opt.value = value;
    opt.textContent = label;
    select.appendChild(opt);
  }
})();

// Build time dropdown slots
function buildTimeSlots(bookedTimes) {
  var select = document.getElementById('bTime');
  select.innerHTML = '<option value="">-- Select a time --</option>';
  HOUR_VALUES.forEach(function(val, i) {
    var opt = document.createElement('option');
    opt.value = val;
    if (bookedTimes.indexOf(val) !== -1) {
      opt.textContent = HOURS[i] + ' — Unavailable';
      opt.disabled = true;
      opt.style.color = '#aaa';
    } else {
      opt.textContent = HOURS[i];
    }
    select.appendChild(opt);
  });
  select.disabled = false;
}

// Fetch booked times when date changes
document.getElementById('bDate').addEventListener('change', function() {
  var date = this.value;
  if (!date) return;

  var timeSelect = document.getElementById('bTime');
  timeSelect.innerHTML = '<option>Loading...</option>';
  timeSelect.disabled = true;

  fetch(SCRIPT_URL + '?date=' + date)
    .then(function(res) { return res.json(); })
    .then(function(data) { buildTimeSlots(data.booked || []); })
    .catch(function() { buildTimeSlots([]); }); // fail open if fetch errors
});

// Form submit
