/**
 * SmartLogX Admin Panel - Draggable Tables & AJAX Operations
 * Zoho Projects Style with Persistent Column Order
 */

// ============================================
// Draggable Table Class
// ============================================
class AdminDraggableTable {
    constructor(tableId, tableName) {
        this.table = document.getElementById(tableId);
        this.tableName = tableName;
        this.storageKey = `admin_${tableName}_cols`;
        this.draggedCol = null;
        this.draggedIdx = null;
        
        if (this.table) {
            this.init();
        }
    }
    
    init() {
        this.headerRow = this.table.querySelector('thead tr');
        this.headers = Array.from(this.headerRow.querySelectorAll('th[data-col]'));
        this.loadColumnOrder();
        this.setupDragEvents();
    }
    
    loadColumnOrder() {
        const saved = localStorage.getItem(this.storageKey);
        if (saved) {
            try {
                const order = JSON.parse(saved);
                this.reorderColumns(order);
            } catch (e) { console.error('Column order load error:', e); }
        }
    }
    
    saveColumnOrder() {
        const order = this.headers.map(th => th.dataset.col);
        localStorage.setItem(this.storageKey, JSON.stringify(order));
    }
    
    reorderColumns(order) {
        const tbody = this.table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const currentOrder = this.headers.map(th => th.dataset.col);

        const sortedHeaders = [...this.headers].sort((a, b) => {
            return order.indexOf(a.dataset.col) - order.indexOf(b.dataset.col);
        });
        
        sortedHeaders.forEach(th => this.headerRow.appendChild(th));
        this.headers = sortedHeaders;
        
        rows.forEach(row => {
            const cells = Array.from(row.querySelectorAll('td[data-col]'));
            const sortedCells = [...cells].sort((a, b) => {
                return order.indexOf(a.dataset.col) - order.indexOf(b.dataset.col);
            });
            sortedCells.forEach(td => row.appendChild(td));
        });
    }
    
    setupDragEvents() {
        this.headers.forEach((header, idx) => {
            if (header.dataset.draggable === 'false') return;
            
            header.setAttribute('draggable', 'true');
            header.classList.add('draggable-col');
            
            if (!header.querySelector('.drag-icon')) {
                const icon = document.createElement('i');
                icon.className = 'bi bi-grip-vertical drag-icon';
                header.insertBefore(icon, header.firstChild);
            }
            
            header.addEventListener('dragstart', (e) => this.onDragStart(e, idx));
            header.addEventListener('dragend', () => this.onDragEnd());
            header.addEventListener('dragover', (e) => e.preventDefault());
            header.addEventListener('dragenter', (e) => this.onDragEnter(e, idx));
            header.addEventListener('drop', (e) => this.onDrop(e, idx));
        });
    }
    
    onDragStart(e, idx) {
        this.draggedCol = this.headers[idx];
        this.draggedIdx = idx;
        e.dataTransfer.effectAllowed = 'move';
        setTimeout(() => this.draggedCol.classList.add('dragging'), 0);
    }
    
    onDragEnd() {
        if (this.draggedCol) this.draggedCol.classList.remove('dragging');
        this.headers.forEach(h => h.classList.remove('drag-over'));
        this.draggedCol = null;
        this.draggedIdx = null;
    }
    
    onDragEnter(e, idx) {
        e.preventDefault();
        this.headers.forEach(h => h.classList.remove('drag-over'));
        if (this.headers[idx] !== this.draggedCol) {
            this.headers[idx].classList.add('drag-over');
        }
    }
    
    onDrop(e, targetIdx) {
        e.preventDefault();
        this.headers[targetIdx].classList.remove('drag-over');
        if (this.draggedIdx === targetIdx) return;
        
        this.swapColumns(this.draggedIdx, targetIdx);
        this.saveColumnOrder();
    }
    
