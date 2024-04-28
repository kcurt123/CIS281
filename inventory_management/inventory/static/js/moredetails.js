document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('tbody tr').forEach(row => {
        row.addEventListener('click', function() {
            const cells = this.cells;  // This is more reliable than this.children for targeting table cells directly

            const modalBody = document.querySelector('#itemDetailsModal .modal-body');
            if (modalBody && cells) {  // Check if the modalBody and cells are not null
                modalBody.innerHTML = `
                    <p>ID: ${this.cells[0].innerText}</p>
                    <p>PC Name: ${this.cells[1].innerText}</p>
                    <p>Department: ${this.cells[2].innerText}</p>
                    <p>Model Number: ${this.cells[3].innerText}</p>
                    <p>Serial Number: ${this.cells[4].innerText}</p>
                    <p>Notes: ${this.cells[5].innerText}</p>
                    <p>Supplier: ${this.cells[6].innerText}</p>
                    <p>Status: ${this.cells[7].innerText}</p>
                    <p>Domain User: ${this.dataset.domain_user}</p>
                    <p>Device Type: ${this.dataset.device_type}</p>
                    <p>Costs: ${this.dataset.costs}</p>
                    <p>Date Delivered: ${this.dataset.date_delivered}</p>
                    <p>Is Computer: ${this.dataset.is_computer}</p>
                    <p>New Computer: ${this.dataset.new_computer}</p>
                    <p>Has Dock: ${this.dataset.has_dock}</p>
                    <p>Has LCD: ${this.dataset.has_lcd}</p>
                    <p>Has LCD2: ${this.dataset.has_lcd2}</p>
                    <p>Has Stand: ${this.dataset.has_stand}</p>
                    <p>Has Keyboard: ${this.dataset.has_keyboard}</p>
                    <p>Has CD: ${this.dataset.has_cd}</p>
                    <p>Last Checked Out At: ${this.dataset.last_checked_out_at || 'N/A'} </p>

                `;
                var myModal = new bootstrap.Modal(document.getElementById('itemDetailsModal'));
                myModal.show();
            }
        });
    });
});

