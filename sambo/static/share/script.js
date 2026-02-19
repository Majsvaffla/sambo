function getFileItems(e) {
    return [...e.dataTransfer.items].filter(item => item.kind === "file")
}

function preventDefaultDragoverForFiles(e) {
    const fileItems = getFileItems(e)
    if (fileItems.length > 0) {
        e.preventDefault()
        const dropZone = document.getElementById("drop-zone")
        if (!dropZone.contains(e.target)) {
            e.dataTransfer.dropEffect = "none";
        }
    }
}

function handleDragover(e) {
    const fileItems = getFileItems(e)
    if (fileItems.length > 0) {
        e.preventDefault()
        if (fileItems.some(item => item.type.startsWith("image/"))) {
            e.dataTransfer.dropEffect = "copy"
        } else {
            e.dataTransfer.dropEffect = "none"
        }
    }
}

function handleDrop(e, fileInputElement) {
    console.log(fileInputElement)
    console.log(e)
    e.preventDefault()
    if (e.dataTransfer.files.length != 1) {
        return
    }
    fileInputElement.files = e.dataTransfer.files
}

function handleProgress(e, progressRingElement) {
    progressRingElement.setAttribute("value", e.detail.loaded / e.detail.total * 100)
}

window.addEventListener("dragover", preventDefaultDragoverForFiles)