    swapColumns(fromIdx, toIdx) {
        const tbody = this.table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const fromHeader = this.headers[fromIdx];
        const toHeader = this.headers[toIdx];
        
        if (fromIdx < toIdx) {
            this.headerRow.insertBefore(fromHeader, toHeader.nextSibling);
        } else {
            this.headerRow.insertBefore(fromHeader, toHeader);
        }
        
        this.headers = Array.from(this.headerRow.querySelectorAll('th[data-col]'));
        
        rows.forEach(row => {
            const cells = Array.from(row.querySelectorAll('td[data-col]'));
            const fromCell = cells[fromIdx];
            const toCell = cells[toIdx];
            if (fromCell && toCell) {
                if (fromIdx < toIdx) {
                    row.insertBefore(fromCell, toCell.nextSibling);
                } else {
                    row.insertBefore(fromCell, toCell);
                }
            }
        });
    }
    
    resetOrder() {
        localStorage.removeItem(this.storageKey);
        location.reload();
    }
}

// ============================================
// Slide Panel Functions
// ============================================
function openAdminSlidePanel(title, content) {
    const panel = document.getElementById('adminSlidePanel');
    const overlay = document.getElementById('adminSlidePanelOverlay');
    document.getElementById('adminSlidePanelTitle').textContent = title;
    document.getElementById('adminSlidePanelBody').innerHTML = content;
    panel.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeAdminSlidePanel() {
    const panel = document.getElementById('adminSlidePanel');
    const overlay = document.getElementById('adminSlidePanelOverlay');
    panel.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
}

// ============================================
// AJAX Helper Functions
// ============================================
function adminAjax(url, method, data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    };
    if (data) options.body = JSON.stringify(data);
    return fetch(url, options).then(r => r.json());
}

function showAdminLoader() {
    document.getElementById('adminLoader')?.classList.add('active');
}

function hideAdminLoader() {
    document.getElementById('adminLoader')?.classList.remove('active');
}


// ============================================
// Leave Management Functions
// ============================================
function viewLeaveAdmin(id) {
    showAdminLoader();
    adminAjax(`/adminpanel/attendance/leave/${id}/`, 'GET').then(data => {
        hideAdminLoader();
        if (data.success) {
            const l = data.leave;
            const statusClass = l.is_approved === 1 ? 'approved' : (l.is_approved === 0 ? 'rejected' : 'pending');
            const html = `
                <div class="admin-view-header">
                    <div class="admin-view-icon leave"><i class="bi bi-calendar-x"></i></div>
                    <div><h4>${l.leave_type} Leave</h4><p>${l.user_name} (${l.user_id})</p></div>
                </div>
                <div class="admin-view-grid">
                    <div class="admin-view-item"><label>Date</label><span>${l.leave_date_display}</span></div>
                    <div class="admin-view-item"><label>Status</label><span class="status-badge ${statusClass}">${l.status}</span></div>
                    <div class="admin-view-item"><label>Requested</label><span>${l.requested_at}</span></div>
                    ${l.approved_at ? `<div class="admin-view-item"><label>Processed</label><span>${l.approved_at}</span></div>` : ''}
                </div>
                ${l.notes ? `<div class="admin-view-content"><label>Notes</label><p>${escapeHtml(l.notes)}</p></div>` : ''}
                ${l.approval_notes ? `<div class="admin-view-content"><label>Admin Notes</label><p>${escapeHtml(l.approval_notes)}</p></div>` : ''}
            `;
            openAdminSlidePanel('Leave Details', html);
        }
    });
}

