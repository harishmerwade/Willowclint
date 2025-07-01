document.addEventListener('DOMContentLoaded', function() {
    // File input validation
    const fileInput = document.getElementById('videos');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const files = this.files;
            if (files.length > 15) {
                alert('You can upload maximum 15 videos at a time.');
                this.value = '';
            }
        });
    }
});