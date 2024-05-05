document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('tbody tr').forEach(row => {
        row.addEventListener('click', function() {
            const cells = this.cells;  // This is more reliable than this.children for targeting table cells directly

            const modalBody = document.querySelector('#itemDetailsModal .modal-body');
            if (modalBody && cells) {  // Check if the modalBody and cells are not null
                modalBody.innerHTML = `
                    <p>PC Name: ${this.dataset.pc_name}</p>
                    <p>Domain User: ${this.dataset.domain_user}</p>
                    <p>Person: ${this.dataset.person}</p>
                    <p>Department: ${this.dataset.department}</p>
                    <p>Device Type: ${this.dataset.device_type}</p>
                    <p>Cost: ${this.dataset.costs}</p>
                    <p>New Computer: ${this.dataset.new_computer}</p>
                    <p>Date Delivered: ${this.dataset.date_delivered}</p>
                    <p>Is Computer: ${this.dataset.is_computer}</p>
                    <p>Has Dock: ${this.dataset.has_dock}</p>
                    <p>Has LCD: ${this.dataset.has_lcd}</p>
                    <p>Has LCD2: ${this.dataset.has_lcd2}</p>
                    <p>Has Stand: ${this.dataset.has_stand}</p>
                    <p>Has Keyboard: ${this.dataset.has_keyboard}</p>
                    <p>Has CD: ${this.dataset.has_cd}</p>
                    <p>Last Checked Out At: ${this.dataset.last_checked_out_at}</p>
                    <p>Model Number: ${this.dataset.model_number}</p>
                    <p>Serial Number: ${this.dataset.serial_number}</p>
                    <p>Supplier: ${this.dataset.supplier}</p>
                    <p>Notes: ${this.dataset.notes}</p>
                `;
                var myModal = new bootstrap.Modal(document.getElementById('itemDetailsModal'));
                myModal.show();
            }
        });
    });
});

