document.addEventListener('DOMContentLoaded', () => {
    // Dark mode toggle functionality
    const darkModeToggle = document.querySelector('[data-dark-mode-toggle]');
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
        });
    }

    // Optional: Add CSRF token to AJAX requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');
    
    // Attach CSRF token to fetch requests
    fetch.prototype.originalFetch = fetch.prototype.fetch;
    fetch.prototype.fetch = function(url, options = {}) {
        options.headers = {
            ...options.headers,
            'X-CSRFToken': csrftoken
        };
        return this.originalFetch(url, options);
    };
});