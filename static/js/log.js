const logDetailModal = document.getElementById('logDetailModal');
const logDetailModalClose = document.getElementById('logDetailModalClose');
const logDetailModalCancel = document.getElementById('logDetailModalCancel');
const logDetailButtons = document.querySelectorAll('.btn-log-detail');

function showLogDetail(button) {
    document.getElementById('logDetailCreated').textContent = button.dataset.created || '-';
    document.getElementById('logDetailLevel').textContent = button.dataset.level || '-';
    document.getElementById('logDetailEvent').textContent = button.dataset.event || '-';
    document.getElementById('logDetailPath').textContent = button.dataset.path || '-';
    document.getElementById('logDetailMethod').textContent = button.dataset.method || '-';
    document.getElementById('logDetailStatus').textContent = button.dataset.status || '-';
    document.getElementById('logDetailUser').textContent = button.dataset.user || '-';
    document.getElementById('logDetailModule').textContent = button.dataset.module || '-';
    document.getElementById('logDetailAction').textContent = button.dataset.action || '-';
    document.getElementById('logDetailObjectRepr').textContent = button.dataset.objectRepr || '-';
    document.getElementById('logDetailIp').textContent = button.dataset.ip || '-';
    document.getElementById('logDetailUserAgent').textContent = button.dataset.userAgent || '-';
    document.getElementById('logDetailMetadata').textContent = button.dataset.metadata || '{}';

    logDetailModal.classList.add('open');
}

if (logDetailButtons.length) {
    logDetailButtons.forEach(button => {
        button.addEventListener('click', () => {
            showLogDetail(button);
        });
    });
}

if (logDetailModalClose) {
    logDetailModalClose.addEventListener('click', () => {
        logDetailModal.classList.remove('open');
    });
}

if (logDetailModalCancel) {
    logDetailModalCancel.addEventListener('click', () => {
        logDetailModal.classList.remove('open');
    });
}

if (logDetailModal) {
    logDetailModal.addEventListener('click', (e) => {
        if (e.target === logDetailModal) {
            logDetailModal.classList.remove('open');
        }
    });
}