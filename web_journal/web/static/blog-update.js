function resizeOnInput() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
}
const textareas = document.getElementsByTagName('textarea');
for (let i = 0; i < textareas.length; i++) {
    textarea=textareas[i]
    textarea.setAttribute('style', 'height:' + (textarea.scrollHeight) + 'px; overflow-y:hidden;');
    textarea.addEventListener('input', resizeOnInput, false);
}