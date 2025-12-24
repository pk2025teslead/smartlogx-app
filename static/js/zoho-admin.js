/**
 * SmartLogX Admin Panel - Zoho Projects Style JavaScript
 */

// ============================================
// Sidebar Toggle
// ============================================
function initSidebar() {
    const sidebar = document.querySelector('.zoho-sidebar');
    const main = document.querySelector('.zoho-main');
    const toggleBtn = document.querySelector('.zoho-sidebar-toggle');
    const mobileToggle = document.querySelector('.zoho-mobile-toggle');
    
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            main.classList.toggle('expanded');
            
            // Save state to localStorage
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
            
            // Update toggle icon
            const icon = toggleBtn.querySelector('i');
            if (sidebar.classList.contains('collapsed')) {
                icon.classList.remove('bi-chevron-left');
                icon.classList.add('bi-chevron-right');
            } else {
                icon.classList.remove('bi-chevron-right');
                icon.classList.add('bi-chevron-left');
            }
        });
    }
    
    // Mobile toggle
    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            sidebar.classList.toggle('mobile-open');
        });
    }
    
    // Restore sidebar state
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (isCollapsed && sidebar) {
        sidebar.classList.add('collapsed');
        main.classList.add('expanded');
    }
    
    // Close sidebar on mobile when clicking outside
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 992) {
            if (!sidebar.contains(e.target) && !mobileToggle.contains(e.target)) {
                sidebar.classList.remove('mobile-open');
            }
        }
    });
    
    // Submenu toggle
    initSidebarSubmenu();
}

// ============================================
// Sidebar Submenu Toggle
// ============================================
function initSidebarSubmenu() {
    const submenuToggles = document.querySelectorAll('.zoho-sidebar-toggle-submenu');
    
    submenuToggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            const parent = toggle.closest('.zoho-sidebar-dropdown');
            
            // Close other open submenus
            document.querySelectorAll('.zoho-sidebar-dropdown.open').forEach(item => {
                if (item !== parent) {
                    item.classList.remove('open');
                }
            });
            
            // Toggle current submenu
            parent.classList.toggle('open');
        });
    });
}

// ============================================
// Table Search & Filter
// ============================================
function initTableSearch() {
    const searchInput = document.querySelector('.zoho-search-input');
    const table = document.querySelector('.zoho-table');
    
    if (searchInput && table) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
            
            updatePaginationInfo();
        });
    }
}

function initRoleFilter() {
    const roleFilter = document.querySelector('.zoho-role-filter');
    const table = document.querySelector('.zoho-table');
    
    if (roleFilter && table) {
        roleFilter.addEventListener('change', function() {
            const selectedRole = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const roleCell = row.querySelector('[data-role]');
                if (roleCell) {
                    const role = roleCell.getAttribute('data-role').toLowerCase();
                    if (selectedRole === '' || role.includes(selectedRole)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            });
            
            updatePaginationInfo();
        });
    }
}

// ============================================
// Pagination
// ============================================
let currentPage = 1;
let rowsPerPage = 10;

function initPagination() {
    const rowsSelect = document.querySelector('.zoho-rows-select');
    
    if (rowsSelect) {
        rowsSelect.addEventListener('change', function() {
            rowsPerPage = parseInt(this.value);
            currentPage = 1;
            showPage(currentPage);
        });
    }
    
    showPage(1);
}

function showPage(page) {
    const table = document.querySelector('.zoho-table');
    if (!table) return;
    
    const rows = Array.from(table.querySelectorAll('tbody tr')).filter(row => row.style.display !== 'none');
    const totalRows = rows.length;
    const totalPages = Math.ceil(totalRows / rowsPerPage);
    
    currentPage = Math.max(1, Math.min(page, totalPages));
    
    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    
    // Hide all rows first
    table.querySelectorAll('tbody tr').forEach(row => {
        row.classList.add('pagination-hidden');
    });
    
    // Show rows for current page
    rows.forEach((row, index) => {
        if (index >= start && index < end) {
            row.classList.remove('pagination-hidden');
        }
    });
    
    updatePaginationControls(totalPages);
    updatePaginationInfo();
}

function updatePaginationControls(totalPages) {
    const controls = document.querySelector('.zoho-pagination-controls');
    if (!controls) return;
    
    let html = `
        <button class="zoho-page-btn" onclick="showPage(1)" ${currentPage === 1 ? 'disabled' : ''}>
            <i class="bi bi-chevron-double-left"></i>
        </button>
        <button class="zoho-page-btn" onclick="showPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
            <i class="bi bi-chevron-left"></i>
        </button>
    `;
    
    // Page numbers
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);
    
    for (let i = startPage; i <= endPage; i++) {
        html += `
            <button class="zoho-page-btn ${i === currentPage ? 'active' : ''}" onclick="showPage(${i})">
                ${i}
            </button>
        `;
    }
    
    html += `
        <button class="zoho-page-btn" onclick="showPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
            <i class="bi bi-chevron-right"></i>
        </button>
        <button class="zoho-page-btn" onclick="showPage(${totalPages})" ${currentPage === totalPages ? 'disabled' : ''}>
            <i class="bi bi-chevron-double-right"></i>
        </button>
    `;
    
    controls.innerHTML = html;
}

