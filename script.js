document.addEventListener("DOMContentLoaded", () => {
    const themeToggleBtn = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const htmlElement = document.documentElement;

    // 1. Persistent Theme Sync Engine
    const savedTheme = localStorage.getItem("portfolio-theme") || "light";
    htmlElement.setAttribute("data-theme", savedTheme);
    syncIconStyle(savedTheme);

    themeToggleBtn.addEventListener("click", () => {
        const activeTheme = htmlElement.getAttribute("data-theme");
        const alternateTheme = activeTheme === "dark" ? "light" : "dark";
        
        htmlElement.setAttribute("data-theme", alternateTheme);
        localStorage.setItem("portfolio-theme", alternateTheme);
        syncIconStyle(alternateTheme);
    });

    function syncIconStyle(themeState) {
        if (themeState === "dark") {
            themeIcon.className = "fas fa-sun";
        } else {
            themeIcon.className = "fas fa-moon";
        }
    }

    // 2. ScrollReveal Engine (Cleans transform blocks on load completion)
    if (typeof ScrollReveal !== 'undefined') {
        const isMobile = window.innerWidth < 768;

        const revealConfig = {
            origin: 'bottom',
            distance: isMobile ? '10px' : '30px', 
            duration: 900,
            delay: 100,
            reset: false,
            useDelay: 'onload',
            afterReveal: function (el) {
                el.style.transform = '';
                el.style.transition = '';
            }
        };

        ScrollReveal().reveal('.reveal-bottom', revealConfig);
        ScrollReveal().reveal('.reveal-card', {
            ...revealConfig,
            interval: 50
        });
    }
});