function editLeaveAdmin(id) {
    showAdminLoader();
    adminAjax(`/adminpanel/attendance/leave/${id}/`, 'GET').then(data => {
        hideAdminLoader();
        if (data.success) {
            const l = data.leave;
            const html = `
                <form id="editLeaveForm" class="admin-form">
                    <div class="form-group"><label>Employee</label><input type="text" value="${l.user_name} (${l.user_id})" disabled class="form-input"></div>
                    <div class="form-group"><label>Date</label><input type="date" name="leave_date" value="${l.leave_date}" class="form-input" required></div>
                    <div class="form-group"><label>Type</label>
                        <select name="leave_type" class="form-input" required>
                            <option value="Planned" ${l.leave_type==='Planned'?'selected':''}>Planned</option>
                            <option value="Casual" ${l.leave_type==='Casual'?'selected':''}>Casual</option>
                            <option value="Emergency" ${l.leave_type==='Emergency'?'selected':''}>Emergency</option>
                            <option value="Sick" ${l.leave_type==='Sick'?'selected':''}>Sick</option>
                        </select>
                    </div>
                    <div class="form-group"><label>Notes</label><textarea name="notes" class="form-input" rows="3">${l.notes}</textarea></div>
                    <div class="form-actions">
                        <button type="submit" class="btn-primary"><i class="bi bi-check-lg"></i> Update</button>
                        <button type="button" class="btn-secondary" onclick="closeAdminSlidePanel()">Cancel</button>
                    </div>
                </form>
            `;
            openAdminSlidePanel('Edit Leave', html);
            document.getElementById('editLeaveForm').addEventListener('submit', (e) => {
                e.preventDefault();
                const fd = new FormData(e.target);
                showAdminLoader();
                adminAjax(`/adminpanel/attendance/leave/${id}/update/`, 'POST', {
                    leave_date: fd.get('leave_date'),
                    leave_type: fd.get('leave_type'),
                    notes: fd.get('notes')
                }).then(res => {
                    hideAdminLoader();
                    if (res.success) {
                        closeAdminSlidePanel();
                        Swal.fire({title:'Updated!',text:res.message,icon:'success',customClass:{popup:'zoho-swal'}}).then(()=>location.reload());
                    } else {
                        Swal.fire({title:'Error',text:res.error,icon:'error',customClass:{popup:'zoho-swal'}});
                    }
                });
            });
        }
    });
}

function deleteLeaveAdmin(id) {
    Swal.fire({
        title: 'Delete Leave?', text: 'This cannot be undone.', icon: 'warning',
        showCancelButton: true, confirmButtonText: 'Delete', customClass: {popup:'zoho-swal'}
    }).then(r => {
        if (r.isConfirmed) {
            showAdminLoader();
            adminAjax(`/adminpanel/attendance/leave/${id}/delete/`, 'POST').then(res => {
                hideAdminLoader();
                if (res.success) {
                    Swal.fire({title:'Deleted!',icon:'success',customClass:{popup:'zoho-swal'}}).then(()=>location.reload());
                } else {
                    Swal.fire({title:'Error',text:res.error,icon:'error',customClass:{popup:'zoho-swal'}});
                }
            });
        }
    });
}

function approveLeaveAdmin(id, approve) {
    const action = approve ? 'Approve' : 'Reject';
    Swal.fire({
        title: `${action} Leave?`, icon: 'question', showCancelButton: true,
        confirmButtonText: action, input: 'textarea', inputPlaceholder: 'Admin notes (optional)',
        customClass: {popup:'zoho-swal'}
    }).then(r => {
        if (r.isConfirmed) {
            showAdminLoader();
            adminAjax(`/adminpanel/attendance/leave/${id}/approve/`, 'POST', {
                is_approved: approve ? 1 : 0,
                approval_notes: r.value || ''
            }).then(res => {
                hideAdminLoader();
                if (res.success) {
                    Swal.fire({title:`${action}d!`,icon:'success',customClass:{popup:'zoho-swal'}}).then(()=>location.reload());
                } else {
                    Swal.fire({title:'Error',text:res.error,icon:'error',customClass:{popup:'zoho-swal'}});
                }
            });
        }
    });
}

