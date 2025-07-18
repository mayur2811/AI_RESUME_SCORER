// Enhanced AI Resume Analyzer with Dopamine-Triggering Interactions
document.addEventListener('DOMContentLoaded', function() {
    // Initialize magical interactions
    initializeMagicalEffects();
    
    // Initialize tooltips with enhanced styling
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enhanced file upload with celebration
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (validateFileUpload(this)) {
                triggerCelebration(this);
                playSuccessSound();
            }
        });
    });

    // Enhanced form submission with excitement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                handleMagicalFormSubmission(submitBtn);
                createRippleEffect(submitBtn, e);
            }
        });
    });

    // Initialize all magical animations
    animateScores();
    updateProgressIndicators();
    initializeFloatingElements();
    addHoverEffects();
    createParticleSystem();
});

function initializeMagicalEffects() {
    // Add magical cursor trail
    document.addEventListener('mousemove', createCursorTrail);
    
    // Add click ripple effects
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn') || e.target.closest('.btn')) {
            createRippleEffect(e.target.closest('.btn') || e.target, e);
        }
    });
    
    // Add keyboard magic
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            createKeyboardSparkle(e.target);
        }
    });
}

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

function handleMagicalFormSubmission(button) {
    // Create excitement build-up
    button.style.transform = 'scale(0.95)';
    setTimeout(() => {
        button.style.transform = 'scale(1.05)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 100);
    }, 100);
    
    // Disable button and show magical loading state
    button.disabled = true;
    const originalText = button.innerHTML;
    
    // Add magical loading spinner with sparkles
    button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        ✨ Processing Magic... ✨
    `;
    
    // Add pulsing glow effect
    button.style.animation = 'glowPulse 1.5s ease-in-out infinite';
    
    // Add loading class to form
    button.closest('form').classList.add('loading');
    
    // Create floating particles around button
    createLoadingParticles(button);
    
    // Reset after timeout (in case of errors)
    setTimeout(() => {
        button.disabled = false;
        button.innerHTML = originalText;
        button.closest('form').classList.remove('loading');
        button.style.animation = '';
    }, 30000);
}

function createRippleEffect(element, event) {
    const ripple = document.createElement('div');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: radial-gradient(circle, rgba(255,255,255,0.6) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        transform: scale(0);
        animation: ripple 0.6s ease-out;
    `;
    
    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
}

function createCursorTrail(e) {
    const trail = document.createElement('div');
    trail.className = 'magic-cursor';
    trail.style.left = e.clientX + 'px';
    trail.style.top = e.clientY + 'px';
    
    document.body.appendChild(trail);
    
    setTimeout(() => trail.remove(), 1000);
}

function triggerCelebration(element) {
    // Add celebration class
    element.closest('.card, .form-group, .mb-4').classList.add('celebration');
    
    // Create confetti effect
    createConfetti(element);
    
    // Show success message with animation
    showMagicalAlert('File uploaded successfully! ✨', 'success');
    
    // Remove celebration class after animation
    setTimeout(() => {
        element.closest('.card, .form-group, .mb-4').classList.remove('celebration');
    }, 2000);
}

function createConfetti(element) {
    const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#11998e', '#38ef7d'];
    const confettiCount = 30;
    const rect = element.getBoundingClientRect();
    
    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: fixed;
            width: 10px;
            height: 10px;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            left: ${rect.left + Math.random() * rect.width}px;
            top: ${rect.top}px;
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            animation: confettiFall 3s ease-out forwards;
        `;
        
        document.body.appendChild(confetti);
        setTimeout(() => confetti.remove(), 3000);
    }
}

function createLoadingParticles(button) {
    const rect = button.getBoundingClientRect();
    const particleCount = 20;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: fixed;
            width: 4px;
            height: 4px;
            background: #667eea;
            left: ${rect.left + rect.width / 2}px;
            top: ${rect.top + rect.height / 2}px;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            animation: particleFloat 2s ease-out infinite;
            animation-delay: ${i * 0.1}s;
        `;
        
        document.body.appendChild(particle);
        
        setTimeout(() => particle.remove(), 10000);
    }
}

function playSuccessSound() {
    // Create audio context for success sound
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.setValueAtTime(523.25, audioContext.currentTime); // C5
        oscillator.frequency.setValueAtTime(659.25, audioContext.currentTime + 0.1); // E5
        oscillator.frequency.setValueAtTime(783.99, audioContext.currentTime + 0.2); // G5
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.5);
    } catch (e) {
        // Fallback: visual feedback only
        console.log('Audio not supported, using visual feedback only');
    }
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

function showMagicalAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertElement.style.cssText = `
        background: var(--gradient-card);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: bounceIn 0.6s ease-out;
    `;
    alertElement.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alertElement, alertContainer.firstChild);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertElement.parentNode) {
            alertElement.style.animation = 'fadeOut 0.5s ease-out forwards';
            setTimeout(() => alertElement.remove(), 500);
        }
    }, 5000);
}

function showAlert(message, type = 'info') {
    showMagicalAlert(message, type);
}

