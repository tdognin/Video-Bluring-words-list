#!/usr/bin/env python3
"""
REST API Server for Video Text Blur Tool

This Flask-based REST API provides endpoints for video text blurring operations.
See openapi.yaml for the complete API specification.
"""

import os
import uuid
import json
from datetime import datetime
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

# Create directories
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

# In-memory job storage (use Redis/database in production)
jobs: Dict[str, Dict] = {}


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_video_async(job_id: str, input_path: str, output_path: str, params: Dict):
    """Process video in background thread."""
    try:
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['started_at'] = datetime.utcnow().isoformat() + 'Z'
        
        # Initialize blur processor
        blur = VideoTextBlur(
            languages=params.get('languages', ['en']),
            blur_strength=params.get('blur_strength', 51),
            confidence_threshold=params.get('confidence', 0.5),
            sample_rate=params.get('sample_rate', 1),
            padding=params.get('padding', 10),
            words_to_blur=params.get('words', None)
        )
        
        # Process video
        blur.process_video(input_path, output_path)
        
        # Update job status
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['completed_at'] = datetime.utcnow().isoformat() + 'Z'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['result_url'] = f'/api/v1/jobs/{job_id}/result'
        
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)
        jobs[job_id]['completed_at'] = datetime.utcnow().isoformat() + 'Z'

@app.route('/')
def index():
    """Serve the web interface."""
    return render_template('index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('static', filename)



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
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    input_path = UPLOAD_FOLDER / f"{job_id}_{filename}"
    file.save(str(input_path))
    
    # Prepare output path
    output_filename = f"{job_id}_blurred_{filename}"
    output_path = OUTPUT_FOLDER / output_filename
    
    # Parse parameters
    params = {
        'languages': request.form.getlist('languages') or ['en'],
        'blur_strength': int(request.form.get('blur_strength', 51)),
        'confidence': float(request.form.get('confidence', 0.5)),
        'sample_rate': int(request.form.get('sample_rate', 1)),
        'padding': int(request.form.get('padding', 10)),
        'words': request.form.getlist('words') or None
    }
    
    # Validate blur_strength is odd
    if params['blur_strength'] % 2 == 0:
        return jsonify({
            'error': 'INVALID_PARAMETER',
            'message': 'blur_strength must be an odd number'
        }), 400
    
    # Create job record
    jobs[job_id] = {
        'job_id': job_id,
        'status': 'queued',
        'created_at': datetime.utcnow().isoformat() + 'Z',
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
        'created_at': jobs[job_id]['created_at'],
        'estimated_duration': 120  # Placeholder
    }), 202


@app.route('/api/v1/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id: str):
    """Get job status."""
    if job_id not in jobs:
        return jsonify({
            'error': 'JOB_NOT_FOUND',
            'message': f'Job {job_id} not found'
        }), 404
    
    job = jobs[job_id]
    
    # Build response
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
    """Download processed video."""
    if job_id not in jobs:
        return jsonify({
            'error': 'JOB_NOT_FOUND',
            'message': f'Job {job_id} not found'
        }), 404
    
    job = jobs[job_id]
    
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
    
    return send_file(
        str(output_path),
        as_attachment=True,
        download_name=job['output_file'],
        mimetype='video/mp4'
    )


@app.route('/api/v1/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id: str):
    """Cancel or delete job."""
    if job_id not in jobs:
        return jsonify({
            'error': 'JOB_NOT_FOUND',
            'message': f'Job {job_id} not found'
        }), 404
    
    job = jobs[job_id]
    
    # Clean up files
    try:
        input_path = Path(job['input_path'])
        if input_path.exists():
            input_path.unlink()
        
        output_path = Path(job['output_path'])
        if output_path.exists():
            output_path.unlink()
    except Exception as e:
        print(f"Error cleaning up files for job {job_id}: {e}")
    
    # Remove job from memory
    del jobs[job_id]
    
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
    
    print("Starting Video Text Blur API Server...")
    print("API Documentation: http://localhost:8000/swagger")
    print("Health Check: http://localhost:8000/api/v1/health")
    
    app.run(host='0.0.0.0', port=8000, debug=True)

# Made with Bob
