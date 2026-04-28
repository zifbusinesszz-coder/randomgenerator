/* ==========================================
   WOOD'S WASTE - INTERACTIVE FEATURES
   ========================================== */

// Smooth scroll and navbar background
document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.navbar');
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    
    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = '0 0 0 rgba(0, 0, 0, 0)';
        }
    });

    // Mobile menu toggle
    if (hamburger) {
        hamburger.addEventListener('click', (e) => {
            e.stopPropagation();
            hamburger.classList.toggle('active');
            if (navLinks) {
                navLinks.classList.toggle('mobile-open');
            }
        });
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (hamburger && navLinks) {
            if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
                hamburger.classList.remove('active');
                navLinks.classList.remove('mobile-open');
            }
        }
    });

    // Close mobile menu on link click
    const navItems = document.querySelectorAll('.nav-links a');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            if (hamburger) hamburger.classList.remove('active');
            if (navLinks) navLinks.classList.remove('mobile-open');
        });
    });

    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards';
            }
        });
    }, observerOptions);

    // Observe elements
    const animateElements = document.querySelectorAll('.service-card, .process-step, .value-item');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });

    // Form handling
    const form = document.querySelector('.quote-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            const button = form.querySelector('button');
            const originalText = button.textContent;
            button.textContent = 'Sending...';
            button.disabled = true;

            // Simulate form submission with visual feedback
            setTimeout(() => {
                button.textContent = 'Quote Sent! 🎉';
                button.style.background = '#10b981';
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.disabled = false;
                    button.style.background = '';
                }, 3000);
            }, 500);
        });
    }

    // Button hover effects with ripple
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', (e) => {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.width = '0';
            ripple.style.height = '0';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.pointerEvents = 'none';
            ripple.style.animation = 'ripple 0.6s ease-out';

            button.style.position = 'relative';
            button.style.overflow = 'hidden';
            button.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Counter animation for stats
    const stats = document.querySelectorAll('.stat-number');
    const countUp = (element) => {
        const originalText = element.textContent.trim();
        
        // Only animate if it's a pure number (with optional + or %)
        const pureNumberMatch = originalText.match(/^(\d+)([\+%]?)$/);
        
        if (!pureNumberMatch) return; // Skip if not a pure number

        const target = parseInt(pureNumberMatch[1]);
        const suffix = pureNumberMatch[2] || '';
        let current = 0;
        const increment = Math.ceil(target / 30);
        
        const counter = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(counter);
            }
            element.textContent = current + suffix;
        }, 30);
    };

    const statObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                countUp(entry.target);
                statObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    stats.forEach(stat => {
        statObserver.observe(stat);
    });

    // Parallax effect for hero background
    const heroBackground = document.querySelector('.hero-background');
    if (heroBackground) {
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
            heroBackground.style.transform = `translateY(${scrollY * 0.5}px)`;
        });
    }

    // Add ripple animation to stylesheet
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            from {
                width: 0;
                height: 0;
                opacity: 1;
            }
            to {
                width: 300px;
                height: 300px;
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});

// Smooth scroll behavior for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const offset = 80; // navbar height
                const targetPosition = target.offsetTop - offset;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Service card hover effect enhancement
const serviceCards = document.querySelectorAll('.service-card');
serviceCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.boxShadow = '0 20px 50px rgba(14, 168, 84, 0.25)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.08)';
    });
});

// Add animation on scroll
function handleIntersection(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
        }
    });
}

const animationObserver = new IntersectionObserver(handleIntersection, {
    threshold: 0.1
});

// Observe all animated elements
document.querySelectorAll('[class*="animate"]').forEach(el => {
    animationObserver.observe(el);
});

// Cursor effect (optional - adds tracking dot to follow cursor on hero)
const heroSection = document.querySelector('.hero');
if (heroSection) {
    heroSection.addEventListener('mousemove', (e) => {
        const x = e.clientX;
        const y = e.clientY;
        
        // Create subtle light effect (commented out - uncomment if desired)
        // const light = document.createElement('div');
        // light.style.position = 'fixed';
        // light.style.left = x + 'px';
        // light.style.top = y + 'px';
        // light.style.width = '100px';
        // light.style.height = '100px';
        // light.style.borderRadius = '50%';
        // light.style.background = 'radial-gradient(circle, rgba(14, 168, 84, 0.2), transparent)';
        // light.style.pointerEvents = 'none';
        // light.style.filter = 'blur(20px)';
        // light.style.zIndex = '-1';
        // document.body.appendChild(light);
    });
}

// Add loading animation for images
const images = document.querySelectorAll('img');
images.forEach(img => {
    img.addEventListener('load', function() {
        this.style.animation = 'fadeInUp 0.8s ease-out';
    });
});

// Call tracking
const callButtons = document.querySelectorAll('[href^="tel:"]');
callButtons.forEach(button => {
    button.addEventListener('click', function(e) {
        // Track the call (optional analytics)
        if (typeof gtag !== 'undefined') {
            gtag('event', 'phone_click', {
                'phone_number': this.href.replace('tel:', '')
            });
        }
    });
});

// Form field focus effects
const formInputs = document.querySelectorAll('.form-group input, .form-group textarea');
formInputs.forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
    });
    
    input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// Dynamic year in footer
const year = new Date().getFullYear();
const copyrightEl = document.querySelector('.footer-bottom p');
if (copyrightEl) {
    copyrightEl.textContent = copyrightEl.textContent.replace(/\d{4}/, year);
}

// Mobile responsiveness enhancements
const checkMobileMenu = () => {
    const navLinks = document.querySelector('.nav-links');
    const hamburger = document.querySelector('.hamburger');
    
    if (window.innerWidth > 768) {
        if (navLinks) navLinks.classList.remove('mobile-open');
        if (hamburger) hamburger.classList.remove('active');
    }
};

window.addEventListener('resize', checkMobileMenu);

// Performance optimization: defer non-critical animations on slower devices
const preferReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (preferReducedMotion) {
    document.documentElement.style.setProperty('--transition-speed', '0.1s');
}

// Add page visibility handling
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        document.body.style.animation = 'none';
    } else {
        // Restore animations
        document.body.style.animation = '';
    }
});

console.log('🌲 Wood\'s Waste - Premium Site Loaded ✨');
