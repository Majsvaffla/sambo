function getFileItems(data) {
    return [...data.items].filter(item => item.kind === "file")
}

function preventDefaultDragoverForFiles(e) {
    const fileItems = getFileItems(e.dataTransfer)
    if (fileItems.length > 0) {
        e.preventDefault()
        const dropZone = document.getElementById("drop-zone")
        if (!dropZone.contains(e.target)) {
            e.dataTransfer.dropEffect = "none";
        }
    }
}

function handleDragover(e) {
    const fileItems = getFileItems(e.dataTransfer)
    if (fileItems.length > 0) {
        e.preventDefault()
        if (fileItems.some(item => item.type.startsWith("image/"))) {
            e.dataTransfer.dropEffect = "copy"
        } else {
            e.dataTransfer.dropEffect = "none"
        }
    }
}

function handleFiles(files, fileInputElement) {
    if (files.length != 1) {
        return
    }
    fileInputElement.files = files
}

function handleProgress(e) {
    e.currentTarget.setAttribute("value", e.detail.loaded / e.detail.total * 100)
}

window.addEventListener("dragover", preventDefaultDragoverForFiles)
