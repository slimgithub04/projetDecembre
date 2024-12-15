document.addEventListener('DOMContentLoaded', function() {
    // Fermeture automatique des notifications après 5 secondes
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const bsAlert = new bootstrap.Alert(alert);
        setTimeout(() => {
            bsAlert.close();
        }, 5000);
    });

    // Effet de survol dynamique sur certains éléments
    const hoverLiftElements = document.querySelectorAll('.hover-lift');
    hoverLiftElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.classList.add('shadow-sm');
        });
        
        element.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-sm');
        });
    });

    // Validation de formulaires (exemple générique)
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});