// ============================================
// Comp-Off Management Functions
// ============================================
function viewCompoffAdmin(id) {
    showAdminLoader();
    adminAjax(`/adminpanel/attendance/compoff/${id}/`, 'GET').then(data => {
        hideAdminLoader();
        if (data.success) {
            const c = data.compoff;
            const statusClass = c.is_approved === 1 ? 'approved' : (c.is_approved === 0 ? 'rejected' : 'pending');
            const html = `
                <div class="admin-view-header">
                    <div class="admin-view-icon compoff"><i class="bi bi-calendar-plus"></i></div>
                    <div><h4>Sunday Comp-Off</h4><p>${c.user_name} (${c.user_id})</p></div>
                </div>
                <div class="admin-view-grid">
                    <div class="admin-view-item"><label>Sunday Worked</label><span>${c.sunday_date_display}</span></div>
                    <div class="admin-view-item"><label>Comp-Off Date</label><span>${c.compoff_date_display}</span></div>
                    <div class="admin-view-item"><label>Status</label><span class="status-badge ${statusClass}">${c.status}</span></div>
                </div>
                <div class="admin-view-content"><label>Work Purpose</label><p>${escapeHtml(c.work_purpose)}</p></div>
                ${c.notes ? `<div class="admin-view-content"><label>Notes</label><p>${escapeHtml(c.notes)}</p></div>` : ''}
            `;
            openAdminSlidePanel('Comp-Off Details', html);
        }
    });
}

function approveCompoffAdmin(id, approve) {
    const action = approve ? 'Approve' : 'Reject';
    Swal.fire({
        title: `${action} Comp-Off?`, icon: 'question', showCancelButton: true,
        confirmButtonText: action, input: 'textarea', inputPlaceholder: 'Admin notes (optional)',
        customClass: {popup:'zoho-swal'}
    }).then(r => {
        if (r.isConfirmed) {
            showAdminLoader();
            adminAjax(`/adminpanel/attendance/compoff/${id}/approve/`, 'POST', {
                is_approved: approve ? 1 : 0, approval_notes: r.value || ''
            }).then(res => {
                hideAdminLoader();
                if (res.success) {
                    Swal.fire({title:`${action}d!`,icon:'success',customClass:{popup:'zoho-swal'}}).then(()=>location.reload());
                } else {
                    Swal.fire({title:'Error',text:res.error,icon:'error',customClass:{popup:'zoho-swal'}});
                }
            });
        }
    });
}

function deleteCompoffAdmin(id) {
    Swal.fire({
        title: 'Delete Comp-Off?', text: 'This cannot be undone.', icon: 'warning',
        showCancelButton: true, confirmButtonText: 'Delete', customClass: {popup:'zoho-swal'}
    }).then(r => {
        if (r.isConfirmed) {
            showAdminLoader();
            adminAjax(`/adminpanel/attendance/compoff/${id}/delete/`, 'POST').then(res => {
                hideAdminLoader();
                if (res.success) {
                    Swal.fire({title:'Deleted!',icon:'success',customClass:{popup:'zoho-swal'}}).then(()=>location.reload());
                } else {
                    Swal.fire({title:'Error',text:res.error,icon:'error',customClass:{popup:'zoho-swal'}});
                }
            });
        }
    });
}

// ============================================
// WFH Management Functions
// ============================================
function viewWfhAdmin(id) {
    showAdminLoader();
    adminAjax(`/adminpanel/attendance/wfh/${id}/`, 'GET').then(data => {
        hideAdminLoader();
        if (data.success) {
            const w = data.wfh;
            const statusClass = w.is_approved === 1 ? 'approved' : (w.is_approved === 0 ? 'rejected' : 'pending');
            const html = `
                <div class="admin-view-header">
                    <div class="admin-view-icon wfh"><i class="bi bi-house"></i></div>
                    <div><h4>Work From Home</h4><p>${w.user_name} (${w.user_id})</p></div>
                </div>
                <div class="admin-view-grid">
                    <div class="admin-view-item"><label>Date</label><span>${w.wfh_date_display}</span></div>
                    <div class="admin-view-item"><label>Status</label><span class="status-badge ${statusClass}">${w.status}</span></div>
                </div>
                <div class="admin-view-content"><label>Reason</label><p>${escapeHtml(w.reason)}</p></div>
                ${w.notes ? `<div class="admin-view-content"><label>Notes</label><p>${escapeHtml(w.notes)}</p></div>` : ''}
            `;
            openAdminSlidePanel('WFH Details', html);
        }
    });
}

