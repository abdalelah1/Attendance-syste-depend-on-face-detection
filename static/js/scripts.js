document.addEventListener('DOMContentLoaded', function() {
    const toggleSidebar = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');
    const submenuToggles = document.querySelectorAll('.has-submenu > a');

    toggleSidebar.addEventListener('click', function() {
        sidebar.classList.toggle('closed');
    });

    submenuToggles.forEach(toggle => {
        toggle.addEventListener('click', function(event) {
            if (sidebar.classList.contains('closed')) {
                // منع الفتح إذا كان الشريط الجانبي مغلقًا
                event.preventDefault();
            } else {
                const submenu = toggle.nextElementSibling;
                submenu.classList.toggle('open');
            }
        });
    });
});
function confirmLogout() {
    if (confirm("Are you sure you want to log out?")) {
        window.location.href = "{% url 'logout' %}";
    }
}
