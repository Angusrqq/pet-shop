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