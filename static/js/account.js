const accountSearch = document.getElementById('accountSearch');
const deleteModal = document.getElementById('deleteModal');
const deleteForm = document.getElementById('deleteForm');
const deleteModalClose = document.getElementById('deleteModalClose');
const deleteModalCancel = document.getElementById('deleteModalCancel');
const deleteButtons = document.querySelectorAll('.btn-delete');

if (accountSearch) {
    accountSearch.addEventListener('input', () => {
        const query = accountSearch.value.trim();
        const url = new URL(window.location.href);
        if (query) {
            url.searchParams.set('q', query);
        } else {
            url.searchParams.delete('q');
        }
        url.searchParams.delete('page');
        window.location.href = url.toString();
    });
}

if (deleteButtons.length) {
    deleteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const deleteUrl = button.dataset.url;
            if (deleteForm) {
                deleteForm.action = deleteUrl;
            }
            if (deleteModal) {
                deleteModal.classList.add('open');
            }
        });
    });
}

if (deleteModalClose) {
    deleteModalClose.addEventListener('click', () => {
        deleteModal.classList.remove('open');
    });
}

if (deleteModalCancel) {
    deleteModalCancel.addEventListener('click', () => {
        deleteModal.classList.remove('open');
    });
}

if (deleteModal) {
    deleteModal.addEventListener('click', (e) => {
        if (e.target === deleteModal) {
            deleteModal.classList.remove('open');
        }
    });
}