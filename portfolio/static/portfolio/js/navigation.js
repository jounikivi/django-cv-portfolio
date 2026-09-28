// Ilman JavaScriptiä navigaation linkit pysyvät näkyvissä.
(() => {
    const header = document.querySelector('.site-header');
    const button = header?.querySelector('.menu-toggle');
    const navigation = document.getElementById('site-navigation');
    if (!header || !button || !navigation) return;

    const mobile = window.matchMedia('(max-width: 48rem)');
    const label = button.querySelector('.menu-label');
    const icon = button.querySelector('.menu-icon');

    function setOpen(open) {
        button.setAttribute('aria-expanded', String(open));
        label.textContent = open ? 'Sulje' : 'Valikko';
        icon.textContent = open ? '×' : '☰';
    }

    button.hidden = false;
    header.classList.add('navigation-ready');
    button.addEventListener('click', () => {
        setOpen(button.getAttribute('aria-expanded') !== 'true');
    });

    navigation.addEventListener('click', (event) => {
        const link = event.target.closest('a');
        if (!mobile.matches || !link) return;
        setOpen(false);
        const target = document.getElementById(link.hash.slice(1));
        if (target) {
            target.setAttribute('tabindex', '-1');
            target.focus({ preventScroll: true });
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && mobile.matches && button.getAttribute('aria-expanded') === 'true') {
            setOpen(false);
            button.focus();
        }
    });

    mobile.addEventListener('change', () => {
        const active = document.activeElement;
        setOpen(false);
        if (mobile.matches && navigation.contains(active)) button.focus();
        else if (!mobile.matches && active === button) navigation.querySelector('a')?.focus();
    });
})();
