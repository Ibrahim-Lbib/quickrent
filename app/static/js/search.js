const searchInput = document.getElementById('searchInput');
        const shortcutLabel = document.getElementById('shortcutLabel');

        // Detect OS and set appropriate keyboard shortcut
        const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
        shortcutLabel.textContent = isMac ? '⌘K' : 'Ctrl+K';

        // Handle keyboard shortcut
        document.addEventListener('keydown', (e) => {
            // Check for Cmd+K (Mac) or Ctrl+K (Windows/Linux)
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                searchInput.focus();
                shortcutLabel.classList.add('active');
            }
        });

        // Remove active state when focus is lost
        searchInput.addEventListener('blur', () => {
            shortcutLabel.classList.remove('active');
        });

        // Also handle keyup to remove active state
        document.addEventListener('keyup', (e) => {
            if (e.key === 'Meta' || e.key === 'Control') {
                shortcutLabel.classList.remove('active');
            }
        });