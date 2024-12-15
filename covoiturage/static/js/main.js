document.addEventListener('DOMContentLoaded', function() {
    const slider = document.getElementById('note-slider');
    const slider1 = document.getElementById('note-slider1');
    const slider2 = document.getElementById('note-slider2');
    
    // Initial color setup and event listener for 'Confort du trajet'
    if (slider) {
        updateValue(slider.value);
        slider.addEventListener('input', function() {
            updateValue(this.value);
        });
    }

    // Initial color setup and event listener for 'Ponctualité'
    if (slider1) {
        updateValue1(slider1.value);
        slider1.addEventListener('input', function() {
            updateValue1(this.value);
        });
    }

    // Initial color setup and event listener for 'Communication'
    if (slider2) {
        updateValue2(slider2.value);
        slider2.addEventListener('input', function() {
            updateValue2(this.value);
        });
    }

    // Optional: Form validation
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const slider = document.getElementById('note-slider');
            if (!slider.value) {
                event.preventDefault();
                alert('Veuillez sélectionner une note.');
            }
        });
    }
});
