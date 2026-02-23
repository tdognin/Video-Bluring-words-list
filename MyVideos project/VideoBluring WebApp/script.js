// Global variables
let currentFile = null;
let currentJobId = null;
let pollInterval = null;
const API_BASE_URL = 'http://localhost:8000/api/v1';

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadSection = document.getElementById('uploadSection');
const editorSection = document.getElementById('editorSection');
const errorMessage = document.getElementById('errorMessage');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const status = document.getElementById('status');
const wordsInput = document.getElementById('wordsInput');
const blurStrength = document.getElementById('blurStrength');
const blurStrengthValue = document.getElementById('blurStrengthValue');
const sampleRate = document.getElementById('sampleRate');
const sampleRateValue = document.getElementById('sampleRateValue');
const processBtn = document.getElementById('processBtn');
const resetBtn = document.getElementById('resetBtn');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const downloadSection = document.getElementById('downloadSection');
const downloadBtn = document.getElementById('downloadBtn');

// Constants
const MAX_FILE_SIZE = 500 * 1024 * 1024; // 500MB
const SUPPORTED_FORMATS = ['video/mp4', 'video/quicktime'];

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

    // Blur strength slider
    blurStrength.addEventListener('input', (e) => {
        blurStrengthValue.textContent = e.target.value;
    });

    // Sample rate slider
    sampleRate.addEventListener('input', (e) => {
        sampleRateValue.textContent = e.target.value;
    });

    // Process button
    processBtn.addEventListener('click', processVideo);

    // Reset button
    resetBtn.addEventListener('click', resetApplication);

    // Download button
    downloadBtn.addEventListener('click', downloadVideo);
}

function handleFileSelect(file) {
    hideError();

    if (!file) {
        showError('No file selected. Please choose a video file.');
        return;
    }

    // Check file extension as fallback for MIME type
    const fileName = file.name.toLowerCase();
    const isVideo = SUPPORTED_FORMATS.includes(file.type) ||
                    fileName.endsWith('.mp4') ||
                    fileName.endsWith('.mov');

    if (!isVideo) {
        showError(`Unsupported file format: ${file.type || 'unknown'}. Please upload an MP4 or MOV video. File: ${file.name}`);
        return;
    }

    if (file.size > MAX_FILE_SIZE) {
        showError('File size exceeds 500MB limit. Please choose a smaller video.');
        return;
    }

    currentFile = file;
    displayVideoInfo(file);
    uploadSection.style.display = 'none';
    editorSection.style.display = 'block';
}

function displayVideoInfo(file) {
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    status.textContent = 'Ready to process';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

async function processVideo() {
    if (!currentFile) {
        showError('No video file selected.');
        return;
    }

    processBtn.disabled = true;
    status.textContent = 'Uploading...';
    progressSection.style.display = 'block';
    downloadSection.style.display = 'none';

    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('video', currentFile);
        
        // Add words if specified
        const words = wordsInput.value.split(',').map(w => w.trim()).filter(w => w);
        words.forEach(word => formData.append('words', word));
        
        // Add parameters
        formData.append('blur_strength', blurStrength.value);
        formData.append('sample_rate', sampleRate.value);
        formData.append('languages', 'en');

        // Upload video
        const response = await fetch(`${API_BASE_URL}/videos/blur`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Failed to upload video');
        }

        const result = await response.json();
        currentJobId = result.job_id;
        
        status.textContent = 'Processing...';
        startPolling();

    } catch (error) {
        showError(`Error: ${error.message}`);
        processBtn.disabled = false;
        progressSection.style.display = 'none';
    }
}

function startPolling() {
    pollInterval = setInterval(checkJobStatus, 3000); // Poll every 3 seconds
}

async function checkJobStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs/${currentJobId}`);
        
        if (!response.ok) {
            throw new Error('Failed to check job status');
        }

        const job = await response.json();
        
        // Update progress
        const progress = job.progress || 0;
        progressFill.style.width = `${progress}%`;
        progressText.textContent = `${progress}%`;
        
        // Update status
        status.textContent = `Processing: ${progress}%`;

        // Check if completed
        if (job.status === 'completed') {
            clearInterval(pollInterval);
            status.textContent = 'Processing complete!';
            progressSection.style.display = 'none';
            downloadSection.style.display = 'block';
            processBtn.disabled = false;
        } else if (job.status === 'failed') {
            clearInterval(pollInterval);
            showError(`Processing failed: ${job.error || 'Unknown error'}`);
            processBtn.disabled = false;
            progressSection.style.display = 'none';
        }

    } catch (error) {
        clearInterval(pollInterval);
        showError(`Error checking status: ${error.message}`);
        processBtn.disabled = false;
        progressSection.style.display = 'none';
    }
}

async function downloadVideo() {
    if (!currentJobId) {
        showError('No processed video available.');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/jobs/${currentJobId}/result`);
        
        if (!response.ok) {
            throw new Error('Failed to download video');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `blurred_${currentFile.name}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

    } catch (error) {
        showError(`Error downloading video: ${error.message}`);
    }
}

function resetApplication() {
    if (pollInterval) {
        clearInterval(pollInterval);
    }
    
    currentFile = null;
    currentJobId = null;
    fileInput.value = '';
    wordsInput.value = '';
    blurStrength.value = 51;
    blurStrengthValue.textContent = '51';
    sampleRate.value = 5;
    sampleRateValue.textContent = '5';
    
    uploadSection.style.display = 'block';
    editorSection.style.display = 'none';
    progressSection.style.display = 'none';
    downloadSection.style.display = 'none';
    processBtn.disabled = false;
    
    hideError();
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.textContent = '';
    errorMessage.style.display = 'none';
}

// Made with Bob
