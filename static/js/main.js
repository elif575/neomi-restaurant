/* Neomi · נעמי — site behaviour
 *
 * User-facing strings come from data-* attributes set by the templates, so
 * this file stays language-agnostic (the site runs in Hebrew and French).
 */

(function () {
    'use strict';

    const CURRENCY = '₪';

    function money(value) {
        // Shekel prices on the menu are whole numbers.
        return CURRENCY + ' ' + Math.round(value);
    }

    /* ── Navbar: solidify once scrolled off the hero ───────────── */

    const nav = document.getElementById('mainNav');
    if (nav) {
        const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 60);
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    /* ── Hero video: opt in rather than always ─────────────────── */

    const heroVideo = document.querySelector('.hero-video[data-src]');
    if (heroVideo) {
        const conn = navigator.connection || {};
        const slow = conn.saveData === true ||
            ['slow-2g', '2g', '3g'].includes(conn.effectiveType);
        const wideEnough = window.innerWidth >= 768;
        const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (wideEnough && !slow && !reduceMotion) {
            heroVideo.src = heroVideo.dataset.src;
            heroVideo.load();
            // Autoplay can still be refused; the poster stays visible if so.
            const attempt = heroVideo.play();
            if (attempt && attempt.catch) attempt.catch(() => {});
        }
    }

    /* ── Scroll reveal ─────────────────────────────────────────── */

    const revealTargets = document.querySelectorAll('.reveal');
    if (revealTargets.length) {
        if (!('IntersectionObserver' in window)) {
            revealTargets.forEach((el) => el.classList.add('is-visible'));
        } else {
            const io = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        io.unobserve(entry.target);
                    }
                });
            }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
            revealTargets.forEach((el) => io.observe(el));
        }
    }

    /* ── Gallery: filter tabs, lightbox, click-to-play video ───── */

    const grid = document.getElementById('galleryGrid');
    if (grid) {
        const tiles = Array.from(grid.querySelectorAll('.gallery-item'));
        const videoTiles = Array.from(grid.querySelectorAll('.gallery-video'));

        const tabs = Array.from(document.querySelectorAll('.gallery-tab'));

        function applyFilter(filter) {
            [...tiles, ...videoTiles].forEach((tile) => {
                tile.hidden = !(filter === 'all' || tile.dataset.group === filter);
            });
        }

        tabs.forEach((tab) => {
            tab.addEventListener('click', () => {
                tabs.forEach((t) => t.classList.remove('is-active'));
                tab.classList.add('is-active');
                applyFilter(tab.dataset.filter);
            });
        });

        // The gallery opens on whichever tab the template marked is-active,
        // so that choice lives in the markup rather than being duplicated
        // here. Filtering on load is deliberate: without it the active tab
        // would say one thing and the grid show another.
        //
        // Nothing is hidden until this runs, so a visitor with JS disabled
        // still gets the whole gallery instead of an empty page.
        const startTab = tabs.find((t) => t.classList.contains('is-active'));
        if (startTab) applyFilter(startTab.dataset.filter);

        // Poster-only until asked: keeps the 42 MB clip off the initial load.
        videoTiles.forEach((tile) => {
            const video = tile.querySelector('video');
            const btn = tile.querySelector('.video-play-btn');
            if (!video || !btn) return;
            btn.addEventListener('click', () => {
                video.play();
                btn.hidden = true;
            });
            video.addEventListener('pause', () => { btn.hidden = false; });
        });

        // Lightbox over the visible tiles only, so arrows follow the filter.
        const lightbox = document.getElementById('lightbox');
        const lightboxImg = document.getElementById('lightboxImg');
        let index = 0;

        function visibleTiles() {
            return tiles.filter((t) => !t.hidden);
        }

        function show(i) {
            const list = visibleTiles();
            if (!list.length) return;
            index = (i + list.length) % list.length;
            const tile = list[index];
            lightboxImg.src = tile.dataset.full;
            const img = tile.querySelector('img');
            lightboxImg.alt = img ? img.alt : '';
        }

        function open(tile) {
            index = visibleTiles().indexOf(tile);
            show(index);
            lightbox.hidden = false;
            document.body.style.overflow = 'hidden';
        }

        function close() {
            lightbox.hidden = true;
            lightboxImg.src = '';
            document.body.style.overflow = '';
        }

        tiles.forEach((tile) => tile.addEventListener('click', () => open(tile)));

        if (lightbox) {
            lightbox.querySelector('.lightbox-close').addEventListener('click', close);
            lightbox.querySelector('.lightbox-prev').addEventListener('click', (e) => {
                e.stopPropagation();
                show(index - 1);
            });
            lightbox.querySelector('.lightbox-next').addEventListener('click', (e) => {
                e.stopPropagation();
                show(index + 1);
            });
            lightbox.addEventListener('click', (e) => {
                if (e.target === lightbox) close();
            });
            document.addEventListener('keydown', (e) => {
                if (lightbox.hidden) return;
                if (e.key === 'Escape') close();
                if (e.key === 'ArrowRight') show(index + 1);
                if (e.key === 'ArrowLeft') show(index - 1);
            });
        }
    }

    /* ── Ordering cart ─────────────────────────────────────────── */

    const cartRoot = document.getElementById('cart-items');
    if (!cartRoot) return;

    const cart = {};
    const strings = cartRoot.dataset;

    function render() {
        const summary = document.getElementById('cart-summary');
        const checkout = document.getElementById('checkout-form');
        const totalEl = document.getElementById('cart-total');
        const items = Object.values(cart);

        if (!items.length) {
            cartRoot.innerHTML = '<p class="cart-empty">' + (strings.empty || '') + '</p>';
            if (summary) summary.hidden = true;
            if (checkout) checkout.hidden = true;
            return;
        }

        cartRoot.textContent = '';
        let total = 0;

        items.forEach((item) => {
            total += item.price * item.quantity;

            const row = document.createElement('div');
            row.className = 'cart-item';

            const label = document.createElement('div');
            const name = document.createElement('span');
            name.className = 'cart-item-name';
            // textContent, not innerHTML: dish names come from the database.
            name.textContent = item.name;
            const unit = document.createElement('small');
            unit.textContent = money(item.price);
            label.append(name, document.createElement('br'), unit);

            const qty = document.createElement('div');
            qty.className = 'cart-item-qty';

            const minus = document.createElement('button');
            minus.type = 'button';
            minus.textContent = '−';
            minus.addEventListener('click', () => change(item.id, -1));

            const count = document.createElement('span');
            count.textContent = item.quantity;

            const plus = document.createElement('button');
            plus.type = 'button';
            plus.textContent = '+';
            plus.addEventListener('click', () => change(item.id, 1));

            const sub = document.createElement('strong');
            sub.textContent = money(item.price * item.quantity);

            qty.append(minus, count, plus, sub);
            row.append(label, qty);
            cartRoot.append(row);
        });

        if (totalEl) totalEl.textContent = money(total);
        if (summary) summary.hidden = false;
        if (checkout) checkout.hidden = false;
    }

    function change(id, delta) {
        const item = cart[id];
        if (!item) return;
        item.quantity += delta;
        if (item.quantity <= 0) delete cart[id];
        render();
    }

    document.querySelectorAll('[data-add-to-cart]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            const price = parseFloat(btn.dataset.price);
            if (cart[id]) {
                cart[id].quantity += 1;
            } else {
                cart[id] = { id: Number(id), name: btn.dataset.name, price, quantity: 1 };
            }
            render();
        });
    });

    const orderType = document.getElementById('order_type');
    if (orderType) {
        const toggle = () => {
            const group = document.getElementById('address-group');
            if (group) group.hidden = orderType.value !== 'delivery';
        };
        orderType.addEventListener('change', toggle);
        toggle();
    }

    const submitBtn = document.getElementById('submit-order');
    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            const items = Object.values(cart);
            if (!items.length) return;

            const name = document.getElementById('customer_name').value.trim();
            const phone = document.getElementById('phone').value.trim();
            if (!name || !phone) {
                alert(strings.required || '');
                return;
            }

            const addressEl = document.getElementById('address');
            submitBtn.disabled = true;

            fetch('/order', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    customer_name: name,
                    phone: phone,
                    order_type: orderType ? orderType.value : 'pickup',
                    address: addressEl ? addressEl.value.trim() : '',
                    notes: document.getElementById('notes').value.trim(),
                    items: items.map((i) => ({ id: i.id, quantity: i.quantity })),
                }),
            })
                .then((res) => {
                    if (!res.ok) throw new Error('Order failed');
                    return res.json();
                })
                .then((data) => {
                    window.location.href = '/order/confirmation/' + data.order_id;
                })
                .catch((err) => {
                    submitBtn.disabled = false;
                    alert(strings.failed || '');
                    console.error(err);
                });
        });
    }

    render();
})();
