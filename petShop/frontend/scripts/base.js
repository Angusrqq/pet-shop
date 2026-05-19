// Automatically hide messages after 5 seconds (5000 milliseconds)
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.alert').forEach((el, i) => {
        const delay = 5000 + i * 80;
        setTimeout(() => {
            if (!el.isConnected) return;
            el.classList.add('dismissing');
            setTimeout(() => el.remove(), 400);
        }, delay);
    });
});

function showMessages(messages) {
    let container = document.querySelector('.alert-messages');
    if (!container) {
        container = document.createElement('div');
        container.className = 'alert-messages';
        document.body.appendChild(container);
    }

    messages.forEach((m, i) => {
        const div = document.createElement('div');
        div.className = `alert ${m.tags}`;
        div.innerHTML = `
            <span class="alert-icon"></span>
            <span class="alert-text">${m.message}</span>
            <button class="alert-close" onclick="this.parentElement.classList.add('dismissing'); setTimeout(() => this.parentElement.remove(), 400)">&#x2715;</button>
        `;
        container.appendChild(div);

        setTimeout(() => {
            if (!div.isConnected) return;
            div.classList.add('dismissing');
            setTimeout(() => div.remove(), 400);
        }, 5000 + i * 80);
    });
}

document.addEventListener('submit', function(e) {
    const form = e.target;
    if (!form.classList.contains('cart-form')) return;
    if (document.querySelector('.cart-wrapper')) return; // let cart page reload normally

    e.preventDefault();

    fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
    })
    .then(res => res.json())
    .then(data => {
        let badge = document.querySelector('.cart-badge');
        if (!badge) {
            badge = document.createElement('span');
            badge.className = 'cart-badge';
            document.querySelector('.cart-icon-wrapper').appendChild(badge);
        }
        badge.textContent = data.cart_count;
        badge.style.display = data.cart_count > 0 ? 'flex' : 'none';

        if (data.messages) showMessages(data.messages);
    });
});

// Adding to wishlist
document.addEventListener('click', function(e) {
    const btn = e.target.closest('.add-to-wishlist-btn');
    if (!btn) return;

    const productId = btn.dataset.productId;
    const form = new FormData();
    form.append('csrfmiddlewaretoken', document.cookie.match(/csrftoken=([^;]+)/)[1]);

    fetch(`/wishlist/toggle/${productId}/`, {
        method: 'POST',
        body: form,
    })
    .then(res => res.json())
    .then(data => {
        btn.classList.toggle('active', data.in_wishlist);
    });
});


// Eyes stuff
const T = {
    light: { br: 13, me: 11 },
    dark:  { br: 6,  me: 22 }
};

let theme = localStorage.getItem('theme') || 'light';
let lx, ly, lastSpeed = 0;

const eyeBtn = document.getElementById('eye-btn');
const eyeEl = document.querySelector('.eye');
const irisEl = document.querySelector('.iris');
const pupilEl = document.querySelector('.pupil');

let eyeRect = eyeBtn.getBoundingClientRect();
window.addEventListener('resize', () => eyeRect = eyeBtn.getBoundingClientRect());

function apply(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('theme', t);
    eyeEl.classList.toggle('cat', t === 'dark');
    pupilEl.style.width = '';
    pupilEl.style.height = '';
    pupilEl.style.borderRadius = '';
}

let searchInterval = null;
let searchStep = 0;
const MAX_STEPS = 8;
let closeTimeout = null;

function searchMove() {
    if (!searchInterval) return;

    const progress = searchStep / MAX_STEPS;
    
    const currentDilation = parseFloat(pupilEl.style.width);
    const maxDilation = theme === 'light' ? T.light.br + T.light.me : T.dark.br + T.dark.me;
    const moveIntensity = currentDilation / maxDilation;
    const range = 12 * moveIntensity * (1 - progress * 0.7);
    const rx = (Math.random() - 0.5) * 2 * range;
    const ry = (Math.random() - 0.5) * 2 * range;
    irisEl.style.transform = `translate(calc(-50% + ${rx}px), calc(-50% + ${ry}px))`;

    const delay = 200 + progress * 800;

    searchStep++;

    if (searchStep >= MAX_STEPS) {
        if (theme === 'light') {
            pupilEl.style.width        = T.light.br + 'px';
            pupilEl.style.height       = T.light.br + 'px';
        } else {
            pupilEl.style.width        = T.dark.br + 'px';
            pupilEl.style.height       = T.dark.me + 'px';
        }
        closeTimeout = setTimeout(() => {
            irisEl.style.transform = `translate(-50%, -50%)`;
            closeTimeout = setTimeout(() => eyeEl.classList.add('closed'), 300);
        }, 400);
        searchInterval = null;
        return;
    }

    searchInterval = setTimeout(searchMove, delay);
}

document.addEventListener('mouseout', (e) => {
    if (e.relatedTarget) return;
    searchStep = 0;
    searchInterval = setTimeout(searchMove, 200);
});

document.addEventListener('mouseover', (e) => {
    if (e.relatedTarget) return;
    clearTimeout(searchInterval);
    searchInterval = null;
    searchStep = 0;

    if (eyeEl.classList.contains('closed') || closeTimeout){
        clearTimeout(closeTimeout);
        closeTimeout = null;
        eyeEl.classList.remove('closed');
        eyeEl.classList.add('opening');
        setTimeout(() => eyeEl.classList.remove('opening'), 300);
    }

    irisEl.style.transform = `translate(-50%, -50%)`;
});

eyeBtn.addEventListener('click', () => {
    eyeEl.classList.add('blinking');

    setTimeout(() => {
        theme = theme === 'light' ? 'dark' : 'light';
        apply(theme);
    }, 140);

    setTimeout(() => {
        eyeEl.classList.remove('blinking');
    }, 280);
});

let pending = false;
let mouseX = 0, mouseY = 0;

document.addEventListener('mousemove', (e) => {
    const dx = e.clientX - (lx || e.clientX);
    const dy = e.clientY - (ly || e.clientY);
    const speed = Math.sqrt(dx*dx + dy*dy);
    lastSpeed = lastSpeed * 0.8 + speed * 0.2;
    lx = e.clientX; ly = e.clientY;
    mouseX = e.clientX; mouseY = e.clientY;

    if (pending) return; // already a frame queued
    pending = true;
    requestAnimationFrame(update);
});

function update() {
    pending = false;

    const ex = eyeRect.left + eyeRect.width / 2;
    const ey = eyeRect.top + eyeRect.height / 2;
    const edx = mouseX - ex;
    const edy = mouseY - ey;
    const dist = Math.sqrt(edx*edx + edy*edy);
    const ox = (edx / Math.max(dist, 1)) * Math.min(dist / 15, 8);
    const oy = (edy / Math.max(dist, 1)) * Math.min(dist / 15, 8);

    irisEl.style.transform  = `translate(calc(-50% + ${ox}px), calc(-50% + ${oy}px))`;

    if (theme === 'light') {
        const size = (T.light.br + Math.max(0, 1 - dist / 180) * T.light.me * 2).toFixed(1);
        pupilEl.style.width = size + 'px';
        pupilEl.style.height = size + 'px';
        pupilEl.style.borderRadius = '50%';
    } else {
        const intensity = Math.min(lastSpeed / 120, 1);
        const height = (T.dark.br + 8 + intensity * T.dark.me).toFixed(1);
        const width  = (6 + intensity * intensity * 30).toFixed(1);
        pupilEl.style.height       = height + 'px';
        pupilEl.style.width        = width  + 'px';
        pupilEl.style.borderRadius = '50%';
    }
}

apply(theme);