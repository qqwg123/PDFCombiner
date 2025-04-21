const fileInput = document.getElementById("pdfFiles");
const fileList = document.getElementById("fileList");
const combineDownloadBtn = document.getElementById("combineDownloadBtn");
const clearFilesBtn = document.getElementById("clearFilesBtn");
const statusText = document.getElementById("status");

let uploadedFiles = [];

fileInput.addEventListener("change", async (event) => {
  const files = event.target.files;
  if (!files.length) return;

  const formData = new FormData();
  for (let file of files) {
    formData.append("pdfs", file);
  }

  try {
    const res = await fetch("/upload", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      throw new Error("Upload failed");
    }

    uploadedFiles = [...files];
    updateFileList();
  } catch (err) {
    statusText.textContent = err.message;
  }
});

combineDownloadBtn.addEventListener("click", async () => {
  if (uploadedFiles.length === 0) {
    statusText.textContent = "No files uploaded.";
    return;
  }

  try {
    const res = await fetch("/combine-and-download", {
      method: "POST"
    });

    if (!res.ok) throw new Error("Failed to combine PDFs");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "combined.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (err) {
    statusText.textContent = err.message;
  }
});


clearFilesBtn.addEventListener("click", async () => {
  try {
    const res = await fetch("/clear-files", {
      method: "POST"
    });

    if (!res.ok) throw new Error("Failed to clear files");

    uploadedFiles = [];
    fileList.innerHTML = "";
    statusText.textContent = "Uploaded files cleared.";
  } catch (err) {
    statusText.textContent = err.message;
  }
});



function updateFileList() {
  fileList.innerHTML = "";
  uploadedFiles.forEach((file) => {
    const li = document.createElement("li");
    li.textContent = file.name;
    fileList.appendChild(li);
  });
}
