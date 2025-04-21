document.getElementById('pdfFiles').addEventListener('change', function () {
  const files = this.files;
  if (!files.length) return alert("No files selected!");

  const formData = new FormData();
  for (const file of files) {
      formData.append('pdfs', file);
  }

  fetch('/upload', {
      method: 'POST',
      body: formData,
  })
  .then(response => response.json())
  .then(data => alert(data.message))
  .catch(() => alert('Error uploading files.'));
});

document.getElementById('combineBtn').addEventListener('click', function () {
  fetch('/combine', {
      method: 'POST',
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          alert('PDFs successfully combined! Click download.');
      } else {
          alert(`Error: ${data.message}`);
      }
  })
  .catch(() => alert('Error combining PDFs.'));
});

document.getElementById('downloadBtn').addEventListener('click', function () {
  window.location.href = '/download';
});
