document.addEventListener('DOMContentLoaded', () => {
    const commentaireCards = document.querySelectorAll('.commentaire-card');
    const editButtons = document.querySelectorAll('.edit-btn');
    const deleteButtons = document.querySelectorAll('.delete-btn');
    
    // Animations et interactions des cartes
    commentaireCards.forEach(card => {
        card.addEventListener('mouseover', () => {
            card.classList.add('animate__pulse');
        });
        
        card.addEventListener('mouseout', () => {
            card.classList.remove('animate__pulse');
        });
    });

    // Gestion des boutons d'édition (à personnaliser selon vos besoins)
    editButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const commentaireId = e.currentTarget.dataset.id;
            // Logique d'édition à implémenter
            console.log(`Éditer le commentaire ${commentaireId}`);
        });
    });

    // Gestion des boutons de suppression (à personnaliser)
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const commentaireId = e.currentTarget.dataset.id;
            if(confirm('Êtes-vous sûr de vouloir supprimer ce commentaire ?')) {
                // Logique de suppression à implémenter
                console.log(`Supprimer le commentaire ${commentaireId}`);
            }
        });
    });
});