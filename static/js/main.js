// Main JavaScript for AI Resume Analyzer
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // File upload validation
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            validateFileUpload(this);
        });
    });

    // Form submission handling
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                handleFormSubmission(submitBtn);
            }
        });
    });

    // Score animation
    animateScores();

    // Progress indicators
    updateProgressIndicators();
});

function validateFileUpload(input) {
    const file = input.files[0];
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['.pdf', '.docx', '.doc'];
    
    if (file) {
        // Check file size
        if (file.size > maxSize) {
            showAlert('File size must be less than 16MB', 'error');
            input.value = '';
            return false;
        }
        
        // Check file type
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        if (!allowedTypes.includes(fileExtension)) {
            showAlert('Please upload a PDF or DOCX file', 'error');
            input.value = '';
            return false;
        }
        
        return true;
    }
    return false;
}

function handleFormSubmission(button) {
    // Disable button and show loading state
    button.disabled = true;
    const originalText = button.innerHTML;
    
    // Add loading spinner
    button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        Processing...
    `;
    
    // Add loading class to form
    button.closest('form').classList.add('loading');
    
    // Reset after timeout (in case of errors)
    setTimeout(() => {
        button.disabled = false;
        button.innerHTML = originalText;
        button.closest('form').classList.remove('loading');
    }, 30000); // 30 seconds timeout
}

function animateScores() {
    const scoreElements = document.querySelectorAll('[data-score]');
    scoreElements.forEach(element => {
        const targetScore = parseInt(element.dataset.score);
        const duration = 2000; // 2 seconds
        const increment = targetScore / (duration / 16); // 60fps
        let currentScore = 0;
        
        const timer = setInterval(() => {
            currentScore += increment;
            if (currentScore >= targetScore) {
                currentScore = targetScore;
                clearInterval(timer);
            }
            element.textContent = Math.floor(currentScore);
        }, 16);
        
        // Add color based on score
        if (targetScore >= 80) {
            element.classList.add('score-excellent');
        } else if (targetScore >= 60) {
            element.classList.add('score-good');
        } else if (targetScore >= 40) {
            element.classList.add('score-average');
        } else {
            element.classList.add('score-poor');
        }
    });
}

function updateProgressIndicators() {
    const progressBars = document.querySelectorAll('.progress-bar[data-progress]');
    progressBars.forEach(bar => {
        const progress = parseInt(bar.dataset.progress);
        setTimeout(() => {
            bar.style.width = progress + '%';
        }, 500);
    });
}

function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertElement.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alertElement, alertContainer.firstChild);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertElement.parentNode) {
            alertElement.remove();
        }
    }, 5000);
}

// Utility functions for dynamic content
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function getScoreColor(score) {
    if (score >= 80) return 'success';
    if (score >= 60) return 'info';
    if (score >= 40) return 'warning';
    return 'danger';
}

function getScoreIcon(score) {
    if (score >= 80) return 'fas fa-star';
    if (score >= 60) return 'fas fa-thumbs-up';
    if (score >= 40) return 'fas fa-meh';
    return 'fas fa-thumbs-down';
}

// Export functions for use in other scripts
window.ResumeAnalyzer = {
    validateFileUpload,
    handleFormSubmission,
    animateScores,
    showAlert,
    formatFileSize,
    getScoreColor,
    getScoreIcon
};

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Handle keyboard navigation
document.addEventListener('keydown', function(e) {
    // ESC key to close modals/alerts
    if (e.key === 'Escape') {
        const alerts = document.querySelectorAll('.alert .btn-close');
        alerts.forEach(close => close.click());
    }
});
