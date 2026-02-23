#!/usr/bin/env python3
"""
REST API Server for Video Text Blur Tool

This Flask-based REST API provides endpoints for video text blurring operations.
See openapi.yaml for the complete API specification.
"""

import os
import uuid
import json
import mimetypes
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from flask_cors import CORS
import threading
import sys

# Add parent directory to path to import blur_text_video
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blur_text_video import VideoTextBlur

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('outputs')
ALLOWED_EXTENSIONS = {'mp4', 'mov'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
API_KEY = os.environ.get('API_KEY', None)  # Optional API key from environment

# Create directories
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

# In-memory job storage with thread safety (use Redis/database in production)
jobs: Dict[str, Dict] = {}
jobs_lock = threading.Lock()  # FIX 1: Thread-safe access to jobs dictionary
JOB_RETENTION_HOURS = 24  # FIX 5: Keep jobs for 24 hours


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup_old_jobs():
    """Remove jobs and files older than retention period. FIX 5: Prevent memory/disk leaks."""
    while True:
        try:
            current_time = datetime.utcnow()
            with jobs_lock:
                jobs_to_delete = []
                
                for job_id, job in jobs.items():
                    try:
                        # Parse created_at timestamp (handle 'Z' suffix properly)
                        created_at_str = job['created_at'].rstrip('Z')
                        created_at = datetime.fromisoformat(created_at_str)
                        age = current_time - created_at
                        
                        # Delete jobs older than retention period
                        if age > timedelta(hours=JOB_RETENTION_HOURS):
                            jobs_to_delete.append(job_id)
                    except (ValueError, KeyError) as e:
                        print(f"Error parsing timestamp for job {job_id}: {e}")
                        continue
                
                # Clean up old jobs
                for job_id in jobs_to_delete:
                    job = jobs[job_id]
                    try:
                        # Remove files
                        input_path = Path(job['input_path'])
                        if input_path.exists():
                            input_path.unlink()
                        output_path = Path(job['output_path'])
                        if output_path.exists():
                            output_path.unlink()
                    except Exception as e:
                        print(f"Error cleaning up files for job {job_id}: {e}")
                    
                    # Remove from jobs dict
                    del jobs[job_id]
                    print(f"Cleaned up old job: {job_id}")
        
        except Exception as e:
            print(f"Error in cleanup thread: {e}")
        
        # Run cleanup every hour
        threading.Event().wait(3600)


def process_video_async(job_id: str, input_path: str, output_path: str, params: Dict):
    """Process video in background thread. FIX 1: Thread-safe job updates."""
    try:
        # FIX 1: Use lock when updating shared job state, check if job still exists
        with jobs_lock:
            if job_id not in jobs:
                print(f"Job {job_id} was deleted before processing started")
                return
            jobs[job_id]['status'] = 'processing'
            jobs[job_id]['started_at'] = datetime.utcnow().isoformat() + 'Z'
        
        # Initialize blur processor
        blur = VideoTextBlur(
            languages=params.get('languages', ['en']),
            blur_strength=params.get('blur_strength', 51),
            confidence_threshold=params.get('confidence', 0.5),
            target_words=params.get('words', None)
        )
        
        # Process video with sample_rate and padding parameters
        blur.process_video(
            input_path,
            output_path,
            sample_rate=params.get('sample_rate', 1),
            padding=params.get('padding', 10)
        )
        
        # FIX 1: Update job status with lock protection, check if job still exists
        with jobs_lock:
            if job_id not in jobs:
                print(f"Job {job_id} was deleted during processing")
                return
            jobs[job_id]['status'] = 'completed'
            jobs[job_id]['completed_at'] = datetime.utcnow().isoformat() + 'Z'
            jobs[job_id]['progress'] = 100
            jobs[job_id]['result_url'] = f'/api/v1/jobs/{job_id}/result'
        
    except Exception as e:
        # FIX 1: Update error status with lock protection, check if job still exists
        with jobs_lock:
            if job_id not in jobs:
                print(f"Job {job_id} was deleted before error could be recorded")
                return
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['error'] = str(e)
            jobs[job_id]['completed_at'] = datetime.utcnow().isoformat() + 'Z'

def check_api_key():
    """Validate API key if configured."""
    if API_KEY:
        provided_key = request.headers.get('X-API-Key')
        if not provided_key or provided_key != API_KEY:
            return jsonify({
                'error': 'UNAUTHORIZED',
                'message': 'Invalid or missing API key'
            }), 401
    return None


@app.route('/')
def index():
    """Serve the web interface."""
    return render_template('index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('static', filename)


@app.route('/swagger')
def swagger_ui():
    """Redirect to Swagger UI or API documentation."""
    return jsonify({
        'message': 'API Documentation',
        'openapi_spec': '/api/v1/openapi.yaml',
        'endpoints': {
            'health': '/api/v1/health',
            'blur_video': '/api/v1/videos/blur',
            'job_status': '/api/v1/jobs/{jobId}',
            'download_result': '/api/v1/jobs/{jobId}/result'
        }
    })


@app.route('/api/v1/openapi.yaml')
def openapi_spec():
    """Serve OpenAPI specification."""
    spec_path = Path(__file__).parent / 'openapi.yaml'
    if spec_path.exists():
        return send_file(str(spec_path), mimetype='text/yaml')
    return jsonify({'error': 'OpenAPI spec not found'}), 404


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })


