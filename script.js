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
