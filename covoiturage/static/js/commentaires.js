document.addEventListener('DOMContentLoaded', () => {
    const commentaireCards = document.querySelectorAll('.commentaire-card');
    
    commentaireCards.forEach(card => {
        card.addEventListener('mouseover', () => {
            card.classList.add('animate__pulse');
        });
        
        card.addEventListener('mouseout', () => {
            card.classList.remove('animate__pulse');
        });
    });
});