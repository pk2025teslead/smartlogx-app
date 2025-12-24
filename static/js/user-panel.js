/**
 * SmartLogX User Panel - Zoho Style JavaScript
 */

// ============================================
// Slide Panel Management
// ============================================

function openSlidePanel(title, content) {
    const panel = document.getElementById('slidePanel');
    const overlay = document.getElementById('slidePanelOverlay');
    const titleEl = document.getElementById('slidePanelTitle');
    const bodyEl = document.getElementById('slidePanelBody');
    
    titleEl.textContent = title;
    bodyEl.innerHTML = content;
    
    panel.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeSlidePanel() {
    const panel = document.getElementById('slidePanel');
    const overlay = document.getElementById('slidePanelOverlay');
    
    panel.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
}

// Close panel on overlay click
document.addEventListener('DOMContentLoaded', function() {
    const overlay = document.getElementById('slidePanelOverlay');
    const closeBtn = document.getElementById('slidePanelClose');
    
    if (overlay) {
        overlay.addEventListener('click', closeSlidePanel);
    }
    
    if (closeBtn) {
        closeBtn.addEventListener('click', closeSlidePanel);
    }
    
    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeSlidePanel();
        }
    });
});

// ============================================
// Add Log Form
// ============================================

let approvalVerified = false;
let currentSessionType = null;

function openAddLogForm(currentDate, currentDateDisplay) {
    const formHtml = `
        <form id="addLogForm" class="zoho-form">
            <!-- Date Section -->
            <div class="log-form-section">
                <div class="log-form-section-title">Log Date</div>
                <div class="log-date-display">
                    <i class="bi bi-calendar-event"></i>
                    <div>
                        <div class="date-text">${currentDateDisplay}</div>
                        <div class="date-note">Auto-filled (Today's date)</div>
                    </div>
                </div>
                <input type="hidden" name="log_date" value="${currentDate}">
            </div>
            
            <!-- Session Section -->
            <div class="log-form-section">
                <div class="log-form-section-title">Session</div>
                <div class="session-selector">
                    <div class="session-option">
                        <input type="radio" name="session_type" id="firstHalf" value="First Half" required>
                        <label for="firstHalf">
                            <i class="bi bi-sun session-icon"></i>
                            <span class="session-name">First Half</span>
                            <span class="session-time">1:00 PM - 2:30 PM</span>
                        </label>
                    </div>
                    <div class="session-option">
                        <input type="radio" name="session_type" id="secondHalf" value="Second Half" required>
                        <label for="secondHalf">
                            <i class="bi bi-moon session-icon"></i>
                            <span class="session-name">Second Half</span>
                            <span class="session-time">6:00 PM - 7:30 PM</span>
                        </label>
                    </div>
                </div>
                <div id="timeWindowStatus"></div>
                <div id="approvalSection" style="display: none;"></div>
            </div>
            
            <!-- Project Section -->
            <div class="log-form-section">
                <div class="log-form-section-title">Project Details</div>
                <div class="zoho-form-group">
                    <label class="zoho-form-label required">Project Title</label>
                    <input type="text" name="project_title" class="zoho-form-input" 
                           placeholder="Enter project name" required list="projectList">
                    <datalist id="projectList">
                        ${window.userProjects ? window.userProjects.map(p => `<option value="${p}">`).join('') : ''}
                    </datalist>
                </div>
                <div class="zoho-form-group">
                    <label class="zoho-form-label required">Log Heading</label>
                    <input type="text" name="log_heading" class="zoho-form-input" 
                           placeholder="Brief summary of your work" required>
                </div>
            </div>
            
            <!-- Log Details Section -->
            <div class="log-form-section">
                <div class="log-form-section-title">Log Details</div>
                <div class="zoho-form-group">
                    <label class="zoho-form-label required">Details</label>
                    <textarea name="log_details" class="zoho-form-input" rows="6" 
                              placeholder="Describe your work in detail..." required style="resize: vertical;"></textarea>
                </div>
            </div>
            
            <!-- Submit Button -->
            <div class="zoho-btn-group" style="margin-top: 24px;">
                <button type="submit" class="zoho-btn zoho-btn-primary" id="submitLogBtn" disabled>
                    <i class="bi bi-check-lg"></i>
                    Save Log
                </button>
                <button type="button" class="zoho-btn zoho-btn-secondary" onclick="closeSlidePanel()">
                    Cancel
                </button>
            </div>
        </form>
    `;
    
    openSlidePanel('Add New Log', formHtml);
    
    // Reset state
    approvalVerified = false;
    currentSessionType = null;
    
    // Add event listeners
    setTimeout(() => {
        const form = document.getElementById('addLogForm');
        const sessionRadios = document.querySelectorAll('input[name="session_type"]');
        
        sessionRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                currentSessionType = this.value;
                checkTimeWindow(this.value);
            });
        });
        
        form.addEventListener('submit', handleLogSubmit);
    }, 100);
}