function updatePaginationInfo() {
    const info = document.querySelector('.zoho-pagination-info');
    const table = document.querySelector('.zoho-table');
    if (!info || !table) return;
    
    const visibleRows = Array.from(table.querySelectorAll('tbody tr')).filter(row => 
        row.style.display !== 'none' && !row.classList.contains('pagination-hidden')
    );
    const totalRows = Array.from(table.querySelectorAll('tbody tr')).filter(row => 
        row.style.display !== 'none'
    ).length;
    
    const start = (currentPage - 1) * rowsPerPage + 1;
    const end = Math.min(currentPage * rowsPerPage, totalRows);
    
    info.textContent = `Showing ${start} to ${end} of ${totalRows} entries`;
}

// ============================================
// Select All Checkbox
// ============================================
function initSelectAll() {
    const selectAll = document.querySelector('.zoho-select-all');
    const checkboxes = document.querySelectorAll('.zoho-row-checkbox');
    
    if (selectAll) {
        selectAll.addEventListener('change', function() {
            checkboxes.forEach(cb => {
                cb.checked = this.checked;
            });
        });
    }
    
    checkboxes.forEach(cb => {
        cb.addEventListener('change', function() {
            const allChecked = Array.from(checkboxes).every(c => c.checked);
            const someChecked = Array.from(checkboxes).some(c => c.checked);
            
            if (selectAll) {
                selectAll.checked = allChecked;
                selectAll.indeterminate = someChecked && !allChecked;
            }
        });
    });
}

