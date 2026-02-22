// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';
const POLL_INTERVAL = 3000; // 3 seconds

// State
let selectedFile = null;
let activePolling = new Set();
let allJobs = [];

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const videoFileInput = document.getElementById('videoFile');
const configSection = document.getElementById('configSection');
const processBtn = document.getElementById('processBtn');
const activeJobsContainer = document.getElementById('activeJobs');
const jobHistoryContainer = document.getElementById('jobHistory');
const jobModal = document.getElementById('jobModal');

// Configuration inputs
const blurStrengthInput = document.getElementById('blurStrength');
const blurStrengthValue = document.getElementById('blurStrengthValue');
const confidenceInput = document.getElementById('confidence');
const confidenceValue = document.getElementById('confidenceValue');
const sampleRateInput = document.getElementById('sampleRate');
const paddingInput = document.getElementById('padding');
const languagesSelect = document.getElementById('languages');
const specificWordsInput = document.getElementById('specificWords');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadJobs();
    setupRangeInputs();
});

// Event Listeners
function initializeEventListeners() {
    // Upload area click
    uploadArea.addEventListener('click', () => videoFileInput.click());
    
    // File input change
    videoFileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Process button
    processBtn.addEventListener('click', handleProcessVideo);
    
    // Modal close
    const modalClose = document.querySelector('.modal-close');
    modalClose.addEventListener('click', closeModal);
    jobModal.addEventListener('click', (e) => {
        if (e.target === jobModal) closeModal();
    });
}

function setupRangeInputs() {
    blurStrengthInput.addEventListener('input', (e) => {
        let value = parseInt(e.target.value);
        // Ensure odd number
        if (value % 2 === 0) value++;
        blurStrengthValue.textContent = value;
        e.target.value = value;
    });
    
    confidenceInput.addEventListener('input', (e) => {
        confidenceValue.textContent = parseFloat(e.target.value).toFixed(1);
    });
}

// File Handling
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        validateAndSetFile(file);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const file = e.dataTransfer.files[0];
    if (file) {
        validateAndSetFile(file);
    }
}

function validateAndSetFile(file) {
    // Validate file type
    const validTypes = ['video/mp4', 'video/quicktime'];
    if (!validTypes.includes(file.type)) {
        showNotification('Please select a valid MP4 or MOV file', 'error');
        return;
    }
    
    // Validate file size (500MB)
    const maxSize = 500 * 1024 * 1024;
    if (file.size > maxSize) {
        showNotification('File size exceeds 500MB limit', 'error');
        return;
    }
    
    selectedFile = file;
    updateUploadArea(file);
    configSection.style.display = 'block';
}

