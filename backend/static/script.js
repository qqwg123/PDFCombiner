const fileInput = document.getElementById("pdfFiles");
const fileList = document.getElementById("fileList");
const combineDownloadBtn = document.getElementById("combineDownloadBtn");
const clearFilesBtn = document.getElementById("clearFilesBtn");
const statusText = document.getElementById("status");
const dropZone = document.getElementById("dropZone");

let uploadedFiles = [];

fileInput.addEventListener("change", (e) => {
  handleFiles(e.target.files);
  // Reset the input so selecting same files again will re-trigger 'change'
  fileInput.value = "";
});

combineDownloadBtn.addEventListener("click", async () => {
  if (uploadedFiles.length === 0) {
    statusText.textContent = "No files uploaded.";
    return;
  }

  try {
    const filenames = uploadedFiles.map((file) => file.name);

    const res = await fetch("/combine-and-download", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ filenames })
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
    fileInput.value = ""; // Reset file input
    fileList.innerHTML = "";
    statusText.textContent = "Uploaded files cleared.";
  } catch (err) {
    statusText.textContent = err.message;
  }
});




function updateFileList() {
  fileList.innerHTML = "";
  uploadedFiles.forEach((file, index) => {
    const li = document.createElement("li");
    li.textContent = file.name;
    li.draggable = true;
    li.dataset.index = index;

    // Drag events
    li.addEventListener("dragstart", (e) => {
      e.dataTransfer.setData("text/plain", index);
    });

    li.addEventListener("dragover", (e) => {
      e.preventDefault();
      li.style.borderTop = "2px solid #007bff";
    });

    li.addEventListener("dragleave", () => {
      li.style.borderTop = "";
    });

    li.addEventListener("drop", (e) => {
      e.preventDefault();
      li.style.borderTop = "";

      const fromIndex = parseInt(e.dataTransfer.getData("text/plain"));
      const toIndex = index;

      const movedItem = uploadedFiles.splice(fromIndex, 1)[0];
      uploadedFiles.splice(toIndex, 0, movedItem);

      updateFileList();
    });

    fileList.appendChild(li);
  });
}




dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener("change", (e) => {
  handleFiles(e.target.files);
});

async function handleFiles(fileListFromInput) {
  const newFileArray = Array.from(fileListFromInput);

  // Filter out duplicates by filename
  const uniqueNewFiles = newFileArray.filter(newFile =>
    !uploadedFiles.some(existing => existing.name === newFile.name)
  );

  if (uniqueNewFiles.length === 0) {
    statusText.textContent = "Some files were already added and were skipped.";
    return;
  }

  const formData = new FormData();
  for (let file of uniqueNewFiles) {
    formData.append("pdfs", file);
  }

  try {
    const res = await fetch("/upload", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) throw new Error("Upload failed");

    uploadedFiles = [...uploadedFiles, ...uniqueNewFiles];
    updateFileList();
    statusText.textContent = "";
  } catch (err) {
    statusText.textContent = err.message;
  }
}

