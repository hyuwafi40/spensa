const mainElement = document.querySelector('main');

let loadingOverlay = null;
let loadingPercent = null;
let loadingFill = null;
let loadingInterval = null;
let loadingFallbackTimeout = null;

if (mainElement) {
    loadingOverlay = document.createElement('div');
    loadingOverlay.className = 'loading-overlay';
    loadingOverlay.innerHTML = `
        <div class="loading-box">
            <div class="loading-spinner"></div>
            <div class="loading-text">Memuat <span class="loading-percent">0%</span></div>
            <div class="loading-progress-track">
                <div class="loading-progress-fill"></div>
            </div>
        </div>
    `;
    mainElement.appendChild(loadingOverlay);
    loadingPercent = loadingOverlay.querySelector('.loading-percent');
    loadingFill = loadingOverlay.querySelector('.loading-progress-fill');
}

function setLoadingProgress(value) {
    if (!loadingPercent || !loadingFill) return;
    const percent = Math.min(Math.max(value, 0), 100);
    loadingPercent.textContent = `${Math.floor(percent)}%`;
    loadingFill.style.width = `${percent}%`;
}

function showLoading() {
    if (!loadingOverlay || !loadingPercent || !loadingFill) return;
    if (loadingInterval) clearInterval(loadingInterval);
    if (loadingFallbackTimeout) clearTimeout(loadingFallbackTimeout);
    loadingOverlay.classList.add('show');
    setLoadingProgress(0);
    let progress = 0;
    loadingInterval = setInterval(() => {
        progress += Math.random() * 20 + 5;
        if (progress >= 90) {
            progress = 90;
            clearInterval(loadingInterval);
        }
        setLoadingProgress(progress);
    }, 60);

    loadingFallbackTimeout = setTimeout(() => {
        hideLoading();
    }, 3000);
}

function hideLoading() {
    if (!loadingOverlay || !loadingPercent || !loadingFill) return;
    if (loadingInterval) clearInterval(loadingInterval);
    if (loadingFallbackTimeout) clearTimeout(loadingFallbackTimeout);
    setLoadingProgress(100);
    setTimeout(() => {
        loadingOverlay.classList.remove('show');
        setLoadingProgress(0);
    }, 180);
}

document.addEventListener('DOMContentLoaded', () => {
    showLoading();
    window.addEventListener('load', () => {
        hideLoading();
    });
});

window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
        hideLoading();
    }
});

document.addEventListener('click', (e) => {
    const link = e.target.closest('a[href]');
    if (!link) return;
    const href = link.getAttribute('href');
    if (
        href &&
        href !== '#' &&
        !href.startsWith('javascript:') &&
        link.target !== '_blank' &&
        link.rel !== 'noopener'
    ) {
        showLoading();
    }
});

document.addEventListener('submit', (e) => {
    const form = e.target;
    if (form.tagName === 'FORM') {
        showLoading();
    }
});