function updateUploadArea(file) {
    const uploadContent = uploadArea.querySelector('.upload-content');
    uploadContent.innerHTML = `
        <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <p class="upload-text">✓ ${file.name}</p>
        <p class="upload-subtext">${formatFileSize(file.size)}</p>
        <p class="upload-formats">Click to change file</p>
    `;
    uploadArea.classList.add('has-file');
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Process Video
async function handleProcessVideo() {
    if (!selectedFile) {
        showNotification('Please select a video file', 'error');
        return;
    }
    
    processBtn.disabled = true;
    processBtn.innerHTML = '<span class="spinner"></span> Processing...';
    
    try {
        const formData = new FormData();
        formData.append('video', selectedFile);
        
        // Add configuration
        const selectedLanguages = Array.from(languagesSelect.selectedOptions).map(opt => opt.value);
        selectedLanguages.forEach(lang => formData.append('languages', lang));
        
        formData.append('blur_strength', blurStrengthInput.value);
        formData.append('confidence', confidenceInput.value);
        formData.append('sample_rate', sampleRateInput.value);
        formData.append('padding', paddingInput.value);
        
        // Add specific words if provided
        const words = specificWordsInput.value.trim();
        if (words) {
            words.split(',').forEach(word => {
                formData.append('words', word.trim());
            });
        }
        
        const response = await fetch(`${API_BASE_URL}/videos/blur`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Failed to submit job');
        }
        
        const job = await response.json();
        showNotification('Job submitted successfully!', 'success');
        
        // Reset form
        resetForm();
        
        // Add job to list and start polling
        addJobToList(job);
        startPolling(job.job_id);
        
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        processBtn.disabled = false;
        processBtn.innerHTML = '<span class="btn-icon">🚀</span> Start Processing';
    }
}

function resetForm() {
    selectedFile = null;
    videoFileInput.value = '';
    configSection.style.display = 'none';
    
    const uploadContent = uploadArea.querySelector('.upload-content');
    uploadContent.innerHTML = `
        <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
        </svg>
        <p class="upload-text">Drag & drop your video here</p>
        <p class="upload-subtext">or click to browse</p>
        <p class="upload-formats">Supports MP4 and MOV (max 500MB)</p>
    `;
    uploadArea.classList.remove('has-file');
}

// Job Management
async function loadJobs() {
    // In a real implementation, this would fetch from an API endpoint
    // For now, we'll just update the display
    updateJobsDisplay();
}

function addJobToList(job) {
    const existingIndex = allJobs.findIndex(j => j.job_id === job.job_id);
    if (existingIndex >= 0) {
        allJobs[existingIndex] = job;
    } else {
        allJobs.unshift(job);
    }
    updateJobsDisplay();
}

function updateJobsDisplay() {
    const activeJobs = allJobs.filter(j => j.status === 'queued' || j.status === 'processing');
    const completedJobs = allJobs.filter(j => j.status === 'completed' || j.status === 'failed');
    
    // Update active jobs
    if (activeJobs.length === 0) {
        activeJobsContainer.innerHTML = '<p class="empty-state">No active jobs</p>';
    } else {
        activeJobsContainer.innerHTML = activeJobs.map(job => createJobCard(job)).join('');
    }
    
    // Update job history
    if (completedJobs.length === 0) {
        jobHistoryContainer.innerHTML = '<p class="empty-state">No completed jobs</p>';
    } else {
        jobHistoryContainer.innerHTML = completedJobs.map(job => createJobCard(job)).join('');
    }
}

function createJobCard(job) {
    const statusClass = `status-${job.status}`;
    const progress = job.progress || 0;
    
    return `
        <div class="job-card" data-job-id="${job.job_id}">
            <div class="job-header">
                <div>
                    <div class="job-title">${job.input_file || 'Video Processing'}</div>
                    <div class="job-id">ID: ${job.job_id}</div>
                </div>
                <span class="job-status ${statusClass}">${job.status.toUpperCase()}</span>
            </div>
            
            ${job.status === 'processing' ? `
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${progress}%"></div>
                </div>
            ` : ''}
            
            <div class="job-info">
                <div class="job-info-item">
                    <span class="job-info-label">Created</span>
                    <span class="job-info-value">${formatDate(job.created_at)}</span>
                </div>
                ${job.completed_at ? `
                    <div class="job-info-item">
                        <span class="job-info-label">Completed</span>
                        <span class="job-info-value">${formatDate(job.completed_at)}</span>
                    </div>
                ` : ''}
                ${job.parameters ? `
                    <div class="job-info-item">
                        <span class="job-info-label">Blur Strength</span>
                        <span class="job-info-value">${job.parameters.blur_strength}</span>
                    </div>
                ` : ''}
            </div>
            
            <div class="job-actions">
                <button class="btn btn-secondary" onclick="viewJobDetails('${job.job_id}')">
                    📋 Details
                </button>
                ${job.status === 'completed' ? `
                    <button class="btn btn-success" onclick="downloadResult('${job.job_id}')">
                        ⬇️ Download
                    </button>
                ` : ''}
                ${job.status === 'failed' ? `
                    <button class="btn btn-danger" onclick="deleteJob('${job.job_id}')">
                        🗑️ Delete
                    </button>
                ` : ''}
                ${job.status === 'queued' || job.status === 'processing' ? `
                    <button class="btn btn-danger" onclick="cancelJob('${job.job_id}')">
                        ❌ Cancel
                    </button>
                ` : ''}
            </div>
        </div>
    `;
}

// Polling
function startPolling(jobId) {
    if (activePolling.has(jobId)) return;
    
    activePolling.add(jobId);
    pollJobStatus(jobId);
}

async function pollJobStatus(jobId) {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`);
        if (!response.ok) throw new Error('Failed to fetch job status');
        
        const job = await response.json();
        addJobToList(job);
        
        // Continue polling if job is still active
        if (job.status === 'queued' || job.status === 'processing') {
            setTimeout(() => pollJobStatus(jobId), POLL_INTERVAL);
        } else {
            activePolling.delete(jobId);
            if (job.status === 'completed') {
                showNotification(`Job ${job.input_file} completed!`, 'success');
            } else if (job.status === 'failed') {
                showNotification(`Job ${job.input_file} failed: ${job.error}`, 'error');
            }
        }
    } catch (error) {
        console.error('Polling error:', error);
        activePolling.delete(jobId);
    }
}

// Job Actions
async function viewJobDetails(jobId) {
    const job = allJobs.find(j => j.job_id === jobId);
    if (!job) return;
    
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    modalTitle.textContent = `Job Details: ${job.input_file || jobId}`;
    modalBody.innerHTML = `
        <div class="job-info">
            <div class="job-info-item">
                <span class="job-info-label">Job ID</span>
                <span class="job-info-value" style="font-family: monospace;">${job.job_id}</span>
            </div>
            <div class="job-info-item">
                <span class="job-info-label">Status</span>
                <span class="job-info-value">
                    <span class="job-status status-${job.status}">${job.status.toUpperCase()}</span>
                </span>
            </div>
            <div class="job-info-item">
                <span class="job-info-label">Input File</span>
                <span class="job-info-value">${job.input_file || 'N/A'}</span>
            </div>
            <div class="job-info-item">
                <span class="job-info-label">Output File</span>
                <span class="job-info-value">${job.output_file || 'N/A'}</span>
            </div>
            <div class="job-info-item">
                <span class="job-info-label">Created At</span>
                <span class="job-info-value">${formatDate(job.created_at)}</span>
            </div>
            ${job.started_at ? `
                <div class="job-info-item">
                    <span class="job-info-label">Started At</span>
                    <span class="job-info-value">${formatDate(job.started_at)}</span>
                </div>
            ` : ''}
            ${job.completed_at ? `
                <div class="job-info-item">
                    <span class="job-info-label">Completed At</span>
                    <span class="job-info-value">${formatDate(job.completed_at)}</span>
                </div>
            ` : ''}
            ${job.progress !== undefined ? `
                <div class="job-info-item">
                    <span class="job-info-label">Progress</span>
                    <span class="job-info-value">${job.progress}%</span>
                </div>
            ` : ''}
        </div>
        
        ${job.parameters ? `
            <h3 class="mt-3 mb-2">Parameters</h3>
            <div class="job-info">
                <div class="job-info-item">
                    <span class="job-info-label">Languages</span>
                    <span class="job-info-value">${job.parameters.languages?.join(', ') || 'N/A'}</span>
                </div>
                <div class="job-info-item">
                    <span class="job-info-label">Blur Strength</span>
                    <span class="job-info-value">${job.parameters.blur_strength}</span>
                </div>
                <div class="job-info-item">
                    <span class="job-info-label">Confidence</span>
                    <span class="job-info-value">${job.parameters.confidence}</span>
                </div>
                <div class="job-info-item">
                    <span class="job-info-label">Sample Rate</span>
                    <span class="job-info-value">${job.parameters.sample_rate}</span>
                </div>
                <div class="job-info-item">
                    <span class="job-info-label">Padding</span>
                    <span class="job-info-value">${job.parameters.padding}px</span>
                </div>
            </div>
        ` : ''}
        
        ${job.error ? `
            <h3 class="mt-3 mb-2">Error</h3>
            <div style="padding: 1rem; background: #fee2e2; border-radius: 0.5rem; color: #991b1b;">
                ${job.error}
            </div>
        ` : ''}
    `;
    
    jobModal.classList.add('show');
}

async function downloadResult(jobId) {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/result`);
        if (!response.ok) throw new Error('Failed to download result');
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `blurred_video_${jobId}.mp4`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showNotification('Download started!', 'success');
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

async function deleteJob(jobId) {
    if (!confirm('Are you sure you want to delete this job?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Failed to delete job');
        
        allJobs = allJobs.filter(j => j.job_id !== jobId);
        updateJobsDisplay();
        showNotification('Job deleted successfully', 'success');
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

async function cancelJob(jobId) {
    if (!confirm('Are you sure you want to cancel this job?')) return;
    await deleteJob(jobId);
}

// Modal
function closeModal() {
    jobModal.classList.remove('show');
}

// Utilities
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString();
}

function showNotification(message, type = 'info') {
    // Simple notification - could be enhanced with a toast library
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        info: '#3b82f6',
        warning: '#f59e0b'
    };
    
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type]};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS for notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Made with Bob
