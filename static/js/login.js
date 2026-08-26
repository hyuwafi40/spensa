const loginForm = document.getElementById('loginForm');
const loadingOverlay = document.createElement('div');
loadingOverlay.className = 'login-loading-overlay';
loadingOverlay.innerHTML = `
    <div class="login-loading-box">
        <div class="login-loading-spinner"></div>
        <div class="login-loading-text">Memuat <span class="login-loading-percent">0%</span></div>
        <div class="login-loading-progress-track">
            <div class="login-loading-progress-fill"></div>
        </div>
    </div>
`;
document.body.appendChild(loadingOverlay);

const loadingPercent = loadingOverlay.querySelector('.login-loading-percent');
const loadingFill = loadingOverlay.querySelector('.login-loading-progress-fill');
let loadingInterval = null;
let loadingFallbackTimeout = null;

function setLoadingProgress(value) {
    const percent = Math.min(Math.max(value, 0), 100);
    loadingPercent.textContent = `${Math.floor(percent)}%`;
    loadingFill.style.width = `${percent}%`;
}

function showLoading() {
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
    if (loadingInterval) clearInterval(loadingInterval);
    if (loadingFallbackTimeout) clearTimeout(loadingFallbackTimeout);
    setLoadingProgress(100);
    setTimeout(() => {
        loadingOverlay.classList.remove('show');
        setLoadingProgress(0);
    }, 180);
}

if (loginForm) {
    loginForm.addEventListener('submit', () => {
        showLoading();
    });
}

window.addEventListener('load', hideLoading);