/**
 * CyberLearn CTF - Theme Switcher System
 * Manages Dark & Light modes with persistent preference.
 * Compliant with Content-Security-Policy: script-src 'self'
 */

(function () {
    "use strict";

    var THEME_KEY = "cyberlearn_theme";

    function getPreferredTheme() {
        var stored = localStorage.getItem(THEME_KEY);
        if (stored === "light" || stored === "dark") {
            return stored;
        }
        if (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches) {
            return "light";
        }
        return "dark";
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        var toggleBtn = document.getElementById("theme-toggle");
        if (toggleBtn) {
            var iconDark = toggleBtn.querySelector(".theme-icon-dark");
            var iconLight = toggleBtn.querySelector(".theme-icon-light");
            var themeText = toggleBtn.querySelector(".theme-label");

            if (theme === "light") {
                toggleBtn.setAttribute("aria-label", "Switch to Dark Mode");
                toggleBtn.setAttribute("title", "Switch to Dark Mode");
                if (iconDark) iconDark.style.display = "none";
                if (iconLight) iconLight.style.display = "inline-block";
                if (themeText) themeText.textContent = "Light";
            } else {
                toggleBtn.setAttribute("aria-label", "Switch to Light Mode");
                toggleBtn.setAttribute("title", "Switch to Light Mode");
                if (iconDark) iconDark.style.display = "inline-block";
                if (iconLight) iconLight.style.display = "none";
                if (themeText) themeText.textContent = "Dark";
            }
        }
    }

    // Apply immediately to prevent white/dark flash (FOUC)
    var initialTheme = getPreferredTheme();
    document.documentElement.setAttribute("data-theme", initialTheme);

    window.toggleTheme = function () {
        var current = document.documentElement.getAttribute("data-theme") || "dark";
        var next = (current === "dark") ? "light" : "dark";
        localStorage.setItem(THEME_KEY, next);
        applyTheme(next);
    };

    document.addEventListener("DOMContentLoaded", function () {
        applyTheme(document.documentElement.getAttribute("data-theme") || "dark");

        var toggleBtn = document.getElementById("theme-toggle");
        if (toggleBtn) {
            toggleBtn.addEventListener("click", function (e) {
                e.preventDefault();
                window.toggleTheme();
            });
        }
    });
})();