function approveWfhAdmin(id, approve) {
    const action = approve ? 'Approve' : 'Reject';
    Swal.fire({
        title: `${action} WFH?`, icon: 'question', showCancelButton: true,
        confirmButtonText: action, input: 'textarea', inputPlaceholder: 'Admin notes (optional)',
        customClass: {popup:'zoho-swal'}
    }).then(r => {
        if (r.isConfirmed) {
            showAdminLoader();
            adminAjax(`/adminpanel/attendance/wfh/${id}/approve/`, 'POST', {
                is_approved: approve ? 1 : 0, approval_notes: r.value || ''
            }).then(res => {
                hideAdminLoader();
                if (res.success) {
                    Swal.fire({title:`${action}d!`,icon:'success',customClass:{popup:'zoho-swal'}}).then(()=>location.reload());
                } else {
                    Swal.fire({title:'Error',text:res.error,icon:'error',customClass:{popup:'zoho-swal'}});
                }
            });
        }
    });
}

function deleteWfhAdmin(id) {
    Swal.fire({
        title: 'Delete WFH?', text: 'This cannot be undone.', icon: 'warning',
        showCancelButton: true, confirmButtonText: 'Delete', customClass: {popup:'zoho-swal'}
    }).then(r => {
        if (r.isConfirmed) {
            showAdminLoader();
            adminAjax(`/adminpanel/attendance/wfh/${id}/delete/`, 'POST').then(res => {
                hideAdminLoader();
                if (res.success) {
                    Swal.fire({title:'Deleted!',icon:'success',customClass:{popup:'zoho-swal'}}).then(()=>location.reload());
                } else {
                    Swal.fire({title:'Error',text:res.error,icon:'error',customClass:{popup:'zoho-swal'}});
                }
            });
        }
    });
}

// ============================================
// Log Management Functions
// ============================================
function viewLogAdmin(id) {
    showAdminLoader();
    adminAjax(`/adminpanel/logs/${id}/`, 'GET').then(data => {
        hideAdminLoader();
        if (data.success) {
            const l = data.log;
            const html = `
                <div class="admin-view-header">
                    <div class="admin-view-icon log"><i class="bi bi-journal-text"></i></div>
                    <div><h4>${escapeHtml(l.project_title)}</h4><p>${l.user_name} (${l.user_id})</p></div>
                </div>
                <div class="admin-view-grid">
                    <div class="admin-view-item"><label>Date</label><span>${l.log_date_display}</span></div>
                    <div class="admin-view-item"><label>Session</label><span class="session-badge ${l.session_type==='First Half'?'first':'second'}">${l.session_type}</span></div>
                    <div class="admin-view-item"><label>Created</label><span>${l.created_at}</span></div>
                    <div class="admin-view-item"><label>Approval</label><span>${l.approval_required ? 'Yes' : 'No'}</span></div>
                </div>
                <div class="admin-view-content"><label>Heading</label><p>${escapeHtml(l.log_heading)}</p></div>
                <div class="admin-view-content"><label>Details</label><p>${escapeHtml(l.log_details)}</p></div>
            `;
            openAdminSlidePanel('Log Details', html);
        }
    });
}

// ============================================
// Utility Functions
// ============================================
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function navigateMonth(year, month, dir) {
    let m = month + dir, y = year;
    if (m > 12) { m = 1; y++; }
    else if (m < 1) { m = 12; y--; }
    window.location.href = `?year=${y}&month=${m}`;
}

function searchAdminTable(query, tableId) {
    const rows = document.querySelectorAll(`#${tableId} tbody tr`);
    query = query.toLowerCase();
    rows.forEach(row => {
        row.style.display = row.textContent.toLowerCase().includes(query) ? '' : 'none';
    });
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    // Close panel events
    document.getElementById('adminSlidePanelOverlay')?.addEventListener('click', closeAdminSlidePanel);
    document.getElementById('adminSlidePanelClose')?.addEventListener('click', closeAdminSlidePanel);
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeAdminSlidePanel(); });
});
