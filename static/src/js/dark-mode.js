const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
const themeToggleAutoIcon = document.getElementById('theme-toggle-auto-icon');

// Change the icons inside the button based on previous settings
if ('color-theme' in localStorage) {
    if (localStorage.getItem('color-theme') === 'dark') {
        themeToggleDarkIcon.classList.remove('hidden');
    } else if (localStorage.getItem('color-theme') === 'light') {
        themeToggleLightIcon.classList.remove('hidden');
    }
} else {
    themeToggleAutoIcon.classList.remove('hidden');
}

const themeToggleBtn = document.getElementById('theme-toggle');

let event = new Event('dark-mode');

themeToggleBtn.addEventListener('click', function () {

    // if set via local storage previously
    if (localStorage.getItem('color-theme')) {
        if (localStorage.getItem('color-theme') === 'dark') {
            // dark -> light
            // Icons
            themeToggleDarkIcon.classList.add('hidden');
            themeToggleLightIcon.classList.remove('hidden');
            themeToggleAutoIcon.classList.add('hidden');
            // Class
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else if (localStorage.getItem('color-theme') === 'light') {
            // light -> auto
            // Icons
            themeToggleDarkIcon.classList.add('hidden');
            themeToggleLightIcon.classList.add('hidden');
            themeToggleAutoIcon.classList.remove('hidden');
            // Class
            // check what the color scheme prefers
            if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
            localStorage.removeItem('color-theme');
        } else {
            // auto -> dark
            // Icons
            themeToggleDarkIcon.classList.remove('hidden');
            themeToggleLightIcon.classList.add('hidden');
            themeToggleAutoIcon.classList.add('hidden');
            // Class
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    } else {
        // Set: auto -> dark
        themeToggleDarkIcon.classList.remove('hidden');
        themeToggleLightIcon.classList.add('hidden');
        themeToggleAutoIcon.classList.add('hidden');
        // Class
        document.documentElement.classList.add('dark');
        localStorage.setItem('color-theme', 'dark');
    }

    document.dispatchEvent(event);
});

// Listen for system color scheme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (!('color-theme' in localStorage) || localStorage.getItem('color-theme') === 'auto') {
        if (e.matches) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }
});