function checkTimeWindow(sessionType) {
    const statusDiv = document.getElementById('timeWindowStatus');
    const approvalDiv = document.getElementById('approvalSection');
    const submitBtn = document.getElementById('submitLogBtn');
    
    statusDiv.innerHTML = '<div class="zoho-spinner" style="width: 20px; height: 20px; margin: 10px auto;"></div>';
    
    fetch('/user/logs/check-time/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ session_type: sessionType })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.is_allowed) {
                statusDiv.innerHTML = `
                    <div class="time-window-status allowed">
                        <i class="bi bi-check-circle-fill"></i>
                        <span>You're within the allowed time window (${data.window_start} - ${data.window_end}). Current time: ${data.current_time}</span>
                    </div>
                `;
                approvalDiv.style.display = 'none';
                submitBtn.disabled = false;
                approvalVerified = false;
            } else {
                statusDiv.innerHTML = `
                    <div class="time-window-status not-allowed">
                        <i class="bi bi-exclamation-triangle-fill"></i>
                        <span>Outside allowed window (${data.window_start} - ${data.window_end}). Current time: ${data.current_time}. Approval required.</span>
                    </div>
                `;
                showApprovalSection(approvalDiv);
                submitBtn.disabled = true;
            }
        } else {
            statusDiv.innerHTML = `<div class="time-window-status not-allowed"><i class="bi bi-x-circle"></i> ${data.error}</div>`;
        }
    })
    .catch(error => {
        statusDiv.innerHTML = `<div class="time-window-status not-allowed"><i class="bi bi-x-circle"></i> Error checking time window</div>`;
    });
}

function showApprovalSection(container) {
    container.style.display = 'block';
    container.innerHTML = `
        <div class="approval-section">
            <div class="approval-section-title">
                <i class="bi bi-shield-lock"></i>
                Request Approval
            </div>
            <p style="font-size: 13px; color: var(--zoho-text-secondary); margin-bottom: 12px;">
                Click the button below to send a 6-digit approval code to the admin. Enter the code to proceed.
            </p>
            <button type="button" class="zoho-btn zoho-btn-secondary" onclick="requestApprovalCode()" id="requestCodeBtn">
                <i class="bi bi-send"></i>
                Request Approval Code
            </button>
            <div id="codeInputSection" style="display: none;">
                <div class="approval-code-input">
                    <input type="text" id="approvalCodeInput" class="zoho-form-input" 
                           placeholder="Enter 6-digit code" maxlength="6" pattern="[0-9]{6}">
                    <button type="button" class="zoho-btn zoho-btn-primary" onclick="verifyApprovalCode()">
                        Verify
                    </button>
                </div>
                <div id="approvalStatus"></div>
            </div>
        </div>
    `;
}

function requestApprovalCode() {
    const btn = document.getElementById('requestCodeBtn');
    const codeSection = document.getElementById('codeInputSection');
    
    btn.disabled = true;
    btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Sending...';
    
    fetch('/user/logs/request-approval/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ session_type: currentSessionType })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            btn.innerHTML = '<i class="bi bi-check"></i> Code Sent';
            btn.classList.remove('zoho-btn-secondary');
            btn.classList.add('zoho-btn-success');
            codeSection.style.display = 'block';
            
            // For development - show the code
            if (data.dev_code) {
                console.log('DEV: Approval code is', data.dev_code);
                Swal.fire({
                    title: 'Development Mode',
                    html: `Approval code: <strong>${data.dev_code}</strong><br><small>(This won't show in production)</small>`,
                    icon: 'info',
                    customClass: { popup: 'zoho-swal' }
                });
            }
        } else {
            btn.disabled = false;
            btn.innerHTML = '<i class="bi bi-send"></i> Request Approval Code';
            Swal.fire({
                title: 'Error',
                text: data.error,
                icon: 'error',
                customClass: { popup: 'zoho-swal' }
            });
        }
    })
    .catch(error => {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-send"></i> Request Approval Code';
        Swal.fire({
            title: 'Error',
            text: 'Failed to request approval code',
            icon: 'error',
            customClass: { popup: 'zoho-swal' }
        });
    });
}

function verifyApprovalCode() {
    const codeInput = document.getElementById('approvalCodeInput');
    const statusDiv = document.getElementById('approvalStatus');
    const submitBtn = document.getElementById('submitLogBtn');
    const code = codeInput.value.trim();
    
    if (code.length !== 6) {
        statusDiv.innerHTML = '<div class="approval-status error"><i class="bi bi-x-circle"></i> Please enter a 6-digit code</div>';
        return;
    }
    
    statusDiv.innerHTML = '<div class="zoho-spinner" style="width: 20px; height: 20px; margin: 10px auto;"></div>';
    
    fetch('/user/logs/verify-code/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            statusDiv.innerHTML = '<div class="approval-status success"><i class="bi bi-check-circle-fill"></i> Code verified! You can now submit your log.</div>';
            approvalVerified = true;
            submitBtn.disabled = false;
            codeInput.disabled = true;
        } else {
            statusDiv.innerHTML = `<div class="approval-status error"><i class="bi bi-x-circle"></i> ${data.error}</div>`;
        }
    })
    .catch(error => {
        statusDiv.innerHTML = '<div class="approval-status error"><i class="bi bi-x-circle"></i> Verification failed</div>';
    });
}

function handleLogSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const submitBtn = document.getElementById('submitLogBtn');
    
    const data = {
        project_title: formData.get('project_title'),
        log_heading: formData.get('log_heading'),
        log_details: formData.get('log_details'),
        session_type: formData.get('session_type'),
        approval_used: approvalVerified,
        approval_code: approvalVerified ? document.getElementById('approvalCodeInput')?.value : null
    };
    
    // Validate
    if (!data.session_type) {
        Swal.fire({
            title: 'Session Required',
            text: 'Please select a session (First Half or Second Half)',
            icon: 'warning',
            customClass: { popup: 'zoho-swal' }
        });
        return;
    }
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Saving...';
    
    fetch('/user/logs/save/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            closeSlidePanel();
            Swal.fire({
                title: 'Success!',
                text: data.message,
                icon: 'success',
                customClass: { popup: 'zoho-swal' }
            }).then(() => {
                window.location.reload();
            });
        } else {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="bi bi-check-lg"></i> Save Log';
            
            const errorMsg = data.errors ? data.errors.join('<br>') : data.error;
            Swal.fire({
                title: 'Error',
                html: errorMsg,
                icon: 'error',
                customClass: { popup: 'zoho-swal' }
            });
        }
    })
    .catch(error => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-check-lg"></i> Save Log';
        Swal.fire({
            title: 'Error',
            text: 'Failed to save log',
            icon: 'error',
            customClass: { popup: 'zoho-swal' }
        });
    });
}

// ============================================
// View Log
// ============================================

function viewLog(logId) {
    showLoader();
    
    fetch(`/user/logs/${logId}/`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        hideLoader();
        
        if (data.success) {
            const log = data.log;
            const sessionClass = log.session_type === 'First Half' ? 'first-half' : 'second-half';
            
            const viewHtml = `
                <div class="log-view-header">
                    <div class="log-view-icon">
                        <i class="bi bi-journal-text"></i>
                    </div>
                    <div class="log-view-title">
                        <h4>${escapeHtml(log.project_title)}</h4>
                        <p>${escapeHtml(log.log_heading)}</p>
                    </div>
                </div>
                
                <div class="log-view-meta">
                    <div class="log-view-meta-item">
                        <div class="log-view-meta-label">Date</div>
                        <div class="log-view-meta-value">${log.log_date}</div>
                    </div>
                    <div class="log-view-meta-item">
                        <div class="log-view-meta-label">Session</div>
                        <div class="log-view-meta-value">
                            <span class="log-session-badge ${sessionClass}">
                                <i class="bi bi-${log.session_type === 'First Half' ? 'sun' : 'moon'}"></i>
                                ${log.session_type}
                            </span>
                        </div>
                    </div>
                    <div class="log-view-meta-item">
                        <div class="log-view-meta-label">Created</div>
                        <div class="log-view-meta-value">${log.created_at}</div>
                    </div>
                    <div class="log-view-meta-item">
                        <div class="log-view-meta-label">Approval</div>
                        <div class="log-view-meta-value">${log.approval_required ? 'Yes' : 'No'}</div>
                    </div>
                </div>
                
                <div class="log-view-content">
                    <div class="log-view-content-label">Log Details</div>
                    <div class="log-view-content-text">${escapeHtml(log.log_details)}</div>
                </div>
            `;
            
            openSlidePanel('View Log', viewHtml);
        } else {
            Swal.fire({
                title: 'Error',
                text: data.error || 'Failed to load log',
                icon: 'error',
                customClass: { popup: 'zoho-swal' }
            });
        }
    })
    .catch(error => {
        hideLoader();
        Swal.fire({
            title: 'Error',
            text: 'Failed to load log',
            icon: 'error',
            customClass: { popup: 'zoho-swal' }
        });
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

function showLoader() {
    const loader = document.getElementById('pageLoader');
    if (loader) loader.classList.add('active');
}

function hideLoader() {
    const loader = document.getElementById('pageLoader');
    if (loader) loader.classList.remove('active');
}

// ============================================
// Month Navigation
// ============================================

function navigateMonth(year, month, direction) {
    let newMonth = month + direction;
    let newYear = year;
    
    if (newMonth > 12) {
        newMonth = 1;
        newYear++;
    } else if (newMonth < 1) {
        newMonth = 12;
        newYear--;
    }
    
    window.location.href = `?year=${newYear}&month=${newMonth}`;
}
