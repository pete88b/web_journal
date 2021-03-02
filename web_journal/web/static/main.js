window.addEventListener('load', () => {
    newPostTitle = document.getElementById('new-post-title')
    newPostTitle.addEventListener('keyup', (event) => {
        newStyle = (newPostTitle.value == '') ? 'none' : 'block'
        document.getElementById('new-post-body').style.display = newStyle
        document.getElementById('new-post-save').style.display = newStyle
    })
});

// upload entries
let dropArea = document.getElementsByTagName('body')[0]
function preventDefaults (e) {
    e.preventDefault()
    e.stopPropagation()
}

;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
})

;['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false)
})
  
;['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false)
})
  
function highlight(e) {
    dropArea.classList.add('highlight')
}
  
function unhighlight(e) {
    dropArea.classList.remove('highlight')
}
  
dropArea.addEventListener('drop', handleDrop, false)

function uploadFile(file) {
    var xhr = new XMLHttpRequest()
    var formData = new FormData()
    xhr.open('POST', 'upload', true)
    xhr.addEventListener('readystatechange', function(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('main-home-link').click()
        } else if (xhr.readyState == 4 && xhr.status != 200) {
            console.log('upload failed ...') // TODO: proper messages
        }
    })
    formData.append('file', file)
    xhr.send(formData)
}

function handleDrop(e) {
    let files = e.dataTransfer.files
    // if not 1 file -> reject
    uploadFile(files[0])
}