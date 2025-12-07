document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link, .navbar-nav .btn-outline-info");

    navLinks.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add("active");
        }

        link.addEventListener("click", () => {
            navLinks.forEach(nav => nav.classList.remove("active"));
            link.classList.add("active");
        });
    });
});