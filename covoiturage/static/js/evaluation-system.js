document.addEventListener('DOMContentLoaded', function() {
    // Form Validation
    const evaluationForms = document.querySelectorAll('form.needs-validation');
    evaluationForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Auto-dismiss Alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const bsAlert = new bootstrap.Alert(alert);
        setTimeout(() => {
            bsAlert.close();
        }, 5000);
    });

    // Slider Color Gradient Initialization
    const sliders = document.querySelectorAll('.slider-interactive');
    sliders.forEach(slider => {
        // Ensure sliders have initial color gradient
        updateSliderInteractive(slider);

        // Add real-time color change on input
        slider.addEventListener('input', function() {
            updateSliderInteractive(this);
        });
    });

    // Tooltip Initialization
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // Optional: Prevent form resubmission
    if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href);
    }
});

// Advanced Slider Interactive Function
function updateSliderInteractive(slider) {
    const valueSpan = document.getElementById(slider.name + '-value');
    const maxValue = slider.max === '100' ? 100 : 10;
    
    // Update value display
    valueSpan.textContent = `${slider.value}/${maxValue}`;
    
    // Dynamic color gradient calculation
    const percentage = (slider.value - slider.min) / (slider.max - slider.min) * 100;
    
    // Color mapping based on slider value
    let colorStart, colorEnd;
    if (percentage < 33) {
        colorStart = '#dc3545';  // Red for low values
        colorEnd = '#ffc107';    // Yellow transition
    } else if (percentage < 66) {
        colorStart = '#ffc107';  // Yellow for medium values
        colorEnd = '#28a745';    // Green transition
    } else {
        colorStart = '#28a745';  // Green for high values
        colorEnd = '#007bff';    // Blue transition
    }
    
    // Apply dynamic gradient
    slider.style.background = `linear-gradient(to right, 
        ${colorStart} 0%, 
        ${colorStart} ${percentage}%, 
        ${colorEnd} ${percentage}%, 
        ${colorEnd} 100%)`;
    
    // Optional: Add visual feedback
    slider.classList.add('active');
    setTimeout(() => {
        slider.classList.remove('active');
    }, 300);
}

// Optional: Form Data Validation with Real-time Feedback
function validateFormData() {
    const sliders = document.querySelectorAll('.slider-interactive');
    const submitButton = document.querySelector('button[type="submit"]');
    
    let isValid = true;
    
    sliders.forEach(slider => {
        const value = parseInt(slider.value);
        
        if (value < 0 || value > (slider.max === '100' ? 100 : 10)) {
            slider.classList.add('is-invalid');
            isValid = false;
        } else {
            slider.classList.remove('is-invalid');
        }
    });
    
    // Disable/Enable submit button based on validation
    submitButton.disabled = !isValid;
    
    return isValid;
}