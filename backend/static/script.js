const fileInput = document.getElementById("pdfFiles");
const fileList = document.getElementById("fileList");
const combineDownloadBtn = document.getElementById("combineDownloadBtn");
const clearFilesBtn = document.getElementById("clearFilesBtn");
const statusText = document.getElementById("status");
const dropZone = document.getElementById("dropZone");

let uploadedFiles = [];

/**
 * Updates the status message with appropriate styling
 * @param {string} message - The message to display
 * @param {string} type - The type of message ('success', 'error', 'info', 'warning')
 * @param {number} timeout - Time in ms before message disappears (0 = no timeout)
 */
function updateStatus(message, type = 'info', timeout = 0) {
  const statusText = document.getElementById("status");
  
  // Remove all existing classes
  statusText.classList.remove('error', 'success', 'info', 'warning');
  
  // Add the appropriate class
  statusText.classList.add(type);
  
  // Set the message text
  statusText.textContent = message;
  
  // Clear after timeout if specified
  if (timeout > 0) {
    setTimeout(() => {
      if (statusText.textContent === message) {
        statusText.textContent = "";
        statusText.classList.remove('error', 'success', 'info', 'warning');
      }
    }, timeout);
  }
}

fileInput.addEventListener("change", (e) => {
  handleFiles(e.target.files);
  // Reset the input so selecting same files again will re-trigger 'change'
  fileInput.value = "";
});

combineDownloadBtn.addEventListener("click", async () => {
  if (uploadedFiles.length === 0) {
    updateStatus("No files uploaded.", "warning");
    return;
  }
  
  if (uploadedFiles.length === 1) {
    updateStatus("You need at least 2 PDF files to combine.", "warning");
    return;
  }

  // Show "combining" status
  updateStatus("Combining PDFs...", "info");
  
  try {
    const filenames = uploadedFiles.map((file) => file.name);

    const res = await fetch("/combine-and-download", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ filenames })
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.error || "Failed to combine PDFs");
    }

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "combined.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    
    // Success message
    updateStatus("PDFs combined successfully!", "success", 10000);
  } catch (err) {
    updateStatus(err.message, "error");
  }
});

clearFilesBtn.addEventListener("click", async () => {
  try {
    updateStatus("Clearing files...", "info");
    
    const res = await fetch("/clear-files", {
      method: "POST"
    });

    if (!res.ok) throw new Error("Failed to clear files");

    uploadedFiles = [];
    fileInput.value = ""; // Reset file input
    fileList.innerHTML = "";
    updateStatus("Uploaded files cleared.", "success", 5000);
  } catch (err) {
    updateStatus(err.message, "error");
  }
});

function updateFileList() {
  fileList.innerHTML = "";
  
  if (uploadedFiles.length === 0) {
    fileList.innerHTML = "<li class='empty-list'>No files added yet</li>";
    return;
  }
  
  uploadedFiles.forEach((file, index) => {
    const li = document.createElement("li");
    li.setAttribute("data-index", index);
    
    // File info container
    const fileInfo = document.createElement("div");
    fileInfo.className = "file-info";
    
    // PDF icon
    const icon = document.createElement("span");
    icon.className = "icon";
    icon.textContent = "📄";
    fileInfo.appendChild(icon);
    
    // File name
    const fileName = document.createElement("span");
    fileName.className = "file-name";
    fileName.textContent = file.name;
    fileName.title = file.name; // Show full name on hover
    fileInfo.appendChild(fileName);
    
    // Add file size
    const fileSize = document.createElement("span");
    fileSize.className = "file-size";
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.appendChild(fileSize);
    
    li.appendChild(fileInfo);
    
    // Actions container
    const actions = document.createElement("div");
    actions.className = "file-actions";
    
    // Delete button
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "delete-file";
    deleteBtn.innerHTML = "×";
    deleteBtn.title = "Remove file";
    deleteBtn.addEventListener("click", () => {
      uploadedFiles.splice(index, 1);
      updateFileList();
    });
    actions.appendChild(deleteBtn);
    
    li.appendChild(actions);
    
    // Drag functionality
    li.draggable = true;
    
    li.addEventListener("dragstart", (e) => {
      e.dataTransfer.setData("text/plain", index);
    });

    li.addEventListener("dragover", (e) => {
      e.preventDefault();
      li.classList.add("drag-over");
    });

    li.addEventListener("dragleave", () => {
      li.classList.remove("drag-over");
    });

    li.addEventListener("drop", (e) => {
      e.preventDefault();
      li.classList.remove("drag-over");

      const fromIndex = parseInt(e.dataTransfer.getData("text/plain"));
      const toIndex = index;
      
      if (fromIndex !== toIndex) {
        const movedItem = uploadedFiles.splice(fromIndex, 1)[0];
        uploadedFiles.splice(toIndex, 0, movedItem);
        updateFileList();
      }
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

function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

async function handleFiles(fileListFromInput) {
  const newFileArray = Array.from(fileListFromInput);
  
  // Filter for PDF files only
  const pdfFiles = newFileArray.filter(file => 
    file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
  );
  
  if (pdfFiles.length === 0) {
    updateStatus("Please select PDF files only.", "error");
    return;
  }
  
  if (newFileArray.length !== pdfFiles.length) {
    updateStatus("Some non-PDF files were skipped.", "warning");
  }

  // Filter out duplicates by filename
  const uniqueNewFiles = pdfFiles.filter(newFile =>
    !uploadedFiles.some(existing => existing.name === newFile.name)
  );

  if (uniqueNewFiles.length === 0) {
    updateStatus("These files were already added and were skipped.", "warning");
    return;
  }

  updateStatus("Uploading files...", "info");

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
    statusText.textContent = `${uniqueNewFiles.length} file(s) uploaded successfully.`;
    
    // Clear success message after a few seconds
    updateStatus(`${uniqueNewFiles.length} file(s) uploaded successfully.`, "success", 10000);
  } catch (err) {
    updateStatus(err.message, "error");
  }
}

// Initialize file list in case there are any
updateFileList();