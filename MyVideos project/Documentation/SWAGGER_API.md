# Swagger API Documentation

Comprehensive documentation for the Video Text Blur REST API with OpenAPI/Swagger specification.

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [API Specification](#api-specification)
4. [Authentication](#authentication)
5. [Endpoints Reference](#endpoints-reference)
6. [Request/Response Examples](#requestresponse-examples)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)
9. [Best Practices](#best-practices)
10. [Client SDKs](#client-sdks)

---

## Overview

The Video Text Blur REST API provides HTTP endpoints for automated text detection and blurring in videos. The API is built with Flask and follows RESTful principles with OpenAPI 3.0 specification.

### Key Features

- 🚀 **RESTful Design**: Standard HTTP methods and status codes
- 📝 **OpenAPI 3.0**: Complete API specification in `swagger/openapi.yaml`
- 🔄 **Asynchronous Processing**: Job-based workflow for long-running operations
- 📊 **Progress Tracking**: Real-time job status and progress updates
- 📥 **File Upload/Download**: Multipart form data for video uploads
- 🔍 **Interactive Documentation**: Swagger UI for testing and exploration
- 🌐 **CORS Enabled**: Cross-origin requests supported

### Architecture

```
Client → REST API → Job Queue → Video Processor → Result Storage
         (Flask)    (In-memory)  (VideoTextBlur)   (File system)
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- FFmpeg installed
- All dependencies from `requirements.txt`

### Installation

```bash
# Navigate to swagger directory
cd swagger

# Install dependencies
pip install -r requirements.txt

# Start the API server
python api_server.py
```

The server will start on `http://localhost:8000`

### Quick Test

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status":"healthy","version":"1.0.0","timestamp":"2026-02-23T10:00:00Z"}
```

---

## API Specification

### OpenAPI Document

The complete API specification is available in `swagger/openapi.yaml`:

```yaml
openapi: 3.0.3
info:
  title: Video Text Blur API
  version: 1.0.0
  description: REST API for automatically detecting and blurring text in videos
servers:
  - url: http://localhost:8000/api/v1
    description: Local development server
```

### Viewing the Specification

**Option 1: Swagger Editor**
1. Go to [editor.swagger.io](https://editor.swagger.io/)
2. File → Import File → Select `swagger/openapi.yaml`

**Option 2: Swagger UI (Local)**
```bash
# Install swagger-ui
npm install -g swagger-ui-watcher

# Serve the spec
swagger-ui-watcher swagger/openapi.yaml
```

**Option 3: VS Code Extension**
- Install "OpenAPI (Swagger) Editor" extension
- Open `swagger/openapi.yaml`

### API Versioning

Current version: **v1**

Base path: `/api/v1`

Future versions will use `/api/v2`, `/api/v3`, etc.

---

## Authentication

### API Key Authentication

The API supports optional API key authentication via the `X-API-Key` header.

**Enable Authentication**:
```bash
# Set environment variable
export API_KEY="your-secret-api-key"

# Start server
python api_server.py
```

**Using API Key**:
```bash
curl -H "X-API-Key: your-secret-api-key" \
  http://localhost:8000/api/v1/jobs/{jobId}
```

### Public Endpoints

The following endpoints do not require authentication:
- `GET /api/v1/health` - Health check

### Security Considerations

- **Development Mode**: API key is optional (not set by default)
- **Production Mode**: Always set `API_KEY` environment variable
- **HTTPS**: Use HTTPS in production to protect API keys
- **Key Rotation**: Regularly rotate API keys
- **Rate Limiting**: Implement rate limiting in production

---

## Endpoints Reference

### 1. Health Check

**Purpose**: Verify API service is running

**Endpoint**: `GET /api/v1/health`

**Authentication**: None

**Response**: `200 OK`

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-23T10:00:00Z"
}
```

**Use Cases**:
- Monitoring and health checks
- Load balancer health probes
- Service discovery

---

### 2. Submit Video for Blurring

**Purpose**: Upload video and start processing job

**Endpoint**: `POST /api/v1/videos/blur`

**Authentication**: API Key (optional in dev)

**Content-Type**: `multipart/form-data`

**Request Body**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `video` | file | ✅ Yes | - | Video file (MP4/MOV, max 500MB) |
| `languages` | string[] | No | `["en"]` | OCR languages (e.g., "en", "fr", "es") |
| `blur_strength` | integer | No | `51` | Blur kernel size (odd number, 1-201) |
| `confidence` | float | No | `0.5` | OCR confidence threshold (0.0-1.0) |
| `sample_rate` | integer | No | `1` | Process every Nth frame (1-30) |
| `padding` | integer | No | `10` | Padding around text (pixels, 0-50) |
| `words` | string[] | No | `null` | Specific words to blur (case-insensitive) |

**Response**: `202 Accepted`

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "created_at": "2026-02-23T10:00:00Z",
  "estimated_duration": 120
}
```

**Error Responses**:

| Status | Error Code | Description |
|--------|------------|-------------|
| 400 | `INVALID_REQUEST` | Missing or invalid parameters |
| 413 | `FILE_TOO_LARGE` | Video exceeds 500MB limit |
| 415 | `UNSUPPORTED_MEDIA_TYPE` | Invalid video format |

---

### 3. Get Job Status

**Purpose**: Check processing status and progress

**Endpoint**: `GET /api/v1/jobs/{jobId}`

**Authentication**: API Key (optional in dev)

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `jobId` | UUID | Job identifier from submit response |

**Response**: `200 OK`

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "created_at": "2026-02-23T10:00:00Z",
  "started_at": "2026-02-23T10:00:05Z",
  "completed_at": null,
  "progress": 45,
  "input_file": "input.mp4",
  "output_file": "550e8400-e29b-41d4-a716-446655440000_blurred_input.mp4",
  "parameters": {
    "languages": ["en"],
    "blur_strength": 51,
    "confidence": 0.5,
    "sample_rate": 5,
    "padding": 10,
    "words": ["password"]
  },
  "result_url": "/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000/result"
}
```

**Status Values**:

| Status | Description |
|--------|-------------|
| `queued` | Job waiting in queue |
| `processing` | Currently processing video |
| `completed` | Processing finished successfully |
| `failed` | Processing failed (see `error` field) |

**Error Responses**:

| Status | Error Code | Description |
|--------|------------|-------------|
| 404 | `JOB_NOT_FOUND` | Invalid or expired job ID |

---

### 4. Download Processed Video

**Purpose**: Download the blurred video file

**Endpoint**: `GET /api/v1/jobs/{jobId}/result`

**Authentication**: API Key (optional in dev)

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `jobId` | UUID | Job identifier |

**Response**: `200 OK`

**Content-Type**: `video/mp4` or `video/quicktime`

Returns binary video data with appropriate headers:
- `Content-Disposition: attachment; filename="output.mp4"`
- `Content-Length: {file_size}`

**Error Responses**:

| Status | Error Code | Description |
|--------|------------|-------------|
| 404 | `JOB_NOT_FOUND` | Job not found |
| 404 | `RESULT_NOT_AVAILABLE` | Job not completed or result deleted |
| 202 | `PROCESSING_IN_PROGRESS` | Job still processing (returns status JSON) |

**202 Response** (still processing):
```json
{
  "message": "Video processing is still in progress",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 45
}
```

---

### 5. Delete Job

**Purpose**: Cancel job or delete results

**Endpoint**: `DELETE /api/v1/jobs/{jobId}`

**Authentication**: API Key (optional in dev)

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `jobId` | UUID | Job identifier |

**Response**: `204 No Content`

**Behavior**:
- Cancels job if still processing
- Deletes input and output files
- Removes job from system

**Error Responses**:

| Status | Error Code | Description |
|--------|------------|-------------|
| 404 | `JOB_NOT_FOUND` | Job not found |

---

## Request/Response Examples

### Example 1: Basic Video Processing

```bash
# Submit video
curl -X POST http://localhost:8000/api/v1/videos/blur \
  -F "video=@input.mp4" \
  -F "blur_strength=71"

# Response
{
  "job_id": "abc123...",
  "status": "queued",
  "created_at": "2026-02-23T10:00:00Z",
  "estimated_duration": 120
}
```

### Example 2: Selective Word Blurring

```bash
# Blur specific words
curl -X POST http://localhost:8000/api/v1/videos/blur \
  -F "video=@sensitive.mp4" \
  -F "words=password" \
  -F "words=email" \
  -F "words=secret" \
  -F "blur_strength=101" \
  -F "padding=20"
```

### Example 3: Multi-Language Processing

```bash
# Support multiple languages
curl -X POST http://localhost:8000/api/v1/videos/blur \
  -F "video=@multilingual.mp4" \
  -F "languages=en" \
  -F "languages=fr" \
  -F "languages=es" \
  -F "sample_rate=3"
```

### Example 4: Complete Workflow with jq

```bash
#!/bin/bash

# Submit video and extract job ID
JOB_ID=$(curl -s -X POST http://localhost:8000/api/v1/videos/blur \
  -F "video=@input.mp4" \
  -F "blur_strength=71" \
  | jq -r '.job_id')

echo "Job ID: $JOB_ID"

# Poll for completion
while true; do
  STATUS=$(curl -s http://localhost:8000/api/v1/jobs/$JOB_ID \
    | jq -r '.status')
  PROGRESS=$(curl -s http://localhost:8000/api/v1/jobs/$JOB_ID \
    | jq -r '.progress // 0')
  
  echo "Status: $STATUS - Progress: $PROGRESS%"
  
  if [ "$STATUS" = "completed" ]; then
    break
  elif [ "$STATUS" = "failed" ]; then
    ERROR=$(curl -s http://localhost:8000/api/v1/jobs/$JOB_ID \
      | jq -r '.error')
    echo "Error: $ERROR"
    exit 1
  fi
  
  sleep 5
done

# Download result
curl -O -J http://localhost:8000/api/v1/jobs/$JOB_ID/result
echo "Download complete!"
```

---

## Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": {
    "field": "Additional context"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description | Solution |
|------|-------------|-------------|----------|
| `INVALID_REQUEST` | 400 | Missing or invalid parameters | Check request format |
| `FILE_TOO_LARGE` | 413 | Video exceeds size limit | Reduce file size or split video |
| `UNSUPPORTED_MEDIA_TYPE` | 415 | Invalid video format | Use MP4 or MOV format |
| `JOB_NOT_FOUND` | 404 | Invalid job ID | Verify job ID is correct |
| `RESULT_NOT_AVAILABLE` | 404 | Result not ready or deleted | Check job status first |
| `PROCESSING_FAILED` | 500 | Video processing error | Check video format and content |

### Error Handling Best Practices

1. **Check HTTP Status**: Always check status code first
2. **Parse Error Response**: Extract error code and message
3. **Implement Retries**: Use exponential backoff for 5xx errors
4. **Validate Input**: Validate parameters before submission
5. **Handle Timeouts**: Set appropriate timeout values

**Example Error Handling** (Python):

```python
import requests
from requests.exceptions import RequestException

def submit_video_safe(video_path, **params):
    try:
        with open(video_path, 'rb') as f:
            files = {'video': f}
            response = requests.post(
                'http://localhost:8000/api/v1/videos/blur',
                files=files,
                data=params,
                timeout=30
            )
        
        # Check for HTTP errors
        response.raise_for_status()
        return response.json()['job_id']
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            error = e.response.json()
            print(f"Invalid request: {error['message']}")
        elif e.response.status_code == 413:
            print("File too large. Please reduce video size.")
        elif e.response.status_code == 415:
            print("Unsupported format. Use MP4 or MOV.")
        else:
            print(f"HTTP error: {e}")
        raise
        
    except RequestException as e:
        print(f"Network error: {e}")
        raise
        
    except FileNotFoundError:
        print(f"Video file not found: {video_path}")
        raise
```

---

## Rate Limiting

### Current Implementation

**Development Mode**: No rate limiting

**Production Recommendations**:
- Implement rate limiting per API key
- Suggested limits:
  - 10 requests per minute per IP
  - 100 requests per hour per API key
  - 1000 requests per day per API key

### Rate Limit Headers

When rate limiting is implemented, responses will include:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1614556800
```

### Handling Rate Limits

```python
def make_request_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url)
        
        if response.status_code == 429:  # Too Many Requests
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limited. Waiting {retry_after} seconds...")
            time.sleep(retry_after)
            continue
        
        return response
    
    raise Exception("Max retries exceeded")
```

---

## Best Practices

### 1. Job Management

**Poll Efficiently**:
```python
# Good: Exponential backoff
wait_time = 5
while status != 'completed':
    time.sleep(wait_time)
    status = get_status(job_id)
    wait_time = min(wait_time * 1.5, 60)  # Max 60 seconds

# Bad: Constant rapid polling
while status != 'completed':
    time.sleep(1)  # Too frequent
    status = get_status(job_id)
```

**Clean Up Jobs**:
```python
# Always delete jobs when done
try:
    result = download_result(job_id)
finally:
    delete_job(job_id)  # Free up resources
```

### 2. File Handling

**Validate Before Upload**:
```python
def validate_video(path):
    # Check file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"Video not found: {path}")
    
    # Check file size
    size = os.path.getsize(path)
    if size > 500 * 1024 * 1024:  # 500MB
        raise ValueError("File too large")
    
    # Check extension
    ext = path.suffix.lower()
    if ext not in ['.mp4', '.mov']:
        raise ValueError("Invalid format. Use MP4 or MOV")
```

**Stream Large Downloads**:
```python
def download_large_file(url, output_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
```

### 3. Error Recovery

**Implement Retry Logic**:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def submit_video_with_retry(video_path, **params):
    return submit_video(video_path, **params)
```

### 4. Performance Optimization

**Use Appropriate Sample Rates**:
```python
# For long videos with static text
params = {'sample_rate': 10}  # Process every 10th frame

# For videos with changing text
params = {'sample_rate': 3}  # More frequent sampling

# For maximum accuracy
params = {'sample_rate': 1}  # Every frame (slow)
```

**Batch Processing**:
```python
from concurrent.futures import ThreadPoolExecutor

def process_videos_batch(video_paths, **params):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(process_video, path, **params)
            for path in video_paths
        ]
        results = [f.result() for f in futures]
    return results
```

---

## Client SDKs

### Official Python Client

See [API_REFERENCE.md](API_REFERENCE.md#example-2-python-client) for the complete Python client implementation.

### JavaScript/Node.js Client

See [API_REFERENCE.md](API_REFERENCE.md#example-3-javascriptnodejs-client) for the complete JavaScript client.

### Generate Custom SDKs

Use OpenAPI Generator to create clients in other languages:

```bash
# Install OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# Generate Python client
openapi-generator-cli generate \
  -i swagger/openapi.yaml \
  -g python \
  -o clients/python

# Generate Java client
openapi-generator-cli generate \
  -i swagger/openapi.yaml \
  -g java \
  -o clients/java

# Generate Go client
openapi-generator-cli generate \
  -i swagger/openapi.yaml \
  -g go \
  -o clients/go
```

### Supported Languages

OpenAPI Generator supports 50+ languages including:
- Python, JavaScript, TypeScript
- Java, Kotlin, Scala
- C#, Go, Rust
- PHP, Ruby, Swift
- And many more...

---

## Testing the API

### Manual Testing with cURL

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Submit test video
curl -X POST http://localhost:8000/api/v1/videos/blur \
  -F "video=@test.mp4" \
  -F "sample_rate=10"

# Check status
curl http://localhost:8000/api/v1/jobs/{job_id}

# Download result
curl -O -J http://localhost:8000/api/v1/jobs/{job_id}/result
```

### Testing with Postman

1. Import OpenAPI spec: `swagger/openapi.yaml`
2. Set base URL: `http://localhost:8000/api/v1`
3. Add API key header (if enabled)
4. Test endpoints interactively

### Automated Testing

```python
import pytest
import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'

def test_submit_video():
    with open('test.mp4', 'rb') as f:
        files = {'video': f}
        response = requests.post(
            f"{BASE_URL}/videos/blur",
            files=files
        )
    assert response.status_code == 202
    assert 'job_id' in response.json()

def test_invalid_video_format():
    with open('test.txt', 'rb') as f:
        files = {'video': f}
        response = requests.post(
            f"{BASE_URL}/videos/blur",
            files=files
        )
    assert response.status_code == 415
```

---

## Production Deployment

### Recommendations

1. **Use Production WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 api_server:app
   ```

2. **Enable API Key Authentication**:
   ```bash
   export API_KEY="your-secure-api-key"
   ```

3. **Use Proper Job Queue**:
   - Replace in-memory storage with Redis or database
   - Use Celery or RQ for job processing

4. **Add Rate Limiting**:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=get_remote_address)
   ```

5. **Enable HTTPS**:
   - Use reverse proxy (Nginx, Apache)
   - Configure SSL/TLS certificates

6. **Monitor and Log**:
   - Use logging framework
   - Monitor with Prometheus/Grafana
   - Track errors with Sentry

---

## See Also

- [API_REFERENCE.md](API_REFERENCE.md) - Complete API reference
- [DOCKER.md](DOCKER.md) - Docker deployment guide
- [swagger/README.md](../swagger/README.md) - REST API server documentation
- [swagger/openapi.yaml](../swagger/openapi.yaml) - OpenAPI specification
- [OpenAPI Specification](https://swagger.io/specification/) - Official OpenAPI docs
- [Swagger Editor](https://editor.swagger.io/) - Online API editor

---

**Document Version**: 1.0.0  
**Last Updated**: February 23, 2026  
**API Version**: v1

---

**End of Swagger API Documentation**