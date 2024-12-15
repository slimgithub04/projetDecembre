document.addEventListener('DOMContentLoaded', function() {
    const reclamationForm = document.getElementById('reclamationForm');
    const participationRadios = document.querySelectorAll('input[name="statut_participation"]');
    const groupeSelection = document.getElementById('groupe_selection');
    const temoinRadios = document.querySelectorAll('input[name="temoin_option"]');
    const temoinDetails = document.getElementById('temoin_details');

    // Group Selection Toggle
    participationRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            groupeSelection.style.display = this.value === 'groupe' ? 'block' : 'none';
            groupeSelection.classList.toggle('animate__animated', true);
            groupeSelection.classList.toggle('animate__fadeIn', true);
        });
    });

    // Witness Details Toggle
    temoinRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            temoinDetails.style.display = this.value === 'oui' ? 'block' : 'none';
            temoinDetails.classList.toggle('animate__animated', true);
            temoinDetails.classList.toggle('animate__fadeIn', true);
        });
    });

    // Basic Client-Side Validation
    reclamationForm.addEventListener('submit', function(event) {
        let isValid = true;
        const requiredFields = reclamationForm.querySelectorAll('[required]');

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });

        // File Size Validation
        const fileInput = document.querySelector('input[type="file"]');
        if (fileInput.files.length > 0) {
            const fileSize = fileInput.files[0].size / 1024 / 1024; // in MB
            if (fileSize > 5) {
                alert('La taille du fichier ne doit pas dépasser 5 Mo');
                event.preventDefault();
                isValid = false;
            }
        }

        if (!isValid) {
            event.preventDefault();
            const firstInvalidField = reclamationForm.querySelector('.is-invalid');
            firstInvalidField.focus();
        }
    });

    // Dynamic File Input Label
    const fileInput = document.querySelector('input[type="file"]');
    fileInput.addEventListener('change', function() {
        const fileName = this.files.length > 0 ? this.files[0].name : 'Aucun fichier sélectionné';
        const fileLabel = this.nextElementSibling;
        fileLabel.textContent = fileName;
    });
});