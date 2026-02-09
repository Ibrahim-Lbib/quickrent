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