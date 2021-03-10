window.addEventListener('load', () => {
    const newPostTitle = document.getElementById('new-post-title');
    newPostTitle.addEventListener('keyup', (event) => {
        if (newPostTitle.value.startsWith('/')) {
            try {
                const pattern = newPostTitle.value.substring(1).replaceAll('\\','\\\\');
                const re = new RegExp(pattern, 'i');
                const articles = document.getElementsByTagName('article');
                for (let i = 0; i < articles.length; i++) {
                    const article = articles[i];
                    article.style.display = (article.textContent.match(re)) ? 'block' : 'none';
                }
            } catch (error) {
                // probably bad regex ...
            }
        } else {
            const newStyle = (newPostTitle.value == '') ? 'none' : 'block';
            document.getElementById('new-post-body').style.display = newStyle;
            document.getElementById('new-post-save').style.display = newStyle;
        }
    });
});

// upload entries
function preventDefaults (e) {
    e.preventDefault();
    e.stopPropagation();
}
  
function highlight(e) {
    dropArea.classList.add('highlight');
}
  
function unhighlight(e) {
    dropArea.classList.remove('highlight');
}

function uploadFile(file) {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    xhr.open('POST', 'upload', true);
    xhr.addEventListener('readystatechange', function(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('main-home-link').click();
        } else if (xhr.readyState == 4 && xhr.status != 200) {
            console.log('upload failed ...'); // TODO: proper messages
        }
    })
    formData.append('file', file);
    xhr.send(formData);
}

function handleDrop(e) {
    const files = e.dataTransfer.files
    // TODO: if not 1 file -> reject
    uploadFile(files[0]);
}

const dropArea = document.getElementsByTagName('body')[0];
function addListener(eventNames, fn) {
    eventNames.forEach(name => dropArea.addEventListener(name, fn, false))
}
addListener(['dragenter', 'dragover', 'dragleave', 'drop'], preventDefaults);
addListener(['dragenter', 'dragover'], highlight);
addListener(['dragleave', 'drop'], unhighlight);
addListener(['drop'], handleDrop);