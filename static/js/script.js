// Green Sensei Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initializeNavigation();
    initializeForms();
    initializeAnimations();
    initializeMessages();
});

// Navigation functionality
function initializeNavigation() {
    // Highlight active navigation item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Mobile menu toggle (if needed in future)
    // This can be expanded when mobile menu is implemented
}

// Form enhancements
function initializeForms() {
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Form validation feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Add loading states to submit buttons
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitBtn.disabled = true;

                // Re-enable after 3 seconds (fallback)
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    });

    // Password strength indicator for signup
    const passwordField = document.querySelector('input[name="password1"]');
    if (passwordField) {
        passwordField.addEventListener('input', function() {
            updatePasswordStrength(this.value);
        });
    }
}

// Password strength indicator
function updatePasswordStrength(password) {
    let strength = 0;
    let feedback = [];

    if (password.length >= 8) strength++;
    else feedback.push('At least 8 characters');

    if (/[a-z]/.test(password)) strength++;
    else feedback.push('Lowercase letter');

    if (/[A-Z]/.test(password)) strength++;
    else feedback.push('Uppercase letter');

    if (/[0-9]/.test(password)) strength++;
    else feedback.push('Number');

    if (/[^A-Za-z0-9]/.test(password)) strength++;
    else feedback.push('Special character');

    // Update UI (this would need corresponding HTML elements)
    const strengthIndicator = document.querySelector('.password-strength');
    if (strengthIndicator) {
        const strengthText = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'][strength] || 'Very Weak';
        strengthIndicator.textContent = `Password strength: ${strengthText}`;
        strengthIndicator.className = `password-strength strength-${strength}`;
    }
}

// Animation and visual effects
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Add hover effects to interactive elements
    const interactiveElements = document.querySelectorAll('.action-card, .suggestion-btn, .tip-card');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });

        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Message handling
function initializeMessages() {
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                if (message.parentNode) {
                    message.parentNode.removeChild(message);
                }
            }, 300);
        }, 5000);
    });
}

// Utility functions for templates
function showLoading(element) {
    element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    element.disabled = true;
}

function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}

function confirmAction(message) {
    return confirm(message);
}

// Dashboard specific functions
function refreshDashboard() {
    // This would make an AJAX call to refresh dashboard data
    showLoading(document.querySelector('.btn-primary'));
    setTimeout(() => {
        location.reload();
    }, 1000);
}

// Habit management functions
function editHabit(habitId) {
    // Redirect to edit page or open modal
    window.location.href = `/habits/${habitId}/edit/`;
}

function deleteHabit(habitId) {
    if (confirmAction('Are you sure you want to delete this habit? This action cannot be undone.')) {
        // Make AJAX call to delete habit
        const habitElement = document.querySelector(`[data-habit-id="${habitId}"]`);
        if (habitElement) {
            habitElement.style.opacity = '0.5';
            // In a real implementation, make AJAX call here
            setTimeout(() => {
                habitElement.remove();
                showMessage('Habit deleted successfully!', 'success');
            }, 500);
        }
    }
}

// Recommendation functions
function deleteRecommendation(recId) {
    if (confirmAction('Are you sure you want to delete this recommendation?')) {
        const recElement = document.querySelector(`[data-rec-id="${recId}"]`);
        if (recElement) {
            recElement.style.opacity = '0.5';
            setTimeout(() => {
                recElement.remove();
                showMessage('Recommendation deleted successfully!', 'success');
            }, 500);
        }
    }
}

// Message display function
function showMessage(message, type = 'info') {
    const messagesContainer = document.querySelector('.messages') || document.querySelector('.main-content');
    if (messagesContainer) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            ${message}
        `;
        messagesContainer.insertBefore(messageElement, messagesContainer.firstChild);

        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageElement.style.opacity = '0';
            setTimeout(() => {
                if (messageElement.parentNode) {
                    messageElement.parentNode.removeChild(messageElement);
                }
            }, 300);
        }, 5000);
    }
}

// AI Coach functions
function askQuestion(question) {
    const inputField = document.getElementById('userInput');
    if (inputField) {
        inputField.value = question;
        const form = document.getElementById('chatForm');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }
}

// Scroll helpers
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus search (if implemented)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"], input[placeholder*="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }

    // Escape to close modals (if implemented)
    if (e.key === 'Escape') {
        const modal = document.querySelector('.modal.open');
        if (modal) {
            closeModal(modal);
        }
    }
});

// Modal functions (for future use)
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modal) {
    if (modal) {
        modal.classList.remove('open');
        document.body.style.overflow = 'auto';
    }
}

// Export functions for global use
window.GreenSensei = {
    showLoading,
    hideLoading,
    confirmAction,
    showMessage,
    scrollToTop,
    scrollToElement,
    openModal,
    closeModal,
    askQuestion,
    editHabit,
    deleteHabit,
    deleteRecommendation
};