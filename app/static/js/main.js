// ============================================================================
// Pricing Toggle (Monthly / Annually)
// ============================================================================
function initPricingToggle() {
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    const priceElements = document.querySelectorAll('[data-monthly].price');
    const periodElements = document.querySelectorAll('[data-monthly].price-period');

    if (!toggleButtons.length) return;

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Reset all buttons
            toggleButtons.forEach(btn => {
                btn.classList.remove('active');
                btn.classList.add('inactive');
            });

            // Activate clicked
            button.classList.add('active');
            button.classList.remove('inactive');

            const billingType = button.dataset.billing;

            // Update prices
            priceElements.forEach(el => {
                const value = billingType === 'monthly'
                    ? el.dataset.monthly
                    : el.dataset.annually;
                el.textContent = value ? `UGX ${value}` : 'UGX 0';
            });

            // Update periods
            periodElements.forEach(el => {
                const period = billingType === 'monthly'
                    ? el.dataset.monthly
                    : el.dataset.annually;
                el.textContent = period || '/month';
            });
        });
    });

    // Optional: trigger default (monthly)
    const defaultBtn = document.querySelector('.toggle-btn[data-billing="monthly"]');
    if (defaultBtn) defaultBtn.click();
}

// ============================================================================
// Custom Dropdowns (Location, Price, Property Type)
// ============================================================================
function initDropdowns() {
    const dropdowns = ['location', 'price', 'property'];

    dropdowns.forEach(name => {
        const toggle = document.querySelector(`[data-dropdown="${name}"]`);
        const menu = document.getElementById(`${name}Menu`);
        if (!toggle || !menu) return;

        const options = menu.querySelectorAll('.dropdown-option');

        // Toggle menu
        toggle.addEventListener('click', e => {
            e.stopPropagation();

            // Close others
            document.querySelectorAll('.dropdown-menu.active').forEach(m => {
                if (m !== menu) {
                    m.classList.remove('active');
                    m.previousElementSibling?.classList.remove('active');
                }
            });

            menu.classList.toggle('active');
            toggle.classList.toggle('active');
        });

        // Select option
        options.forEach(option => {
            option.addEventListener('click', () => {
                options.forEach(o => o.classList.remove('selected'));
                option.classList.add('selected');

                // Update visible text
                toggle.querySelector('span').textContent = option.querySelector('span')?.textContent || 'Select';

                // Optional: store real value somewhere (for form submission)
                // toggle.dataset.value = option.dataset.value;

                menu.classList.remove('active');
                toggle.classList.remove('active');
            });
        });
    });

    // Close all dropdowns on outside click
    document.addEventListener('click', e => {
        if (!e.target.closest('.search-dropdown')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => menu.classList.remove('active'));
            document.querySelectorAll('.dropdown-toggle').forEach(t => t.classList.remove('active'));
        }
    });
}

// ============================================================================
// Navbar Scroll Effect
// ============================================================================
function initNavbarScroll() {
    const header = document.getElementById('main-header');
    if (!header) return;

    let lastScrollY = window.scrollY;
    let ticking = false;

    const onScroll = () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const current = window.scrollY;

                if (current > 60) {
                    header.classList.add('shadow-md', 'py-1');
                    header.classList.remove('shadow-sm', 'py-0');
                } else {
                    header.classList.remove('shadow-md', 'py-1');
                    header.classList.add('shadow-sm', 'py-0');
                }

                ticking = false;
            });
            ticking = true;
        }
    };

    window.addEventListener('scroll', onScroll, { passive: true });
}

// ============================================================================
// Mobile Menu (open + close)
// ============================================================================
function initMobileMenu() {
    const openBtn = document.getElementById('mobile-menu-open');
    const dialog = document.getElementById('mobile-menu');

    if (!openBtn || !dialog) return;

    openBtn.addEventListener('click', () => {
        dialog.showModal();
    });

    // Close on backdrop click or Escape (native dialog behavior)
    // If you have a close button inside dialog, add:
    dialog.querySelector('[command="close"], [data-close], button[aria-label*="close"]')?.addEventListener('click', () => {
        dialog.close();
    });
}

// ============================================================================
// Initialize everything when DOM is ready
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    initPricingToggle();
    initDropdowns();
    initNavbarScroll();
    initMobileMenu();
});