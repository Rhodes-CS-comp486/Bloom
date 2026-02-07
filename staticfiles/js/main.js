// ========================================
// BLOOM - Main JavaScript
// ========================================

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  initializeApp();
});

function initializeApp() {
  // Initialize components
  initMoodSelector();
  initCheckInForm();
  initAlerts();
}

// ========================================
// MOOD SELECTOR
// ========================================
function initMoodSelector() {
  const moodOptions = document.querySelectorAll('.mood-option');
  const moodInput = document.getElementById('mood-input');
  
  if (!moodOptions.length || !moodInput) return;
  
  moodOptions.forEach(option => {
    option.addEventListener('click', (e) => {
      e.preventDefault();
      
      // Remove active state from all options
      moodOptions.forEach(opt => opt.classList.remove('active'));
      
      // Add active state to clicked option
      option.classList.add('active');
      
      // Update hidden input value
      const mood = option.dataset.mood;
      moodInput.value = mood;
    });
  });
}

// ========================================
// CHECK-IN FORM ENHANCEMENTS
// ========================================
function initCheckInForm() {
  const form = document.querySelector('.check-in-form');
  if (!form) return;
  
  // Auto-save draft to localStorage
  const inputs = form.querySelectorAll('input, textarea');
  inputs.forEach(input => {
    // Load saved draft
    const savedValue = localStorage.getItem(`checkin_${input.name}`);
    if (savedValue && input.type !== 'radio' && input.type !== 'checkbox') {
      input.value = savedValue;
    }
    
    // Save on change
    input.addEventListener('change', () => {
      if (input.type !== 'radio' && input.type !== 'checkbox') {
        localStorage.setItem(`checkin_${input.name}`, input.value);
      }
    });
  });
  
  // Clear draft on successful submit
  form.addEventListener('submit', () => {
    inputs.forEach(input => {
      localStorage.removeItem(`checkin_${input.name}`);
    });
  });
}

// ========================================
// ALERTS & MESSAGES
// ========================================
function initAlerts() {
  const alerts = document.querySelectorAll('.alert');
  
  alerts.forEach(alert => {
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      fadeOut(alert);
    }, 5000);
    
    // Add close button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'alert-close';
    closeBtn.innerHTML = '×';
    closeBtn.setAttribute('aria-label', 'Close');
    closeBtn.addEventListener('click', () => fadeOut(alert));
    
    alert.appendChild(closeBtn);
  });
}

function fadeOut(element) {
  element.style.opacity = '0';
  setTimeout(() => {
    element.style.display = 'none';
  }, 300);
}

// ========================================
// UTILITIES
// ========================================

// Format date
function formatDate(date) {
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  return date.toLocaleDateString('en-US', options);
}

// Get CSRF token for AJAX requests
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Show loading state
function showLoading(button) {
  button.disabled = true;
  button.dataset.originalText = button.textContent;
  button.textContent = 'Loading...';
}

function hideLoading(button) {
  button.disabled = false;
  button.textContent = button.dataset.originalText;
}

// Toast notifications
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.classList.add('show');
  }, 100);
  
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 300);
  }, 3000);
}

// Debounce function for search/input
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ========================================
// EXPORT FOR OTHER MODULES
// ========================================
window.BloomApp = {
  getCookie,
  showLoading,
  hideLoading,
  showToast,
  debounce,
  formatDate
};