@app.route('/api/v1/videos/blur', methods=['POST'])
def blur_video():
    """Submit video for text blurring."""
    # Check API key if configured
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    
    # Check if video file is present
    if 'video' not in request.files:
        return jsonify({
            'error': 'MISSING_FILE',
            'message': 'Video file is required'
        }), 400
    
    file = request.files['video']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({
            'error': 'EMPTY_FILENAME',
            'message': 'No file selected'
        }), 400
    
    # Check file extension
    if not allowed_file(file.filename):
        return jsonify({
            'error': 'INVALID_FORMAT',
            'message': f'Only {", ".join(ALLOWED_EXTENSIONS)} files are supported'
        }), 415
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Save uploaded file with error handling
    filename = secure_filename(file.filename)
    input_path = UPLOAD_FOLDER / f"{job_id}_{filename}"
    
    try:
        file.save(str(input_path))
        
        # Validate file size after saving
        file_size = input_path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            input_path.unlink()  # Delete the file
            return jsonify({
                'error': 'FILE_TOO_LARGE',
                'message': f'File size exceeds maximum limit of {MAX_FILE_SIZE // (1024*1024)}MB'
            }), 413
    except Exception as e:
        if input_path.exists():
            input_path.unlink()
        return jsonify({
            'error': 'FILE_SAVE_ERROR',
            'message': f'Failed to save uploaded file: {str(e)}'
        }), 500
    
    # Prepare output path
    output_filename = f"{job_id}_blurred_{filename}"
    output_path = OUTPUT_FOLDER / output_filename
    
    # FIX 2: Parse parameters with validation
    try:
        params = {
            'languages': request.form.getlist('languages') or ['en'],
            'blur_strength': int(request.form.get('blur_strength', 51)),
            'confidence': float(request.form.get('confidence', 0.5)),
            'sample_rate': int(request.form.get('sample_rate', 1)),
            'padding': int(request.form.get('padding', 10)),
            'words': request.form.getlist('words') or None
        }
    except (ValueError, TypeError) as e:
        # Clean up uploaded file if parameter parsing fails
        if input_path.exists():
            input_path.unlink()
        return jsonify({
            'error': 'INVALID_PARAMETER',
            'message': f'Invalid parameter value: {str(e)}'
        }), 400
    
    # FIX 4: Validate parameter ranges
    validation_errors = []
    if params['blur_strength'] <= 0:
        validation_errors.append('blur_strength must be positive')
    if params['blur_strength'] % 2 == 0:
        validation_errors.append('blur_strength must be an odd number')
    if not (0.0 <= params['confidence'] <= 1.0):
        validation_errors.append('confidence must be between 0.0 and 1.0')
    if params['sample_rate'] < 1:
        validation_errors.append('sample_rate must be at least 1')
    if params['padding'] < 0:
        validation_errors.append('padding must be non-negative')
    
    if validation_errors:
        if input_path.exists():
            input_path.unlink()
        return jsonify({
            'error': 'INVALID_PARAMETER',
            'message': '; '.join(validation_errors)
        }), 400
    
    # Create job record with thread safety
    created_at = datetime.utcnow().isoformat() + 'Z'
    with jobs_lock:
        jobs[job_id] = {
            'job_id': job_id,
            'status': 'queued',
            'created_at': created_at,
            'input_file': filename,
            'output_file': output_filename,
            'input_path': str(input_path),
            'output_path': str(output_path),
            'parameters': params,
            'progress': 0
        }
    
    # Start processing in background thread
    thread = threading.Thread(
        target=process_video_async,
        args=(job_id, str(input_path), str(output_path), params)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'status': 'queued',
        'created_at': created_at,
        'estimated_duration': 120  # Placeholder
    }), 202


