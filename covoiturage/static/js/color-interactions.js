document.addEventListener('DOMContentLoaded', () => {
    // Interactions de couleur dynamiques
    const cards = document.querySelectorAll('.commentaire-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.backgroundColor = 'color-mix(in srgb, var(--primary-color) 10%, white)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.backgroundColor = 'white';
        });
    });
});