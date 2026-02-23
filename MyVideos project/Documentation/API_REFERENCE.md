# API Reference

Complete API documentation for the Video Text Blur Tool, including Python API, REST API, and Web Application interfaces.

---

## Table of Contents

1. [Python API](#python-api)
   - [VideoTextBlur Class](#videotextblur-class)
   - [Methods](#methods)
   - [Python API Examples](#python-api-examples)
2. [REST API](#rest-api)
   - [Overview](#rest-api-overview)
   - [Authentication](#authentication)
   - [Endpoints](#endpoints)
   - [Request/Response Schemas](#requestresponse-schemas)
   - [REST API Examples](#rest-api-examples)
3. [Web Application](#web-application)
4. [Command-Line Interface](#command-line-interface)
5. [Return Values and Exceptions](#return-values-and-exceptions)

---

## Python API

### Python API Overview

The Python API provides programmatic access to video text blurring functionality through the `VideoTextBlur` class.

---

## VideoTextBlur Class

The main class for processing videos and blurring text.

### Constructor

```python
VideoTextBlur(languages=['en'], blur_strength=51, confidence_threshold=0.5, target_words=None)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `languages` | `list[str]` | `['en']` | List of language codes for OCR detection (e.g., `['en', 'fr', 'es']`) |
| `blur_strength` | `int` | `51` | Gaussian blur kernel size. Must be odd number. Higher values = stronger blur |
| `confidence_threshold` | `float` | `0.5` | Minimum OCR confidence score (0.0-1.0) to consider text valid |
| `target_words` | `list[str]` or `None` | `None` | List of words/phrases to blur (case-insensitive). If `None`, blurs all detected text |

#### Example

```python
from blur_text_video import VideoTextBlur

# Blur all text
processor = VideoTextBlur(languages=['en'])

# Blur specific words
processor = VideoTextBlur(
    languages=['en', 'fr'],
    blur_strength=71,
    confidence_threshold=0.7,
    target_words=['password', 'email', 'secret']
)
```

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `reader` | `easyocr.Reader` | EasyOCR reader instance for text detection |
| `blur_strength` | `int` | Blur kernel size (automatically adjusted to odd number) |
| `confidence_threshold` | `float` | Minimum confidence for text detection |
| `target_words` | `list[str]` or `None` | Lowercase list of target words to blur |

---

## Methods

### should_blur_text()

Determines if detected text should be blurred based on target words.

```python
should_blur_text(detected_text: str) -> bool
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `detected_text` | `str` | Text detected by OCR |

#### Returns

- `bool`: `True` if text should be blurred, `False` otherwise

#### Behavior

- If `target_words` is `None`, returns `True` (blur all text)
- Performs case-insensitive substring matching
- Returns `True` if any target word is found in detected text

#### Example

```python
processor = VideoTextBlur(target_words=['password', 'email'])

processor.should_blur_text('Password123')  # True
processor.should_blur_text('my email address')  # True
processor.should_blur_text('hello world')  # False
```

---

### detect_text_regions()

Detects text regions in a frame that match target words.

```python
detect_text_regions(frame: np.ndarray) -> list[tuple]
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `frame` | `np.ndarray` | Input video frame (BGR format from OpenCV) |

#### Returns

- `list[tuple]`: List of tuples in format `(x1, y1, x2, y2, text)` where:
  - `x1, y1`: Top-left corner coordinates
  - `x2, y2`: Bottom-right corner coordinates
  - `text`: Detected text string

#### Example

```python
import cv2

processor = VideoTextBlur(target_words=['password'])
frame = cv2.imread('screenshot.png')
boxes = processor.detect_text_regions(frame)

for x1, y1, x2, y2, text in boxes:
    print(f"Found '{text}' at ({x1}, {y1}) to ({x2}, {y2})")
```

---

### blur_regions()

Applies Gaussian blur to specified regions in a frame.

```python
blur_regions(frame: np.ndarray, boxes: list[tuple], padding: int = 10) -> np.ndarray
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `frame` | `np.ndarray` | - | Input video frame |
| `boxes` | `list[tuple]` | - | List of regions to blur `(x1, y1, x2, y2, text)` |
| `padding` | `int` | `10` | Extra pixels to add around each text region |

#### Returns

- `np.ndarray`: Frame with blurred regions

#### Example

```python
import cv2

processor = VideoTextBlur()
frame = cv2.imread('frame.png')
boxes = [(100, 100, 200, 150, 'password')]
blurred_frame = processor.blur_regions(frame, boxes, padding=15)
cv2.imwrite('blurred.png', blurred_frame)
```

---

### process_video()

Main method to process an entire video and blur detected text.

```python
process_video(input_path: str, output_path: str, sample_rate: int = 1, padding: int = 10) -> None
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_path` | `str` or `Path` | - | Path to input video file (MP4/MOV) |
| `output_path` | `str` or `Path` | - | Path to output video file |
| `sample_rate` | `int` | `1` | Process every Nth frame for text detection. Higher = faster but may miss text changes |
| `padding` | `int` | `10` | Padding around detected text regions in pixels |

#### Returns

- `None`: Writes output video to disk

#### Raises

- `FileNotFoundError`: If input video doesn't exist
- `ValueError`: If video cannot be opened or output cannot be created
- `subprocess.CalledProcessError`: If FFmpeg conversion fails (falls back to temporary file)

#### Process Flow

1. Opens input video with OpenCV
2. Reads video properties (FPS, resolution, frame count)
3. Creates temporary output with H.264 codec
4. Processes frames:
   - Detects text on sampled frames
   - Applies blur to all frames using last detected boxes
5. Converts to QuickTime-compatible format with FFmpeg
6. Removes temporary file

#### Example

```python
processor = VideoTextBlur(
    languages=['en'],
    target_words=['password', 'email']
)

processor.process_video(
    input_path='input.mp4',
    output_path='output.mp4',
    sample_rate=5,
    padding=15
)
```

---

## Command-Line Interface

### Basic Syntax

```bash
python blur_text_video.py INPUT OUTPUT [OPTIONS]
```

### Positional Arguments

| Argument | Description |
|----------|-------------|
| `INPUT` | Input video file path (MP4/MOV) |
| `OUTPUT` | Output video file path |

### Optional Arguments

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--words WORD [WORD ...]` | `str` | `None` | Specific words/phrases to blur (case-insensitive) |
| `--blur-all` | flag | `False` | Blur ALL detected text (ignores `--words`) |
| `--languages LANG [LANG ...]` | `str` | `['en']` | OCR language codes |
| `--blur N` | `int` | `51` | Blur strength (odd number) |
| `--confidence N` | `float` | `0.5` | Text detection confidence threshold (0.0-1.0) |
| `--sample-rate N` | `int` | `1` | Process every Nth frame |
| `--padding N` | `int` | `10` | Padding around text regions in pixels |
| `-h, --help` | flag | - | Show help message |

### CLI Examples

```bash
# Interactive mode (prompts for words)
python blur_text_video.py input.mp4 output.mp4

# Blur specific words
python blur_text_video.py input.mp4 output.mp4 --words "password" "email" "secret"

# Blur all text
python blur_text_video.py input.mp4 output.mp4 --blur-all

# Custom settings
python blur_text_video.py input.mp4 output.mp4 \
    --words "confidential" \
    --blur 71 \
    --sample-rate 5 \
    --padding 20

# Multiple languages
python blur_text_video.py input.mp4 output.mp4 \
    --words "mot" "texte" \
    --languages en fr es
```

---

## Python API Examples

### Example 1: Basic Usage

```python
from blur_text_video import VideoTextBlur

# Create processor
processor = VideoTextBlur(languages=['en'])

# Process video
processor.process_video('input.mp4', 'output.mp4')
```

### Example 2: Blur Specific Words

```python
from blur_text_video import VideoTextBlur

# Blur only passwords and emails
processor = VideoTextBlur(
    languages=['en'],
    target_words=['password', 'email', 'secret']
)

processor.process_video(
    input_path='sensitive.mp4',
    output_path='redacted.mp4',
    sample_rate=3,
    padding=15
)
```

### Example 3: Multi-Language Support

```python
from blur_text_video import VideoTextBlur

# Support English and French
processor = VideoTextBlur(
    languages=['en', 'fr'],
    target_words=['password', 'mot de passe', 'email', 'courriel']
)

processor.process_video('multilingual.mp4', 'output.mp4')
```

### Example 4: High-Quality Blur

```python
from blur_text_video import VideoTextBlur

# Strong blur with high confidence
processor = VideoTextBlur(
    languages=['en'],
    blur_strength=101,  # Very strong blur
    confidence_threshold=0.7,  # High confidence only
    target_words=['confidential', 'secret']
)

processor.process_video(
    input_path='sensitive.mp4',
    output_path='secure.mp4',
    sample_rate=1,  # Process every frame
    padding=25  # Extra padding
)
```

### Example 5: Batch Processing

```python
from blur_text_video import VideoTextBlur
from pathlib import Path

# Process multiple videos
processor = VideoTextBlur(
    languages=['en'],
    target_words=['password', 'email']
)

videos = Path('.').glob('*.mp4')
for video in videos:
    output = f"blurred_{video.name}"
    print(f"Processing {video}...")
    processor.process_video(video, output, sample_rate=5)
```

### Example 6: Error Handling

```python
from blur_text_video import VideoTextBlur
from pathlib import Path

try:
    processor = VideoTextBlur(
        languages=['en'],
        target_words=['password']
    )
    
    input_file = 'input.mp4'
    if not Path(input_file).exists():
        raise FileNotFoundError(f"Video not found: {input_file}")
    
    processor.process_video(input_file, 'output.mp4')
    print("✓ Processing complete!")
    
except FileNotFoundError as e:
    print(f"Error: {e}")
except ValueError as e:
    print(f"Invalid video: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Return Values and Exceptions

### Return Values

| Method | Return Type | Description |
|--------|-------------|-------------|
| `should_blur_text()` | `bool` | Whether text should be blurred |
| `detect_text_regions()` | `list[tuple]` | List of text regions with coordinates |
| `blur_regions()` | `np.ndarray` | Frame with blurred regions |
| `process_video()` | `None` | Writes output to disk |

### Exceptions

#### FileNotFoundError

Raised when input video file doesn't exist.

```python
try:
    processor.process_video('nonexistent.mp4', 'output.mp4')
except FileNotFoundError as e:
    print(f"File not found: {e}")
```

#### ValueError

Raised when:
- Video cannot be opened (corrupted or unsupported format)
- Output video cannot be created (invalid path or permissions)

```python
try:
    processor.process_video('corrupted.mp4', 'output.mp4')
except ValueError as e:
    print(f"Video error: {e}")
```

#### subprocess.CalledProcessError

Raised when FFmpeg conversion fails. The tool handles this gracefully by falling back to the temporary output file.

```python
# Handled internally - user sees warning but processing continues
```

#### KeyboardInterrupt

Raised when user interrupts processing (Ctrl+C). Handled by CLI.

```python
# In CLI mode, shows "Process interrupted by user" message
```

---

## Type Hints

For type checking with mypy or similar tools:

```python
from typing import List, Tuple, Optional
import numpy as np
from pathlib import Path

class VideoTextBlur:
    def __init__(
        self,
        languages: List[str] = ['en'],
        blur_strength: int = 51,
        confidence_threshold: float = 0.5,
        target_words: Optional[List[str]] = None
    ) -> None: ...
    
    def should_blur_text(self, detected_text: str) -> bool: ...
    
    def detect_text_regions(
        self,
        frame: np.ndarray
    ) -> List[Tuple[int, int, int, int, str]]: ...
    
    def blur_regions(
        self,
        frame: np.ndarray,
        boxes: List[Tuple[int, int, int, int, str]],
        padding: int = 10
    ) -> np.ndarray: ...
    
    def process_video(
        self,
        input_path: str | Path,
        output_path: str | Path,
        sample_rate: int = 1,
        padding: int = 10
    ) -> None: ...
```

---

## Performance Considerations

### Memory Usage

- Each frame is loaded into memory during processing
- Peak memory usage: ~3x frame size (original + blurred + output buffer)
- For 1080p video: ~20MB per frame

### Processing Speed

Factors affecting speed:
- **Sample rate**: Higher = faster (recommended: 3-10 for most videos)
- **Resolution**: 4K takes ~4x longer than 1080p
- **GPU**: CUDA-enabled GPU provides 3-5x speedup
- **Blur strength**: Higher values slightly slower
- **Text density**: More text = slower processing

### Optimization Tips

```python
# Fast processing for long videos
processor = VideoTextBlur(
    languages=['en'],
    target_words=['password'],
    confidence_threshold=0.6  # Higher = faster
)
processor.process_video(
    'long_video.mp4',
    'output.mp4',
    sample_rate=10  # Process every 10th frame
)

# High quality for short videos
processor = VideoTextBlur(
    languages=['en'],
    target_words=['password'],
    confidence_threshold=0.3  # Lower = more thorough
)
processor.process_video(
    'short_video.mp4',
    'output.mp4',
    sample_rate=1  # Process every frame
)
```

---


---

## REST API

### REST API Overview

The Video Text Blur REST API provides HTTP endpoints for video processing operations. The API follows RESTful principles and uses JSON for request/response payloads.

**Base URL**: `http://localhost:8000/api/v1`

**API Specification**: OpenAPI 3.0 (see `swagger/openapi.yaml`)

**Interactive Documentation**: Available via Swagger UI

### Authentication

Most endpoints require API key authentication via the `X-API-Key` header.

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/v1/jobs/{jobId}
```

**Public Endpoints** (no authentication required):
- `GET /api/v1/health` - Health check

**Note**: API key authentication is optional in development mode. Set the `API_KEY` environment variable to enable it.

### Endpoints

#### Health Check

Check if the API service is running.

**Endpoint**: `GET /api/v1/health`

**Authentication**: None required

**Response**: `200 OK`

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-23T10:00:00Z"
}
```

**Example**:
```bash
curl http://localhost:8000/api/v1/health
```

---

#### Submit Video for Blurring

Upload a video file and configure blur parameters. Returns a job ID for tracking.

**Endpoint**: `POST /api/v1/videos/blur`

**Authentication**: API Key (optional in dev mode)

**Content-Type**: `multipart/form-data`

**Request Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `video` | file | Yes | - | Video file (MP4 or MOV format) |
| `languages` | array[string] | No | `["en"]` | OCR languages to use |
| `blur_strength` | integer | No | `51` | Blur strength (must be odd number) |
| `confidence` | float | No | `0.5` | Text detection confidence threshold (0-1) |
| `sample_rate` | integer | No | `1` | Process every Nth frame |
| `padding` | integer | No | `10` | Padding around text regions in pixels |
| `words` | array[string] | No | `null` | Specific words to blur (optional) |

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
- `400 Bad Request` - Invalid request parameters
- `413 Payload Too Large` - Video file exceeds size limit (500MB)
- `415 Unsupported Media Type` - Invalid video format

**Example**:
```bash
curl -X POST http://localhost:8000/api/v1/videos/blur \
  -F "video=@input.mp4" \
  -F "blur_strength=71" \
  -F "sample_rate=5" \
  -F "languages=en" \
  -F "languages=fr" \
  -F "words=password" \
  -F "words=email"
```

---

#### Get Job Status

Check the processing status of a video blur job.

**Endpoint**: `GET /api/v1/jobs/{jobId}`

**Authentication**: API Key (optional in dev mode)

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `jobId` | string (UUID) | Job ID returned from blur request |

**Response**: `200 OK`

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "created_at": "2026-02-23T10:00:00Z",
  "started_at": "2026-02-23T10:00:05Z",
  "progress": 45,
  "input_file": "input.mp4",
  "output_file": "output.mp4",
  "parameters": {
    "languages": ["en"],
    "blur_strength": 51,
    "confidence": 0.5,
    "sample_rate": 5,
    "padding": 10,
    "words": ["password"]
  }
}
```

**Status Values**:
- `queued` - Job is waiting to be processed
- `processing` - Job is currently being processed
- `completed` - Job completed successfully
- `failed` - Job failed with error

**Error Responses**:
- `404 Not Found` - Job ID not found

**Example**:
```bash
curl http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000
```

---

#### Download Processed Video

Download the blurred video once processing is complete.

**Endpoint**: `GET /api/v1/jobs/{jobId}/result`

**Authentication**: API Key (optional in dev mode)

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `jobId` | string (UUID) | Job ID |

**Response**: `200 OK`

**Content-Type**: `video/mp4` or `video/quicktime`

Returns the processed video file as binary data.

**Error Responses**:
- `404 Not Found` - Job not found or result not available
- `202 Accepted` - Processing not yet complete (returns status JSON)

**Example**:
```bash
# Download with original filename
curl -O -J http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000/result

# Download to specific file
curl -o output.mp4 http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000/result
```

---

#### Delete Job

Cancel a running job or delete a completed job and its results.

**Endpoint**: `DELETE /api/v1/jobs/{jobId}`

**Authentication**: API Key (optional in dev mode)

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `jobId` | string (UUID) | Job ID |

**Response**: `204 No Content`

**Error Responses**:
- `404 Not Found` - Job not found

**Example**:
```bash
curl -X DELETE http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000
```

---

### Request/Response Schemas

#### JobResponse Schema

```json
{
  "job_id": "string (UUID)",
  "status": "queued | processing | completed | failed",
  "created_at": "string (ISO 8601 datetime)",
  "estimated_duration": "integer (seconds)"
}
```

#### JobStatus Schema

```json
{
  "job_id": "string (UUID)",
  "status": "queued | processing | completed | failed",
  "created_at": "string (ISO 8601 datetime)",
  "started_at": "string (ISO 8601 datetime, optional)",
  "completed_at": "string (ISO 8601 datetime, optional)",
  "progress": "integer (0-100)",
  "input_file": "string",
  "output_file": "string",
  "parameters": {
    "languages": ["string"],
    "blur_strength": "integer",
    "confidence": "float",
    "sample_rate": "integer",
    "padding": "integer",
    "words": ["string"] or null
  },
  "error": "string (optional)",
  "result_url": "string (optional)"
}
```

#### Error Schema

```json
{
  "error": "string (error code)",
  "message": "string (human-readable message)",
  "details": {
    "additional": "error details"
  }
}
```

---

### REST API Examples

#### Example 1: Complete Workflow

```bash
# 1. Submit video for processing
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/videos/blur \
  -F "video=@input.mp4" \
  -F "blur_strength=71" \
  -F "sample_rate=5")

# 2. Extract job ID
JOB_ID=$(echo $RESPONSE | jq -r '.job_id')
echo "Job ID: $JOB_ID"

# 3. Poll for completion
while true; do
  STATUS=$(curl -s http://localhost:8000/api/v1/jobs/$JOB_ID | jq -r '.status')
  echo "Status: $STATUS"
  
  if [ "$STATUS" = "completed" ]; then
    break
  elif [ "$STATUS" = "failed" ]; then
    echo "Job failed!"
    exit 1
  fi
  
  sleep 5
done

# 4. Download result
curl -O -J http://localhost:8000/api/v1/jobs/$JOB_ID/result
echo "Download complete!"
```

#### Example 2: Python Client

```python
import requests
import time
from pathlib import Path

class VideoBlurClient:
    def __init__(self, base_url="http://localhost:8000/api/v1"):
        self.base_url = base_url
    
    def submit_video(self, video_path, **params):
        """Submit video for processing."""
        with open(video_path, 'rb') as f:
            files = {'video': f}
            response = requests.post(
                f"{self.base_url}/videos/blur",
                files=files,
                data=params
            )
        response.raise_for_status()
        return response.json()['job_id']
    
    def get_status(self, job_id):
        """Get job status."""
        response = requests.get(f"{self.base_url}/jobs/{job_id}")
        response.raise_for_status()
        return response.json()
    
    def download_result(self, job_id, output_path):
        """Download processed video."""
        response = requests.get(f"{self.base_url}/jobs/{job_id}/result")
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
    
    def process_video(self, video_path, output_path, **params):
        """Complete workflow: submit, wait, download."""
        # Submit
        job_id = self.submit_video(video_path, **params)
        print(f"Job submitted: {job_id}")
        
        # Wait for completion
        while True:
            status = self.get_status(job_id)
            print(f"Status: {status['status']} - Progress: {status.get('progress', 0)}%")
            
            if status['status'] == 'completed':
                break
            elif status['status'] == 'failed':
                raise Exception(f"Job failed: {status.get('error')}")
            
            time.sleep(5)
        
        # Download
        self.download_result(job_id, output_path)
        print(f"Video saved to: {output_path}")

# Usage
client = VideoBlurClient()
client.process_video(
    'input.mp4',
    'output.mp4',
    blur_strength=71,
    sample_rate=5,
    languages=['en', 'fr'],
    words=['password', 'email']
)
```

#### Example 3: JavaScript/Node.js Client

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

class VideoBlurClient {
  constructor(baseURL = 'http://localhost:8000/api/v1') {
    this.baseURL = baseURL;
  }

  async submitVideo(videoPath, params = {}) {
    const form = new FormData();
    form.append('video', fs.createReadStream(videoPath));
    
    Object.entries(params).forEach(([key, value]) => {
      if (Array.isArray(value)) {
        value.forEach(v => form.append(key, v));
      } else {
        form.append(key, value);
      }
    });

    const response = await axios.post(
      `${this.baseURL}/videos/blur`,
      form,
      { headers: form.getHeaders() }
    );
    
    return response.data.job_id;
  }

  async getStatus(jobId) {
    const response = await axios.get(`${this.baseURL}/jobs/${jobId}`);
    return response.data;
  }

  async downloadResult(jobId, outputPath) {
    const response = await axios.get(
      `${this.baseURL}/jobs/${jobId}/result`,
      { responseType: 'stream' }
    );
    
    const writer = fs.createWriteStream(outputPath);
    response.data.pipe(writer);
    
    return new Promise((resolve, reject) => {
      writer.on('finish', resolve);
      writer.on('error', reject);
    });
  }

  async processVideo(videoPath, outputPath, params = {}) {
    // Submit
    const jobId = await this.submitVideo(videoPath, params);
    console.log(`Job submitted: ${jobId}`);
    
    // Wait for completion
    while (true) {
      const status = await this.getStatus(jobId);
      console.log(`Status: ${status.status} - Progress: ${status.progress || 0}%`);
      
      if (status.status === 'completed') {
        break;
      } else if (status.status === 'failed') {
        throw new Error(`Job failed: ${status.error}`);
      }
      
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
    
    // Download
    await this.downloadResult(jobId, outputPath);
    console.log(`Video saved to: ${outputPath}`);
  }
}

// Usage
const client = new VideoBlurClient();
client.processVideo('input.mp4', 'output.mp4', {
  blur_strength: 71,
  sample_rate: 5,
  languages: ['en', 'fr'],
  words: ['password', 'email']
}).catch(console.error);
```

---

## Web Application

### Web Application Overview

The Video Blurring Web Application provides a browser-based interface for video text blurring with client-side processing.

**URL**: `http://localhost:8080` (when running with Docker)

**Features**:
- Client-side video processing (no server upload required)
- Real-time preview
- Drag-and-drop file upload
- Configurable blur parameters
- Progress tracking
- Download processed video

### Web Application Usage

1. **Access the Application**:
   ```bash
   # Using Docker
   cd "VideoBluring WebApp/Docker"
   docker-compose up -d
   open http://localhost:8080
   ```

2. **Upload Video**:
   - Drag and drop video file or click to browse
   - Supported formats: MP4, MOV

3. **Configure Settings**:
   - Blur strength: Adjust slider (1-100)
   - Sample rate: Process every Nth frame
   - Languages: Select OCR languages
   - Target words: Enter specific words to blur

4. **Process Video**:
   - Click "Process Video" button
   - Monitor progress bar
   - Preview results in real-time

5. **Download Result**:
   - Click "Download" button when complete
   - Video saved to your downloads folder

### Web Application API

The web application uses the browser's File API and Web Workers for client-side processing:

```javascript
// Example: Process video in browser
const processor = new VideoProcessor({
  blurStrength: 71,
  sampleRate: 5,
  languages: ['en'],
  targetWords: ['password', 'email']
});

processor.on('progress', (percent) => {
  console.log(`Progress: ${percent}%`);
});

processor.on('complete', (blob) => {
  // Download processed video
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'output.mp4';
  a.click();
});

processor.processVideo(videoFile);
```

---
## Version Information

**API Version**: 1.0.0  
**Last Updated**: February 22, 2026  
**Compatibility**: Python 3.8+

---

## See Also

- [README.md](README.md) - Quick start guide
- [SWAGGER_API.md](SWAGGER_API.md) - Detailed Swagger/OpenAPI documentation
- [DOCKER.md](DOCKER.md) - Docker deployment guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) - Comprehensive technical reference
- [UPDATED_FEATURES.md](UPDATED_FEATURES.md) - Feature documentation
- [example_usage.py](../example_usage.py) - Code examples
- [swagger/openapi.yaml](../swagger/openapi.yaml) - OpenAPI specification
- [swagger/README.md](../swagger/README.md) - REST API server documentation
- [VideoBluring WebApp/Docker/README.md](../VideoBluring%20WebApp/Docker/README.md) - Docker setup guide

---

**API Reference Version**: 2.0.0
**Last Updated**: February 23, 2026
**Includes**: Python API, REST API, Web Application

---

**End of API Reference**