function initializeFloatingElements() {
    // Create floating background elements
    const icons = ['fas fa-robot', 'fas fa-chart-line', 'fas fa-lightbulb', 'fas fa-star'];
    
    for (let i = 0; i < 4; i++) {
        const element = document.createElement('div');
        element.className = `floating-element ${icons[i]}`;
        element.style.cssText = `
            font-size: 3rem;
            color: rgba(102, 126, 234, 0.1);
            position: fixed;
            pointer-events: none;
            z-index: -1;
        `;
        document.body.appendChild(element);
    }
}

function addHoverEffects() {
    // Add magical hover effects to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.classList.add('feature-card');
        card.style.setProperty('--delay', index);
        
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) rotateX(5deg)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
    
    // Add click effects to icons
    const icons = document.querySelectorAll('.fa-robot, .fa-chart-bar, .fa-briefcase, .fa-upload');
    icons.forEach(icon => {
        icon.classList.add('clickable-icon');
        icon.addEventListener('click', function(e) {
            createSparkles(this);
            playSuccessSound();
        });
    });
}

function createSparkles(element) {
    const rect = element.getBoundingClientRect();
    const sparkleCount = 8;
    
    for (let i = 0; i < sparkleCount; i++) {
        const sparkle = document.createElement('div');
        sparkle.innerHTML = '✨';
        sparkle.style.cssText = `
            position: fixed;
            left: ${rect.left + rect.width / 2}px;
            top: ${rect.top + rect.height / 2}px;
            font-size: 1rem;
            pointer-events: none;
            z-index: 1000;
            animation: sparkleOut 1s ease-out forwards;
            animation-delay: ${i * 0.1}s;
        `;
        
        document.body.appendChild(sparkle);
        setTimeout(() => sparkle.remove(), 1200);
    }
}

function createParticleSystem() {
    // Create ambient particle effects
    setInterval(() => {
        if (Math.random() < 0.3) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: fixed;
                width: 3px;
                height: 3px;
                background: rgba(102, 126, 234, 0.6);
                border-radius: 50%;
                left: ${Math.random() * window.innerWidth}px;
                top: -10px;
                pointer-events: none;
                z-index: -1;
                animation: particleDrift 8s linear forwards;
            `;
            
            document.body.appendChild(particle);
            setTimeout(() => particle.remove(), 8000);
        }
    }, 2000);
}

function createKeyboardSparkle(element) {
    if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
        const rect = element.getBoundingClientRect();
        const sparkle = document.createElement('div');
        sparkle.innerHTML = '⭐';
        sparkle.style.cssText = `
            position: fixed;
            left: ${rect.right - 20}px;
            top: ${rect.top - 10}px;
            font-size: 1.2rem;
            pointer-events: none;
            z-index: 1000;
            animation: sparkle 0.8s ease-out forwards;
        `;
        
        document.body.appendChild(sparkle);
        setTimeout(() => sparkle.remove(), 800);
    }
}

// Legacy function for compatibility
function handleFormSubmission(button) {
    handleMagicalFormSubmission(button);
}

// Add celebration when high scores are achieved
function celebrateHighScore(score) {
    if (score >= 80) {
        createConfetti(document.body);
        showMagicalAlert('🎉 Excellent score! Your resume is fantastic!', 'success');
        playSuccessSound();
    } else if (score >= 70) {
        createSparkles(document.body);
        showMagicalAlert('⭐ Great score! Well done!', 'success');
    }
}

// Enhanced score animation with celebration
function enhancedAnimateScores() {
    const scoreElements = document.querySelectorAll('[data-score]');
    scoreElements.forEach((element, index) => {
        const targetScore = parseInt(element.dataset.score);
        const duration = 2000 + (index * 300); // Stagger animations
        const increment = targetScore / (duration / 16);
        let currentScore = 0;
        
        // Add celebration class if high score
        if (targetScore >= 80) {
            element.closest('.card').classList.add('celebration');
        }
        
        const timer = setInterval(() => {
            currentScore += increment;
            if (currentScore >= targetScore) {
                currentScore = targetScore;
                clearInterval(timer);
                // Trigger celebration for high scores
                if (targetScore >= 80) {
                    setTimeout(() => celebrateHighScore(targetScore), 500);
                }
            }
            element.textContent = Math.floor(currentScore) + '%';
        }, 16);
        
        // Add color based on score
        setTimeout(() => {
            if (targetScore >= 80) {
                element.classList.add('score-excellent');
                element.closest('.card').classList.add('success-glow');
            } else if (targetScore >= 60) {
                element.classList.add('score-good');
            } else if (targetScore >= 40) {
                element.classList.add('score-average');
            } else {
                element.classList.add('score-poor');
                element.closest('.card').classList.add('error-shake');
            }
        }, duration);
    });
}

// Override the original function
function animateScores() {
    enhancedAnimateScores();
}

// Add interactive tooltips with magical effects
function addMagicalTooltips() {
    const tooltipElements = document.querySelectorAll('[title]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            createSparkles(this);
        });
    });
}

// Initialize magical features when page loads
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        addMagicalTooltips();
        // Add magical welcome message
        if (window.location.pathname === '/') {
            setTimeout(() => {
                showMagicalAlert('✨ Welcome to the magical world of AI resume analysis! ✨', 'info');
            }, 1500);
        }
    }, 1000);
});

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
