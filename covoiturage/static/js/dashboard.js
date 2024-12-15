document.addEventListener('DOMContentLoaded', function() {
    // Add table row hover effect
    const tableRows = document.querySelectorAll('.table-hover tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.classList.add('table-active');
        });
        row.addEventListener('mouseleave', function() {
            this.classList.remove('table-active');
        });
    });

    // Add action button hover and click effects
    const actionButtons = document.querySelectorAll('.action-buttons .btn');
    actionButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.opacity = '0.8';
        });
        button.addEventListener('mouseleave', function() {
            this.style.opacity = '1';
        });
    });
});
