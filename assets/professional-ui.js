/**
 * Professional UI Utilities for AquaWise
 * Toast notifications, loading spinners, confirmations
 */

// Toast Notification System
const Toast = {
    container: null,

    init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    },

    show(message, type = 'info', duration = 4000) {
        this.init();

        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };

        const titles = {
            success: 'Success',
            error: 'Error',
            warning: 'Warning',
            info: 'Information'
        };

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="toast-icon">${icons[type]}</div>
            <div class="toast-content">
                <div class="toast-title">${titles[type]}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close">×</button>
        `;

        this.container.appendChild(toast);

        // Close button
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.onclick = () => this.remove(toast);

        // Auto remove
        if (duration > 0) {
            setTimeout(() => this.remove(toast), duration);
        }

        return toast;
    },

    remove(toast) {
        toast.classList.add('removing');
        setTimeout(() => toast.remove(), 300);
    },

    success(message, duration) {
        return this.show(message, 'success', duration);
    },

    error(message, duration) {
        return this.show(message, 'error', duration);
    },

    warning(message, duration) {
        return this.show(message, 'warning', duration);
    },

    info(message, duration) {
        return this.show(message, 'info', duration);
    }
};

// Loading Spinner
const Loading = {
    overlay: null,

    show(message = 'Processing...') {
        if (this.overlay) return;

        this.overlay = document.createElement('div');
        this.overlay.className = 'spinner-overlay';
        this.overlay.innerHTML = `
            <div class="spinner-content">
                <div class="spinner"></div>
                <div class="spinner-text">${message}</div>
            </div>
        `;

        document.body.appendChild(this.overlay);
        document.body.style.overflow = 'hidden';
    },

    hide() {
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
            document.body.style.overflow = '';
        }
    },

    update(message) {
        if (this.overlay) {
            const text = this.overlay.querySelector('.spinner-text');
            if (text) text.textContent = message;
        }
    }
};

// Multi-Step Progress Bar
const ProgressSteps = {
    overlay: null,
    currentStep: 0,
    steps: [],

    show(steps) {
        if (this.overlay) return;

        this.steps = steps;
        this.currentStep = 0;

        this.overlay = document.createElement('div');
        this.overlay.className = 'spinner-overlay';
        this.overlay.innerHTML = `
            <div class="progress-container">
                <div class="progress-steps" id="progress-steps"></div>
                <div class="progress-bar-container">
                    <div class="progress-bar" id="progress-bar"></div>
                </div>
                <div class="progress-message" id="progress-message"></div>
            </div>
        `;

        document.body.appendChild(this.overlay);
        document.body.style.overflow = 'hidden';

        this.renderSteps();
        this.start();
    },

    renderSteps() {
        const container = this.overlay.querySelector('#progress-steps');
        container.innerHTML = this.steps.map((step, index) => `
            <div class="progress-step ${index === 0 ? 'active' : ''}" data-step="${index}">
                <div class="step-icon">${step.icon}</div>
                <div class="step-label">${step.label}</div>
            </div>
        `).join('');
    },

    async start() {
        for (let i = 0; i < this.steps.length; i++) {
            await this.goToStep(i);
            if (i < this.steps.length - 1) {
                await this.delay(this.steps[i].duration || 800);
            }
        }
    },

    async goToStep(index) {
        this.currentStep = index;
        const step = this.steps[index];

        // Update step classes
        const stepElements = this.overlay.querySelectorAll('.progress-step');
        stepElements.forEach((el, i) => {
            el.classList.remove('active', 'completed');
            if (i < index) el.classList.add('completed');
            if (i === index) el.classList.add('active');
        });

        // Update progress bar
        const progress = ((index + 1) / this.steps.length) * 100;
        const progressBar = this.overlay.querySelector('#progress-bar');
        progressBar.style.width = progress + '%';

        // Update message
        const messageEl = this.overlay.querySelector('#progress-message');
        messageEl.textContent = step.label;
    },

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    hide() {
        if (this.overlay) {
            this.overlay.style.opacity = '0';
            setTimeout(() => {
                if (this.overlay) {
                    this.overlay.remove();
                    this.overlay = null;
                    document.body.style.overflow = '';
                }
            }, 300);
        }
    }
}

// Confirmation Dialog
function showConfirmation(options) {
    return new Promise((resolve) => {
        const {
            title = 'Are you sure?',
            message = 'This action cannot be undone.',
            confirmText = 'Confirm',
            cancelText = 'Cancel',
            type = 'warning'
        } = options;

        const icons = {
            warning: '⚠️',
            danger: '🗑️',
            info: 'ℹ️'
        };

        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';
        overlay.innerHTML = `
            <div class="confirmation-modal">
                <div class="modal-icon ${type}">
                    ${icons[type] || icons.warning}
                </div>
                <h3 class="modal-title">${title}</h3>
                <p class="modal-text">${message}</p>
                <div class="modal-actions">
                    <button class="modal-btn modal-btn-cancel">${cancelText}</button>
                    <button class="modal-btn modal-btn-confirm">${confirmText}</button>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        const modal = overlay.querySelector('.confirmation-modal');
        const cancelBtn = overlay.querySelector('.modal-btn-cancel');
        const confirmBtn = overlay.querySelector('.modal-btn-confirm');

        const cleanup = () => {
            overlay.style.opacity = '0';
            setTimeout(() => overlay.remove(), 200);
        };

        cancelBtn.onclick = () => {
            cleanup();
            resolve(false);
        };

        confirmBtn.onclick = () => {
            cleanup();
            resolve(true);
        };

        overlay.onclick = (e) => {
            if (e.target === overlay) {
                cleanup();
                resolve(false);
            }
        };
    });
}

