document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.querySelector('[x-on:click]');
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
        });
    }
});