// ============================================
// Delete Confirmation with SweetAlert2
// ============================================
function confirmDelete(userId, userName) {
    Swal.fire({
        title: 'Delete User?',
        html: `Are you sure you want to delete <strong>${userName}</strong>?<br>This action cannot be undone.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, Delete',
        cancelButtonText: 'Cancel',
        customClass: {
            popup: 'zoho-swal',
            confirmButton: 'zoho-btn zoho-btn-danger',
            cancelButton: 'zoho-btn zoho-btn-secondary'
        },
        buttonsStyling: false,
        showClass: {
            popup: 'animate__animated animate__fadeInUp animate__faster'
        },
        hideClass: {
            popup: 'animate__animated animate__fadeOutDown animate__faster'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            showLoader();
            document.getElementById('delete-form-' + userId).submit();
        }
    });
}

// ============================================
// Reset Password Confirmation
// ============================================
function confirmResetPassword(userId, userName) {
    Swal.fire({
        title: 'Reset Password?',
        html: `Reset password for <strong>${userName}</strong> to <code>Temp@123</code>?`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Yes, Reset',
        cancelButtonText: 'Cancel',
        customClass: {
            popup: 'zoho-swal',
            confirmButton: 'zoho-btn zoho-btn-primary',
            cancelButton: 'zoho-btn zoho-btn-secondary'
        },
        buttonsStyling: false
    }).then((result) => {
        if (result.isConfirmed) {
            showLoader();
            document.getElementById('reset-form-' + userId).submit();
        }
    });
}

// ============================================
// Loader
// ============================================
function showLoader() {
    const loader = document.querySelector('.zoho-loader-overlay');
    if (loader) {
        loader.classList.add('active');
    }
}

function hideLoader() {
    const loader = document.querySelector('.zoho-loader-overlay');
    if (loader) {
        loader.classList.remove('active');
    }
}

// ============================================
// Toast Notifications
// ============================================
function showToast(message, type = 'success') {
    const container = document.querySelector('.zoho-toast-container') || createToastContainer();
    
    const icons = {
        success: 'bi-check-circle-fill',
        error: 'bi-x-circle-fill',
        warning: 'bi-exclamation-triangle-fill'
    };
    
    const toast = document.createElement('div');
    toast.className = `zoho-toast ${type}`;
    toast.innerHTML = `
        <i class="bi ${icons[type]} zoho-toast-icon"></i>
        <span class="zoho-toast-message">${message}</span>
        <button class="zoho-toast-close" onclick="this.parentElement.remove()">
            <i class="bi bi-x"></i>
        </button>
    `;
    
    container.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'zoho-toast-container';
    document.body.appendChild(container);
    return container;
}

// ============================================
// Form Validation
// ============================================
function initFormValidation() {
    const forms = document.querySelectorAll('.zoho-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                removeError(field);
                
                if (!field.value.trim()) {
                    showError(field, 'This field is required');
                    isValid = false;
                }
                
                // Email validation
                if (field.type === 'email' && field.value) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(field.value)) {
                        showError(field, 'Please enter a valid email address');
                        isValid = false;
                    }
                }
                
                // Mobile validation
                if (field.name === 'mobile_number' && field.value) {
                    const mobileRegex = /^[0-9]{10}$/;
                    if (!mobileRegex.test(field.value)) {
                        showError(field, 'Please enter a valid 10-digit mobile number');
                        isValid = false;
                    }
                }
            });
            
            // Password confirmation
            const password = form.querySelector('[name="password"]');
            const confirmPassword = form.querySelector('[name="confirm_password"]');
            
            if (password && confirmPassword && password.value !== confirmPassword.value) {
                showError(confirmPassword, 'Passwords do not match');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
            } else {
                showLoader();
            }
        });
    });
}

function showError(field, message) {
    field.classList.add('error');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'zoho-form-error';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function removeError(field) {
    field.classList.remove('error');
    const errorDiv = field.parentNode.querySelector('.zoho-form-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// ============================================
// Dropdown Menu
// ============================================
function initDropdowns() {
    const dropdowns = document.querySelectorAll('.zoho-dropdown');
    
    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('.zoho-dropdown-trigger');
        
        if (trigger) {
            trigger.addEventListener('click', (e) => {
                e.stopPropagation();
                
                // Close other dropdowns
                dropdowns.forEach(d => {
                    if (d !== dropdown) d.classList.remove('open');
                });
                
                dropdown.classList.toggle('open');
            });
        }
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', () => {
        dropdowns.forEach(d => d.classList.remove('open'));
    });
}

// ============================================
// Initialize AOS Animations
// ============================================
function initAnimations() {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 600,
            easing: 'ease-out-cubic',
            once: true,
            offset: 50
        });
    }
}

// ============================================
// Profile Panel
// ============================================
function initProfilePanel() {
    const profileToggle = document.getElementById('profileToggle');
    const profilePanel = document.getElementById('profilePanel');
    const profileOverlay = document.getElementById('profileOverlay');
    const profileClose = document.getElementById('profileClose');
    const photoInput = document.getElementById('photoInput');
    const profileForm = document.getElementById('profileForm');
    
    if (!profileToggle || !profilePanel) return;
    
    // Open profile panel
    profileToggle.addEventListener('click', () => {
        profilePanel.classList.add('active');
        profileOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
    
    // Close profile panel
    function closeProfilePanel() {
        profilePanel.classList.remove('active');
        profileOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    profileClose.addEventListener('click', closeProfilePanel);
    profileOverlay.addEventListener('click', closeProfilePanel);
    
    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && profilePanel.classList.contains('active')) {
            closeProfilePanel();
        }
    });
    
    // Photo upload preview
    if (photoInput) {
        photoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const profileImage = document.getElementById('profileImage');
                    const profileInitials = document.getElementById('profileInitials');
                    
                    profileImage.src = e.target.result;
                    profileImage.style.display = 'block';
                    profileInitials.style.display = 'none';
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Profile form submit
    if (profileForm) {
        profileForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/adminpanel/profile/update/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                });
                
                const result = await response.json();
                
                if (result.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Profile Updated',
                        text: result.message,
                        background: '#1f2124',
                        color: '#fff',
                        confirmButtonColor: '#3b82f6'
                    }).then(() => {
                        if (result.reload) {
                            window.location.reload();
                        }
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: result.error,
                        background: '#1f2124',
                        color: '#fff',
                        confirmButtonColor: '#3b82f6'
                    });
                }
            } catch (error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Something went wrong. Please try again.',
                    background: '#1f2124',
                    color: '#fff',
                    confirmButtonColor: '#3b82f6'
                });
            }
        });
    }
}

// ============================================
// Initialize Everything
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    initSidebar();
    initTableSearch();
    initRoleFilter();
    initPagination();
    initSelectAll();
    initFormValidation();
    initDropdowns();
    initAnimations();
    initProfilePanel();
    
    // Hide loader on page load
    hideLoader();
    
    // Show success/error messages from Django
    const messages = document.querySelectorAll('.django-message');
    messages.forEach(msg => {
        const type = msg.dataset.type || 'success';
        showToast(msg.textContent, type);
    });
});

// Add CSS for pagination hidden rows
const style = document.createElement('style');
style.textContent = '.pagination-hidden { display: none !important; }';
document.head.appendChild(style);
