document.addEventListener('DOMContentLoaded', function () {
    const containers = document.querySelectorAll('.dropdown-login');
    if (!containers || containers.length === 0) return;

    function closeAll() {
        containers.forEach(c => {
            c.classList.remove('open');
            const t = c.querySelector('.dropdown-toggle');
            if (t) t.setAttribute('aria-expanded', 'false');
        });
    }

    // Click fuera cierra todos
    document.addEventListener('click', function (ev) {
        let clickedInsideAny = false;
        containers.forEach(c => { if (c.contains(ev.target)) clickedInsideAny = true; });
        if (!clickedInsideAny) closeAll();
    });

    // Escape cierra
    document.addEventListener('keydown', function (ev) {
        if (ev.key === 'Escape') closeAll();
    });

    containers.forEach(container => {
        const toggle = container.querySelector('.dropdown-toggle');
        const menu = container.querySelector('.dropdown-menu');
        if (!toggle) return;

        toggle.setAttribute('role', 'button');
        toggle.setAttribute('aria-haspopup', 'true');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.style.cursor = 'pointer';

        toggle.addEventListener('click', function (ev) {
            ev.preventDefault();
            const isOpen = container.classList.toggle('open');
            toggle.setAttribute('aria-expanded', String(isOpen));
            // cerrar otros dropdowns
            containers.forEach(c => { if (c !== container) c.classList.remove('open'); });
        });

        if (menu) {
            menu.addEventListener('click', function (ev) { ev.stopPropagation(); });
            // Cerrar al click en un enlace dentro del menú
            menu.querySelectorAll('a').forEach(a => {
                a.addEventListener('click', function () {
                    container.classList.remove('open');
                    toggle.setAttribute('aria-expanded', 'false');
                });
            });
        }
    });
});