// Form Validation Helper
function validateField(input, rules) {
    const value = input.value.trim();
    let isValid = true;
    let errorMessage = '';

    // Required
    if (rules.required && !value) {
        isValid = false;
        errorMessage = 'This field is required';
    }

    // Email
    if (rules.email && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email';
        }
    }

    // Min length
    if (rules.minLength && value.length < rules.minLength) {
        isValid = false;
        errorMessage = `Minimum ${rules.minLength} characters required`;
    }

    // Pattern
    if (rules.pattern && value) {
        if (!rules.pattern.test(value)) {
            isValid = false;
            errorMessage = rules.patternMessage || 'Invalid format';
        }
    }

    // Update UI
    input.classList.remove('valid', 'invalid');
    input.classList.add(isValid ? 'valid' : 'invalid');

    // Show/hide error message
    let errorDiv = input.parentElement.querySelector('.field-error');
    if (!isValid && errorMessage) {
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'field-error';
            input.parentElement.appendChild(errorDiv);
        }
        errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${errorMessage}`;
    } else if (errorDiv) {
        errorDiv.remove();
    }

    return isValid;
}

// Input Prompt Dialog
function showPrompt(options) {
    return new Promise((resolve) => {
        const {
            title = 'Input Required',
            message = 'Please enter a value:',
            placeholder = '',
            confirmText = 'OK',
            cancelText = 'Cancel',
            inputType = 'text',
            required = true
        } = options;

        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';
        overlay.innerHTML = `
            <div class="confirmation-modal">
                <div class="modal-icon warning">
                    ⚠️
                </div>
                <h3 class="modal-title">${title}</h3>
                <p class="modal-text">${message}</p>
                <input type="${inputType}" class="prompt-input" placeholder="${placeholder}" 
                       style="width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 14px; margin-bottom: 16px; outline: none; transition: border-color 0.2s;">
                <div class="modal-actions">
                    <button class="modal-btn modal-btn-cancel">${cancelText}</button>
                    <button class="modal-btn modal-btn-confirm">${confirmText}</button>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        const input = overlay.querySelector('.prompt-input');
        const cancelBtn = overlay.querySelector('.modal-btn-cancel');
        const confirmBtn = overlay.querySelector('.modal-btn-confirm');

        // Focus input
        setTimeout(() => input.focus(), 100);

        // Input validation styling
        input.addEventListener('input', () => {
            if (input.value.trim()) {
                input.style.borderColor = '#10b981';
            } else {
                input.style.borderColor = '#e5e7eb';
            }
        });

        const cleanup = () => {
            overlay.style.opacity = '0';
            setTimeout(() => overlay.remove(), 200);
        };

        const handleConfirm = () => {
            const value = input.value.trim();
            if (required && !value) {
                input.style.borderColor = '#ef4444';
                input.focus();
                return;
            }
            cleanup();
            resolve(value || null);
        };

        cancelBtn.onclick = () => {
            cleanup();
            resolve(null);
        };

        confirmBtn.onclick = handleConfirm;

        // Enter key submits
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleConfirm();
            }
        });

        // Escape key cancels
        overlay.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                cleanup();
                resolve(null);
            }
        });

        overlay.onclick = (e) => {
            if (e.target === overlay) {
                cleanup();
                resolve(null);
            }
        };
    });
}

// Smooth scroll to element
function smoothScrollTo(element) {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
}

// Make functions globally available
window.Toast = Toast;
window.Loading = Loading;
window.ProgressSteps = ProgressSteps;
window.showConfirmation = showConfirmation;
window.showPrompt = showPrompt;
window.validateField = validateField;
window.smoothScrollTo = smoothScrollTo;
