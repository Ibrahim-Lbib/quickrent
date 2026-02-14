     const toggleButtons = document.querySelectorAll('.toggle-btn');
        const priceElements = document.querySelectorAll('.price[data-monthly]');
        const periodElements = document.querySelectorAll('.price-period[data-monthly]');

        toggleButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Remove active class from all buttons
                toggleButtons.forEach(btn => {
                    btn.classList.remove('active');
                    btn.classList.add('inactive');
                });

                // Add active class to clicked button
                button.classList.add('active');
                button.classList.remove('inactive');

                // Get the billing type
                const billingType = button.getAttribute('data-billing');

                // Update prices
                priceElements.forEach(priceEl => {
                    const monthlyPrice = priceEl.getAttribute('data-monthly');
                    const annuallyPrice = priceEl.getAttribute('data-annually');
                    
                    if (billingType === 'monthly') {
                        priceEl.textContent = 'UGX ' + monthlyPrice;
                    } else {
                        priceEl.textContent = 'UGX ' + annuallyPrice;
                    }
                });

                // Update periods
                periodElements.forEach(periodEl => {
                    const monthlyPeriod = periodEl.getAttribute('data-monthly');
                    const annuallyPeriod = periodEl.getAttribute('data-annually');
                    
                    if (billingType === 'monthly') {
                        periodEl.textContent = monthlyPeriod;
                    } else {
                        periodEl.textContent = annuallyPeriod;
                    }
                });
            });
        });


// for the search section
// Dropdown functionality
function initializeDropdowns() {
    const dropdowns = ['location', 'price', 'property'];
    
    dropdowns.forEach(dropdownName => {
        const toggle = document.querySelector(`[data-dropdown="${dropdownName}"]`);
        const menu = document.getElementById(`${dropdownName}Menu`);
        const options = menu.querySelectorAll('.dropdown-option');
        
        if (!toggle || !menu) return;
        
        // Toggle menu on button click
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            
            // Close other dropdowns
            document.querySelectorAll('.dropdown-menu').forEach(m => {
                if (m !== menu) {
                    m.classList.remove('active');
                    m.previousElementSibling?.classList.remove('active');
                }
            });
            
            menu.classList.toggle('active');
            toggle.classList.toggle('active');
        });
        
        // Handle option selection
        options.forEach(option => {
            option.addEventListener('click', () => {
                // Remove selected from all options
                options.forEach(o => o.classList.remove('selected'));
                // Add selected to clicked option
                option.classList.add('selected');
                // Update button text
                toggle.querySelector('span').textContent = option.querySelector('span').textContent;
                // Close menu
                menu.classList.remove('active');
                toggle.classList.remove('active');
            });
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-dropdown')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.classList.remove('active');
                document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                    toggle.classList.remove('active');
                });
            });
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initializeDropdowns);