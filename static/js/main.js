document.addEventListener('DOMContentLoaded', () => {
    // File input name display
    const fileInput = document.getElementById('video');
    const fileNameDisplay = document.getElementById('fileName');

    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                fileNameDisplay.textContent = e.target.files[0].name;
            } else {
                fileNameDisplay.textContent = 'Choose File';
            }
        });
    }

    // Form submission spinner
    const uploadForm = document.getElementById('uploadForm');
    const loadingDiv = document.getElementById('loading');
    const splitBtn = document.getElementById('splitBtn');

    if (uploadForm) {
        uploadForm.addEventListener('submit', () => {
            // Hide button, show spinner
            splitBtn.style.display = 'none';
            loadingDiv.classList.remove('hidden');
        });
    }
});
