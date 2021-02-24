window.addEventListener('load', () => {
    newPostTitle = document.getElementById('new-post-title')
    newPostTitle.addEventListener('keyup', (event) => {
        newStyle = (newPostTitle.value == '') ? 'none' : 'block'
        document.getElementById('new-post-body').style.display = newStyle
        document.getElementById('new-post-save').style.display = newStyle
    })
});