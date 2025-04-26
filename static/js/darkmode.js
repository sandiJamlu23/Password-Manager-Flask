document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('dark-mode-toggle');
    const body = document.body;

    // Check localStorage for dark mode preference
    if (localStorage.getItem('dark-mode') === 'enabled') {
        body.classList.add('dark-mode');
        toggleButton.textContent = '☀️ Light Mode';
    }

    toggleButton.addEventListener('click', function () {
        if (body.classList.contains('dark-mode')) {
            body.classList.remove('dark-mode');
            localStorage.setItem('dark-mode', 'disabled');
            toggleButton.textContent = '🌙 Dark Mode';
        } else {
            body.classList.add('dark-mode');
            localStorage.setItem('dark-mode', 'enabled');
            toggleButton.textContent = '☀️ Light Mode';
        }
    });
});