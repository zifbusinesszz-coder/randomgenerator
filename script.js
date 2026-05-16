/* ==========================================
   WOOD'S WASTE - INTERACTIVE JS
   ========================================== */

document.addEventListener("DOMContentLoaded", () => {
    initMobileNav();
    initNavbarScroll();
    initSmoothScrolling();
    initScrollAnimations();
    initHeroParallax();
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

    // Close menu when clicking a link
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
   NAVBAR SCROLL EFFECT
   ========================================== */

function initNavbarScroll() {
    const navbar = document.querySelector(".navbar");

    if (!navbar) return;

    let lastScroll = 0;

    window.addEventListener("scroll", () => {
        const currentScroll = window.pageYOffset;

        // Add shadow when scrolling
        if (currentScroll > 50) {
            navbar.style.boxShadow = "0 10px 30px rgba(0,0,0,0.08)";
            navbar.style.background = "rgba(255,255,255,0.98)";
        } else {
            navbar.style.boxShadow = "none";
            navbar.style.background = "rgba(255,255,255,0.95)";
        }

        lastScroll = currentScroll;
    });
}

/* ==========================================
   SMOOTH SCROLLING (enhanced)
   ========================================== */

function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            const targetId = this.getAttribute("href");
            const target = document.querySelector(targetId);

            if (!target) return;

            e.preventDefault();

            window.scrollTo({
                top: target.offsetTop - 70,
                behavior: "smooth"
            });
        });
    });
}

/* ==========================================
   SCROLL ANIMATIONS (Intersection Observer)
   ========================================== */

function initScrollAnimations() {
    const elements = document.querySelectorAll(
        ".service-card, .section-header, .process-step, .value-item, .about-content, .about-visual"
    );

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = "1";
                    entry.target.style.transform = "translateY(0)";
                }
            });
        },
        {
            threshold: 0.15
        }
    );

    elements.forEach(el => {
        el.style.opacity = "0";
        el.style.transform = "translateY(30px)";
        el.style.transition = "all 0.6s ease-out";
        observer.observe(el);
    });
}

/* ==========================================
   HERO PARALLAX EFFECT
   ========================================== */

function initHeroParallax() {
    const orbs = document.querySelectorAll(".gradient-orb");
    const floatingCards = document.querySelectorAll(".floating-card");

    window.addEventListener("scroll", () => {
        const scrollY = window.scrollY;

        // Move background orbs
        orbs.forEach((orb, index) => {
            const speed = index === 0 ? 0.2 : 0.15;
            orb.style.transform = `translateY(${scrollY * speed}px)`;
        });

        // Slight floating card movement
        floatingCards.forEach((card, index) => {
            const speed = 0.05 + index * 0.02;
            card.style.transform = `translateY(${scrollY * speed}px)`;
        });
    });
}

/* ==========================================
   FORM ENHANCEMENTS
   ========================================== */

function initFormEnhancements() {
    const form = document.querySelector(".quote-form");

    if (!form) return;

    form.addEventListener("submit", (e) => {
        const button = form.querySelector("button[type='submit']");
        if (!button) return;

        button.innerText = "Sending...";
        button.disabled = true;

        // Let Formspree handle submission
        setTimeout(() => {
            button.innerText = "Sent!";
            button.style.background = "#10b981";
        }, 1200);
    });

    // Input focus effects
    document.querySelectorAll("input, textarea").forEach(input => {
        input.addEventListener("focus", () => {
            input.parentElement.classList.add("focused");
        });

        input.addEventListener("blur", () => {
            input.parentElement.classList.remove("focused");
        });
    });
}

/* ==========================================
   COUNTER ANIMATIONS (hero stats)
   ========================================== */

function initCounterAnimations() {
    const counters = document.querySelectorAll(".stat-number");

    const animateCounter = (el) => {
        const target = el.innerText.replace(/\D/g, "");
        const suffix = el.innerText.replace(/[0-9]/g, "");
        let count = 0;
        const speed = 30;

        const update = () => {
            if (count < target) {
                count++;
                el.innerText = count + suffix;
                setTimeout(update, speed);
            } else {
                el.innerText = target + suffix;
            }
        };

        update();
    };

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.6 }
    );

    counters.forEach(counter => observer.observe(counter));
}

/* ==========================================
   EXTRA POLISH: BUTTON RIPPLE EFFECT
   ========================================== */

document.addEventListener("click", (e) => {
    const btn = e.target.closest(".btn");
    if (!btn) return;

    const ripple = document.createElement("span");
    ripple.classList.add("ripple");

    const rect = btn.getBoundingClientRect();
    ripple.style.left = `${e.clientX - rect.left}px`;
    ripple.style.top = `${e.clientY - rect.top}px`;

    btn.appendChild(ripple);

    setTimeout(() => ripple.remove(), 600);
});
