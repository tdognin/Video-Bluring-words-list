# Video Text Blur REST API

REST API server for the Video Text Blur Tool with OpenAPI/Swagger documentation.

## Features

- 🚀 RESTful API for video text blurring
- 📝 Complete OpenAPI 3.0 specification
- 🔄 Asynchronous job processing
- 📊 Job status tracking
- 📥 File upload and download
- 🔍 Swagger UI for interactive testing

## Quick Start

### 1. Install Dependencies

```bash
cd swagger
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
python api_server.py
```

The server will start on `http://localhost:8000`

### 3. View API Documentation

Open your browser and navigate to:
- **Swagger UI**: Use any Swagger UI tool and load `openapi.yaml`
- **Health Check**: http://localhost:8000/api/v1/health

## API Endpoints

### Health Check
```bash
GET /api/v1/health
```

### Submit Video for Blurring
```bash
POST /api/v1/videos/blur
Content-Type: multipart/form-data

Parameters:
- video: Video file (required)
- languages: OCR languages (optional, default: ["en"])
- blur_strength: Blur strength (optional, default: 51)
- confidence: Detection confidence (optional, default: 0.5)
- sample_rate: Frame sampling rate (optional, default: 1)
- padding: Padding around text (optional, default: 10)
- words: Specific words to blur (optional)
```

### Check Job Status
```bash
GET /api/v1/jobs/{jobId}
```

### Download Result
```bash
GET /api/v1/jobs/{jobId}/result
```

### Delete Job
```bash
DELETE /api/v1/jobs/{jobId}
```

## Usage Examples

### Using cURL

#### Submit a video for processing:
```bash
curl -X POST http://localhost:8000/api/v1/videos/blur \
  -F "video=@input.mp4" \
  -F "blur_strength=71" \
  -F "sample_rate=5" \
  -F "languages=en" \
  -F "languages=fr"
```

Response:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "created_at": "2026-02-22T10:00:00Z",
  "estimated_duration": 120
}
```

#### Check job status:
```bash
curl http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000
```

Response:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "created_at": "2026-02-22T10:00:00Z",
  "started_at": "2026-02-22T10:00:05Z",
  "completed_at": "2026-02-22T10:02:30Z",
  "progress": 100,
  "input_file": "input.mp4",
  "output_file": "550e8400-e29b-41d4-a716-446655440000_blurred_input.mp4",
  "result_url": "/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000/result"
}
```

#### Download the result:
```bash
curl -O -J http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000/result
```

### Using Python

```python
import requests
import time

# Submit video
with open('input.mp4', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/videos/blur',
        files={'video': f},
        data={
            'blur_strength': 71,
            'sample_rate': 5,
            'languages': ['en', 'fr']
        }
    )

job_id = response.json()['job_id']
print(f"Job ID: {job_id}")

# Poll for completion
while True:
    status_response = requests.get(
        f'http://localhost:8000/api/v1/jobs/{job_id}'
    )
    status = status_response.json()
    
    print(f"Status: {status['status']} - Progress: {status.get('progress', 0)}%")
    
    if status['status'] == 'completed':
        break
    elif status['status'] == 'failed':
        print(f"Error: {status.get('error')}")
        break
    
    time.sleep(5)

# Download result
if status['status'] == 'completed':
    result_response = requests.get(
        f'http://localhost:8000/api/v1/jobs/{job_id}/result'
    )
    
    with open('output.mp4', 'wb') as f:
        f.write(result_response.content)
    
    print("Video downloaded successfully!")
```

## Configuration

### Environment Variables

- `UPLOAD_FOLDER`: Directory for uploaded files (default: `uploads/`)
- `OUTPUT_FOLDER`: Directory for processed files (default: `outputs/`)
- `MAX_FILE_SIZE`: Maximum upload size in bytes (default: 500MB)

### Production Deployment

For production use, consider:

1. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 api_server:app
   ```

2. **Add authentication** (API keys, OAuth, etc.)

3. **Use a proper job queue** (Celery, RQ) instead of threads

4. **Store jobs in a database** (PostgreSQL, MongoDB) instead of memory

5. **Add rate limiting** to prevent abuse

6. **Use cloud storage** (S3, GCS) for files

7. **Add monitoring and logging**

## OpenAPI Specification

The complete API specification is available in `openapi.yaml`. You can:

- View it in [Swagger Editor](https://editor.swagger.io/)
- Generate client SDKs using [OpenAPI Generator](https://openapi-generator.tech/)
- Import into Postman for testing

## Architecture

```
swagger/
├── openapi.yaml          # OpenAPI 3.0 specification
├── api_server.py         # Flask REST API server
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── uploads/             # Uploaded videos (created at runtime)
└── outputs/             # Processed videos (created at runtime)
```

## Limitations

Current implementation limitations:

- Jobs stored in memory (lost on restart)
- Single-threaded processing
- No authentication/authorization
- No rate limiting
- Local file storage only

These are suitable for development/testing but should be addressed for production use.

## See Also

- [Main Documentation](../Documentation/README.md)
- [API Reference](../Documentation/API_REFERENCE.md)
- [Installation Guide](../Documentation/INSTALLATION.md)

## License

MIT License - See [LICENSE](../LICENSE) file for details.