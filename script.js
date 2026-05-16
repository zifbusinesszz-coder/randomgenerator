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

    // Close on link click
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", () => {
            navLinks.classList.remove("mobile-open");
            hamburger.classList.remove("active");
        });
    });

    // Close on outside click
    document.addEventListener("click", (e) => {
        if (!navLinks.contains(e.target) && !hamburger.contains(e.target)) {
            navLinks.classList.remove("mobile-open");
            hamburger.classList.remove("active");
        }
    });
}

/* ==========================================
   NAVBAR (clean + stable)
   ========================================== */

function initNavbarScroll() {
    const navbar = document.querySelector(".navbar");
    if (!navbar) return;

    window.addEventListener("scroll", () => {
        if (window.scrollY > 30) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });
}

/* ==========================================
   SMOOTH SCROLL (anchor links)
   ========================================== */

function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", (e) => {
            const target = document.querySelector(anchor.getAttribute("href"));
            if (!target) return;

            e.preventDefault();

            window.scrollTo({
                top: target.offsetTop - 80,
                behavior: "smooth"
            });
        });
    });
}

/* ==========================================
   SCROLL REVEAL (SAFE + NON-BREAKING)
   ========================================== */

function initScrollReveal() {
    const elements = document.querySelectorAll(
        ".service-card, .section-header, .process-step, .value-item, .about-content, .about-visual"
    );

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("in-view");
            }
        });
    }, {
        threshold: 0.12
    });

    elements.forEach(el => observer.observe(el));
}

/* ==========================================
   FORM UX (conversion focused, no bugs)
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
   COUNTER ANIMATION (safe + smooth)
   ========================================== */

function initCounterAnimations() {
    const counters = document.querySelectorAll(".stat-number");

    const animate = (el) => {
        const raw = el.innerText.replace(/\D/g, "");
        const target = parseInt(raw);

        if (!target) return;

        let count = 0;
        const step = Math.max(1, Math.floor(target / 60));

        const update = () => {
            count += step;

            if (count >= target) {
                el.innerText = el.innerText.includes("+")
                    ? target + "+"
                    : target;
            } else {
                el.innerText = count;
                requestAnimationFrame(update);
            }
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

    counters.forEach(c => observer.observe(c));
}
