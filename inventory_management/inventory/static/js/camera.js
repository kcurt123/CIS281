document.querySelector('#id_name').addEventListener('click', function(event) {
  console.log('Container clicked', event);
}, true); // Using capture phase for logging

document.addEventListener('DOMContentLoaded', (event) => {
   
  const startScanButton = document.getElementById('startScan');
  const stopScanButton = document.getElementById('stopScan');
  const scannerContainer = document.getElementById('scanner-container');
  const barcodeResult = document.getElementById('barcodeResult');

  startScanButton.addEventListener('click', startScanner);
  console.log('start scan clicked');
  stopScanButton.addEventListener('click', stopScanner);

  function startScanner() {
    startScanButton.style.display = 'none';
    stopScanButton.style.display = 'inline-block';

    Quagga.init({
      inputStream: {
        name: 'Live',
        type: 'LiveStream',
        target: scannerContainer,
        constraints: {
          width: 640,
          height: 280,
          facingMode: 'environment'
        }
      },
      decoder: {
        readers: ['ean_reader', 'upc_reader'] // Specify the barcode types to scan
      }
    }, function(err) {
      if (err) {
        console.error(err);
        return;
      }
      console.log('Initialization finished. Ready to start');
      Quagga.start();
    });

    Quagga.onDetected(function(result) {
      const code = result.codeResult.code;
      console.log('Barcode detected:', code);
      document.getElementById('barcodeResult').textContent = 'Barcode detected: ' + code; // Ensure this line is present and correctly setting the text
  
      // Stop the scanner right after a code is detected
      stopScanner();
  
      // Proceed with your fetch request as before
      fetch('/check-item-by-barcode/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify({barcode: code}),
      })
      .then(response => response.json())
      .then(data => {
          if(data.exists) {
              // Existing item logic
              document.getElementById('id_name').value = data.item.name;
              document.getElementById('id_quantity').value = data.item.quantity;
              document.getElementById('id_category').value = data.item.category_id;
              document.getElementById('id_barcode').value = code;
          } else {
              // New item logic
              document.getElementById('id_barcode').value = code;
          }
      })
      .catch((error) => {
          console.error('Error:', error);
      });
  });  
}

  function stopScanner() {
    startScanButton.style.display = 'inline-block';
    stopScanButton.style.display = 'none';

    Quagga.stop();
    Quagga.offDetected();
  }
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
