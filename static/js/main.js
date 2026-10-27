// ============================================================
// AlumniConnect - Main JavaScript
// ============================================================

// Auto-close flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(function () { alert.remove(); }, 500);
        }, 5000);
    });
});

// Modal open/close
function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.style.display = 'flex';
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.style.display = 'none';
}

// Close modal if user clicks outside the content box
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }
});

// Client-side password match validation
(function () {
    const form = document.getElementById('registerForm');
    if (!form) return;
    form.addEventListener('submit', function (e) {
        const pwd = document.getElementById('password');
        const confirm = document.getElementById('confirm_password');
        if (pwd && confirm && pwd.value !== confirm.value) {
            e.preventDefault();
            alert('Passwords do not match. Please re-enter your password.');
            confirm.focus();
        }
    });
})();
