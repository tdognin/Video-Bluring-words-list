// Global variables
let originalImage = null;
let originalCanvas = null;
let blurredCanvas = null;
let currentBlurValue = 0;
let originalFileName = '';
let originalFileExtension = '';

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadSection = document.getElementById('uploadSection');
const editorSection = document.getElementById('editorSection');
const errorMessage = document.getElementById('errorMessage');
const blurSlider = document.getElementById('blurSlider');
const blurValue = document.getElementById('blurValue');
const downloadBtn = document.getElementById('downloadBtn');
const resetBtn = document.getElementById('resetBtn');
const loadingOverlay = document.getElementById('loadingOverlay');

// Constants
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const SUPPORTED_FORMATS = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
});

function initializeEventListeners() {
    // Upload area click
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0]);
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        handleFileSelect(e.dataTransfer.files[0]);
    });

    // Blur slider
    blurSlider.addEventListener('input', (e) => {
        currentBlurValue = parseFloat(e.target.value);
        blurValue.textContent = `${currentBlurValue}px`;
        applyBlur();
    });

    // Download button
    downloadBtn.addEventListener('click', downloadImage);

    // Reset button
    resetBtn.addEventListener('click', resetApplication);
}

function handleFileSelect(file) {
    // Clear previous error
    hideError();

    // Validate file
    if (!file) {
        showError('No file selected. Please choose an image file.');
        return;
    }

    if (!SUPPORTED_FORMATS.includes(file.type)) {
        showError('Unsupported file format. Please upload a JPG, PNG, GIF, or WebP image.');
        return;
    }

    if (file.size > MAX_FILE_SIZE) {
        showError('File size exceeds 10MB limit. Please choose a smaller image.');
        return;
    }

    // Store file info
    originalFileName = file.name.substring(0, file.name.lastIndexOf('.')) || file.name;
    originalFileExtension = file.name.substring(file.name.lastIndexOf('.')) || '.png';

    // Load image
    loadImage(file);
}

function loadImage(file) {
    const reader = new FileReader();

    reader.onload = (e) => {
        const img = new Image();

        img.onload = () => {
            originalImage = img;
            setupCanvases();
            showEditor();
        };

        img.onerror = () => {
            showError('Failed to load image. Please try a different file.');
        };

        img.src = e.target.result;
    };

    reader.onerror = () => {
        showError('Failed to read file. Please try again.');
    };

    reader.readAsDataURL(file);
}

function setupCanvases() {
    // Get canvas elements
    originalCanvas = document.getElementById('originalCanvas');
    blurredCanvas = document.getElementById('blurredCanvas');

    // Calculate dimensions (max width 500px for performance)
    const maxWidth = 500;
    let width = originalImage.width;
    let height = originalImage.height;

    if (width > maxWidth) {
        height = (height * maxWidth) / width;
        width = maxWidth;
    }

    // Set canvas dimensions
    originalCanvas.width = width;
    originalCanvas.height = height;
    blurredCanvas.width = width;
    blurredCanvas.height = height;

    // Draw original image
    const originalCtx = originalCanvas.getContext('2d');
    originalCtx.drawImage(originalImage, 0, 0, width, height);

    // Draw initial blurred image (no blur)
    const blurredCtx = blurredCanvas.getContext('2d');
    blurredCtx.drawImage(originalImage, 0, 0, width, height);

    // Reset blur slider
    blurSlider.value = 0;
    currentBlurValue = 0;
    blurValue.textContent = '0px';
}

function applyBlur() {
    if (!originalImage || !blurredCanvas) return;

    // Show loading overlay
    showLoading();

    // Use requestAnimationFrame for smooth updates
    requestAnimationFrame(() => {
        const ctx = blurredCanvas.getContext('2d');
        
        // Clear canvas
        ctx.clearRect(0, 0, blurredCanvas.width, blurredCanvas.height);

        // Apply blur using CSS filter (more efficient than canvas blur)
        if (currentBlurValue > 0) {
            ctx.filter = `blur(${currentBlurValue}px)`;
        } else {
            ctx.filter = 'none';
        }

        // Draw image with blur
        ctx.drawImage(originalImage, 0, 0, blurredCanvas.width, blurredCanvas.height);

        // Reset filter
        ctx.filter = 'none';

        // Hide loading overlay
        hideLoading();
    });
}

function downloadImage() {
    if (!blurredCanvas) return;

    try {
        // Create a temporary canvas with original image dimensions
        const downloadCanvas = document.createElement('canvas');
        downloadCanvas.width = originalImage.width;
        downloadCanvas.height = originalImage.height;
        const ctx = downloadCanvas.getContext('2d');

        // Apply blur filter
        if (currentBlurValue > 0) {
            ctx.filter = `blur(${currentBlurValue}px)`;
        }

        // Draw full-resolution image
        ctx.drawImage(originalImage, 0, 0);

        // Determine MIME type based on original file extension
        let mimeType = 'image/png';
        if (originalFileExtension === '.jpg' || originalFileExtension === '.jpeg') {
            mimeType = 'image/jpeg';
        } else if (originalFileExtension === '.webp') {
            mimeType = 'image/webp';
        } else if (originalFileExtension === '.gif') {
            mimeType = 'image/png'; // Convert GIF to PNG for better quality
        }

        // Convert to blob and download
        downloadCanvas.toBlob((blob) => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${originalFileName}_blurred${originalFileExtension}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, mimeType, 0.95);

    } catch (error) {
        showError('Failed to download image. Please try again.');
        console.error('Download error:', error);
    }
}

function resetApplication() {
    // Reset variables
    originalImage = null;
    originalCanvas = null;
    blurredCanvas = null;
    currentBlurValue = 0;
    originalFileName = '';
    originalFileExtension = '';

    // Reset file input
    fileInput.value = '';

    // Hide editor, show upload
    editorSection.style.display = 'none';
    uploadSection.style.display = 'block';

    // Clear error
    hideError();
}

function showEditor() {
    uploadSection.style.display = 'none';
    editorSection.style.display = 'block';
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.add('show');
}

function hideError() {
    errorMessage.textContent = '';
    errorMessage.classList.remove('show');
}

function showLoading() {
    loadingOverlay.classList.add('show');
}

function hideLoading() {
    loadingOverlay.classList.remove('show');
}

// Prevent default drag and drop on the whole page
document.addEventListener('dragover', (e) => {
    e.preventDefault();
});

document.addEventListener('drop', (e) => {
    e.preventDefault();
});

// Made with Bob
