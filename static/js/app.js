document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.querySelector('label[for="file-upload"]');
    const fileInput = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name');

    // Handle drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropZone.classList.add('drag-over');
    }

    function unhighlight(e) {
        dropZone.classList.remove('drag-over');
    }

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        updateFileName(files[0]);
    }

    // Handle file selection
    fileInput.addEventListener('change', function(e) {
        if (this.files && this.files[0]) {
            updateFileName(this.files[0]);
        }
    });

    function updateFileName(file) {
        if (file) {
            // Validate file type
            if (!file.name.toLowerCase().endsWith('.pptx')) {
                fileNameDisplay.innerHTML = '<span class="text-red-500">Please select a PPTX file</span>';
                fileInput.value = '';
                return;
            }

            // Display file name and size
            const size = (file.size / (1024 * 1024)).toFixed(2);
            fileNameDisplay.innerHTML = `
                <span class="text-gray-700">
                    <i class="fas fa-file-powerpoint text-blue-500 mr-1"></i>
                    ${file.name}
                </span>
                <span class="text-gray-500 text-sm ml-2">(${size} MB)</span>
            `;
        } else {
            fileNameDisplay.textContent = '';
        }
    }
});
