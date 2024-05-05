
    document.addEventListener("DOMContentLoaded", function() {
        const toggleButton = document.getElementById('toggleNotes');
        const notesColumns = document.querySelectorAll('.notes-column');

        toggleButton.addEventListener('click', function() {
            for (const column of notesColumns) {
                if (column.style.display === 'none') {
                    column.style.display = '';
                } else {
                    column.style.display = 'none';
                }
            }
        });
    });

