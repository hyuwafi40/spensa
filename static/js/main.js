const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const profileToggleBtn = document.getElementById('profileToggleBtn');
const profileDropdownMenu = document.getElementById('profileDropdownMenu');
const toastArea = document.getElementById('toastArea');

if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });
}

if (profileToggleBtn && profileDropdownMenu) {
    profileToggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        profileDropdownMenu.classList.toggle('show');
    });
}

document.addEventListener('click', (e) => {
    if (sidebar && sidebarToggle && window.innerWidth < 1024 && !sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
        sidebar.classList.remove('active');
    }
    if (profileDropdownMenu && profileToggleBtn && !profileDropdownMenu.contains(e.target) && !profileToggleBtn.contains(e.target)) {
        profileDropdownMenu.classList.remove('show');
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        if (sidebar && sidebar.classList.contains('active')) {
            sidebar.classList.remove('active');
        }
        if (profileDropdownMenu && profileDropdownMenu.classList.contains('show')) {
            profileDropdownMenu.classList.remove('show');
        }
    }
});

if (sidebar) {
    const menuItems = sidebar.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            if (window.innerWidth < 1024) {
                sidebar.classList.remove('active');
            }
        });
    });
}

let toastLock = false;

function spawnToast(title, message, type = 'success') {
    if (!toastArea) return;
    if (toastLock) return;
    toastLock = true;
    setTimeout(() => { toastLock = false; }, 350);

    const existingToasts = toastArea.querySelectorAll('.toast-box');
    if (existingToasts.length >= 2) {
        existingToasts[0].classList.add('hiding');
        setTimeout(() => existingToasts[0].remove(), 300);
    }

    const toast = document.createElement('div');
    toast.className = 'toast-box';

    let iconClass = 'fa-circle-check';
    if (type === 'warning') { iconClass = 'fa-triangle-exclamation'; }
    if (type === 'error') { iconClass = 'fa-circle-xmark'; }
    if (type === 'info') { iconClass = 'fa-circle-info'; }

    toast.classList.add(`toast-${type}`);

    toast.innerHTML = `
        <div class="toast-head">
            <span><i class="fa-solid ${iconClass}"></i> ${title}</span>
            <i class="fa-solid fa-xmark toast-close"></i>
        </div>
        <div class="toast-content">${message}</div>
        <div class="toast-progress-bar"></div>
    `;

    toastArea.appendChild(toast);

    const closeBtn = toast.querySelector('.toast-close');
    let removeTimeout;

    const removeToast = () => {
        if (toast.classList.contains('hiding')) return;
        toast.classList.add('hiding');
        setTimeout(() => toast.remove(), 300);
        clearTimeout(removeTimeout);
    };

    closeBtn.addEventListener('click', removeToast);
    removeTimeout = setTimeout(removeToast, 4000);
}

window.spawnToast = spawnToast;

function initDjangoToasts() {
    if (!toastArea) return;
    const djangoToasts = toastArea.querySelectorAll('.toast-box[data-toast-type]');
    djangoToasts.forEach(toast => {
        const type = toast.dataset.toastType;
        const title = toast.dataset.toastTitle || 'Info';
        const iconClass = type === 'error' ? 'fa-circle-xmark' :
            type === 'warning' ? 'fa-triangle-exclamation' :
                type === 'success' ? 'fa-circle-check' : 'fa-circle-info';

        toast.classList.add(`toast-${type}`);
        const headSpan = toast.querySelector('.toast-head span');
        if (headSpan) {
            headSpan.innerHTML = `<i class="fa-solid ${iconClass}"></i> ${title}`;
        }

        const closeBtn = toast.querySelector('.toast-close');
        let removeTimeout;
        const removeToast = () => {
            if (toast.classList.contains('hiding')) return;
            toast.classList.add('hiding');
            setTimeout(() => toast.remove(), 300);
            clearTimeout(removeTimeout);
        };
        closeBtn.addEventListener('click', removeToast);
        removeTimeout = setTimeout(removeToast, 4000);
    });
}

function setActiveSidebarItem() {
    if (!sidebar) return;
    const currentPath = window.location.pathname;
    const menuItems = sidebar.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

window.addEventListener('DOMContentLoaded', () => {
    initDjangoToasts();
    setActiveSidebarItem();
});