@app.route('/api/v1/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id: str):
    """Get job status. FIX 6: Thread-safe job access."""
    # Check API key if configured
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    
    # FIX 6: Thread-safe job access
    with jobs_lock:
        if job_id not in jobs:
            return jsonify({
                'error': 'JOB_NOT_FOUND',
                'message': f'Job {job_id} not found'
            }), 404
        
        # Create a copy to avoid holding lock during response building
        job = jobs[job_id].copy()
    
    # Build response (outside lock)
    response = {
        'job_id': job['job_id'],
        'status': job['status'],
        'created_at': job['created_at'],
        'input_file': job['input_file'],
        'output_file': job['output_file'],
        'parameters': job['parameters'],
        'progress': job.get('progress', 0)
    }
    
    # Add optional fields
    if 'started_at' in job:
        response['started_at'] = job['started_at']
    if 'completed_at' in job:
        response['completed_at'] = job['completed_at']
    if 'error' in job:
        response['error'] = job['error']
    if 'result_url' in job:
        response['result_url'] = job['result_url']
    
    return jsonify(response)


@app.route('/api/v1/jobs/<job_id>/result', methods=['GET'])
def download_result(job_id: str):
    """Download processed video. FIX 3 & 6: Fixed deprecated parameter and thread safety."""
    # Check API key if configured
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    
    # FIX 6: Thread-safe job access
    with jobs_lock:
        if job_id not in jobs:
            return jsonify({
                'error': 'JOB_NOT_FOUND',
                'message': f'Job {job_id} not found'
            }), 404
        
        job = jobs[job_id].copy()
    
    if job['status'] != 'completed':
        return jsonify({
            'error': 'RESULT_NOT_READY',
            'message': f'Job is {job["status"]}, result not available'
        }), 425
    
    output_path = Path(job['output_path'])
    if not output_path.exists():
        return jsonify({
            'error': 'RESULT_NOT_FOUND',
            'message': 'Result file not found'
        }), 404
    
    # Detect MIME type from file extension
    mimetype, _ = mimetypes.guess_type(str(output_path))
    if not mimetype:
        mimetype = 'video/mp4'  # Default fallback
    
    # FIX 3: Use download_name instead of deprecated attachment_filename
    return send_file(
        str(output_path),
        as_attachment=True,
        download_name=job['output_file'],
        mimetype=mimetype
    )


@app.route('/api/v1/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id: str):
    """Cancel or delete job. FIX 6: Thread-safe job deletion."""
    # Check API key if configured
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    
    # FIX 6: Thread-safe job access and deletion
    with jobs_lock:
        if job_id not in jobs:
            return jsonify({
                'error': 'JOB_NOT_FOUND',
                'message': f'Job {job_id} not found'
            }), 404
        
        job = jobs[job_id].copy()
        del jobs[job_id]
    
    # Clean up files (outside lock to avoid blocking)
    try:
        input_path = Path(job['input_path'])
        if input_path.exists():
            input_path.unlink()
        
        output_path = Path(job['output_path'])
        if output_path.exists():
            output_path.unlink()
    except Exception as e:
        print(f"Error cleaning up files for job {job_id}: {e}")
    
    return '', 204


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({
        'error': 'FILE_TOO_LARGE',
        'message': f'File size exceeds maximum limit of {MAX_FILE_SIZE // (1024*1024)}MB'
    }), 413


@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    return jsonify({
        'error': 'INTERNAL_ERROR',
        'message': 'An internal server error occurred'
    }), 500


if __name__ == '__main__':
    # Set max file size
    app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
    
    # FIX 5: Start cleanup thread to prevent memory/disk leaks
    cleanup_thread = threading.Thread(target=cleanup_old_jobs, daemon=True)
    cleanup_thread.start()
    
    print("Starting Video Text Blur API Server...")
    print("API Documentation: http://localhost:8000/swagger")
    print("Health Check: http://localhost:8000/api/v1/health")
    
    # Use debug mode only in development (check environment variable)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=8000, debug=debug_mode)

# Made with Bob
