# Architecture Documentation

Comprehensive architecture documentation for the Video Text Blur Tool.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Component Architecture](#component-architecture)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [Design Patterns](#design-patterns)
7. [Processing Pipeline](#processing-pipeline)
8. [Memory Management](#memory-management)
9. [Performance Architecture](#performance-architecture)
10. [Security Architecture](#security-architecture)
11. [Extensibility](#extensibility)

---

## System Overview

The Video Text Blur Tool is a Python-based video processing application that uses computer vision and optical character recognition (OCR) to detect and blur text in video files.

### Key Characteristics

- **Type**: Desktop application / Python library
- **Architecture Style**: Pipeline architecture with modular components
- **Processing Model**: Frame-by-frame sequential processing
- **Deployment**: Local execution (no server required)
- **Data Storage**: Temporary file-based (no database)

### Core Capabilities

1. **Text Detection**: OCR-based text recognition in video frames
2. **Selective Blurring**: Target specific words or blur all text
3. **Video Processing**: Frame manipulation and video encoding
4. **Format Conversion**: QuickTime-compatible H.264 output

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  CLI Interface          │  Python API          │  Shell Scripts  │
│  (argparse)            │  (VideoTextBlur)     │  (bash)         │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
├─────────────────────────────────────────────────────────────────┤
│                     VideoTextBlur Class                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Initialization│  │Text Detection│  │Blur Processing│         │
│  │   & Config   │  │   Pipeline   │  │   Pipeline    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Processing Layer                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Frame Reader │  │  OCR Engine  │  │ Blur Engine  │         │
│  │  (OpenCV)    │  │  (EasyOCR)   │  │  (OpenCV)    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │Frame Writer  │  │Text Matching │  │Region Extract│         │
│  │  (OpenCV)    │  │   (Python)   │  │  (NumPy)     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Infrastructure Layer                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │Video Codecs  │  │  GPU/CUDA    │  │File System   │         │
│  │  (FFmpeg)    │  │  (PyTorch)   │  │  (pathlib)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. User Interface Layer

#### CLI Interface (`main()` function)
- **Responsibility**: Parse command-line arguments and orchestrate processing
- **Dependencies**: `argparse`, `sys`
- **Input**: Command-line arguments
- **Output**: Processed video file

```python
# Entry point
main() → parse_args() → VideoTextBlur() → process_video()
```

#### Python API (`VideoTextBlur` class)
- **Responsibility**: Provide programmatic access to video processing
- **Dependencies**: Core processing components
- **Usage**: Import and instantiate in Python scripts

#### Shell Scripts
- **Responsibility**: Convenience wrappers for common operations
- **Files**: `run_blur.sh`, `run_blur_interactive.sh`
- **Purpose**: Simplify execution for end users

### 2. Application Layer

#### VideoTextBlur Class

**Core Responsibilities**:
1. Initialize OCR engine
2. Manage processing configuration
3. Coordinate text detection and blurring
4. Handle video I/O operations

**Key Methods**:
- `__init__()`: Initialize with configuration
- `should_blur_text()`: Text matching logic
- `detect_text_regions()`: OCR integration
- `blur_regions()`: Apply blur effects
- `process_video()`: Main processing pipeline

**State Management**:
- `reader`: EasyOCR reader instance (persistent)
- `blur_strength`: Blur kernel size
- `confidence_threshold`: OCR confidence filter
- `target_words`: Words to blur (optional)

### 3. Processing Layer

#### Frame Reader (OpenCV)
```python
cv2.VideoCapture(input_path)
cap.read() → (success, frame)
```
- Reads video frames sequentially
- Provides video metadata (FPS, resolution, frame count)

#### OCR Engine (EasyOCR)
```python
reader.readtext(frame) → [(bbox, text, confidence), ...]
```
- Detects text in frames
- Returns bounding boxes and confidence scores
- Supports 80+ languages

#### Text Matching (Python)
```python
should_blur_text(detected_text) → bool
```
- Case-insensitive substring matching
- Filters text based on target words
- Returns boolean decision

#### Blur Engine (OpenCV)
```python
cv2.GaussianBlur(roi, kernel_size, sigma) → blurred_roi
```
- Applies Gaussian blur to regions
- Configurable kernel size
- Preserves image dimensions

#### Frame Writer (OpenCV)
```python
cv2.VideoWriter(output_path, fourcc, fps, size)
out.write(frame)
```
- Writes processed frames to video
- Uses H.264 codec (avc1)
- Maintains original FPS and resolution

#### Region Extraction (NumPy)
```python
roi = frame[y1:y2, x1:x2]
```
- Extracts rectangular regions from frames
- Efficient array slicing
- Handles padding calculations

### 4. Infrastructure Layer

#### Video Codecs (FFmpeg)
```bash
ffmpeg -i temp.mp4 -c:v libx264 -pix_fmt yuv420p output.mp4
```
- Converts to QuickTime-compatible format
- Optimizes for streaming (faststart)
- Handles audio/video synchronization

#### GPU/CUDA (PyTorch)
- Accelerates OCR processing
- Automatic GPU detection
- Falls back to CPU if unavailable

#### File System (pathlib)
- Cross-platform path handling
- File existence checks
- Temporary file management

---

## Data Flow

### High-Level Flow

```
Input Video → Frame Extraction → Text Detection → Text Matching → 
Blur Application → Frame Writing → Format Conversion → Output Video
```

### Detailed Flow

```
1. INPUT STAGE
   ├─ Read video file (MP4/MOV)
   ├─ Extract metadata (FPS, resolution, frame count)
   └─ Initialize video writer

2. PROCESSING STAGE (per frame)
   ├─ Read frame from input video
   ├─ [Every Nth frame] Detect text with OCR
   │  ├─ Convert frame to RGB
   │  ├─ Run EasyOCR detection
   │  ├─ Filter by confidence threshold
   │  └─ Match against target words
   ├─ Apply blur to detected regions
   │  ├─ Extract region with padding
   │  ├─ Apply Gaussian blur
   │  └─ Replace region in frame
   └─ Write frame to temporary output

3. OUTPUT STAGE
   ├─ Close video writer
   ├─ Convert to H.264 with FFmpeg
   ├─ Delete temporary file
   └─ Return output path
```

### Data Structures

#### Frame Data
```python
frame: np.ndarray  # Shape: (height, width, 3), dtype: uint8, format: BGR
```

#### Text Detection Results
```python
detection: tuple = (bbox, text, confidence)
bbox: list = [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]  # 4 corner points
text: str  # Detected text
confidence: float  # 0.0 to 1.0
```

#### Bounding Boxes
```python
box: tuple = (x1, y1, x2, y2, text)
x1, y1: int  # Top-left corner
x2, y2: int  # Bottom-right corner
text: str    # Detected text
```

---

## Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Language | Python | 3.8+ | Core implementation |
| Computer Vision | OpenCV | 4.8.0+ | Video I/O and image processing |
| OCR | EasyOCR | 1.7.0+ | Text detection |
| Deep Learning | PyTorch | Latest | OCR model backend |
| Video Encoding | FFmpeg | Latest | Format conversion |
| Array Processing | NumPy | 1.24.0+ | Numerical operations |
| Image Processing | Pillow | 10.0.0+ | Image utilities |
| Progress Display | tqdm | 4.65.0+ | Progress bars |

### Development Tools

| Tool | Purpose |
|------|---------|
| Git | Version control |
| pip | Package management |
| venv | Virtual environments |
| argparse | CLI argument parsing |
| pathlib | Path manipulation |
| subprocess | External process execution |

---

## Design Patterns

### 1. Facade Pattern

The `VideoTextBlur` class acts as a facade, providing a simple interface to complex subsystems (OCR, video processing, blur effects).

```python
# Simple interface
processor = VideoTextBlur(languages=['en'])
processor.process_video('input.mp4', 'output.mp4')

# Hides complexity of:
# - OCR initialization
# - Video codec management
# - Frame-by-frame processing
# - Format conversion
```

### 2. Strategy Pattern

Text matching strategy can be configured at runtime:

```python
# Strategy 1: Blur all text
processor = VideoTextBlur(target_words=None)

# Strategy 2: Blur specific words
processor = VideoTextBlur(target_words=['password', 'email'])
```

### 3. Pipeline Pattern

Processing follows a clear pipeline:

```python
Frame → Detect → Match → Blur → Write
```

Each stage is independent and can be modified without affecting others.

### 4. Template Method Pattern

`process_video()` defines the algorithm skeleton:

```python
def process_video(self, input_path, output_path, sample_rate, padding):
    # Template method
    self._open_video(input_path)
    self._setup_writer(output_path)
    while self._has_frames():
        frame = self._read_frame()
        if self._should_detect(frame_count, sample_rate):
            boxes = self._detect_text(frame)
        frame = self._apply_blur(frame, boxes, padding)
        self._write_frame(frame)
    self._finalize_output()
```

### 5. Singleton Pattern (Implicit)

EasyOCR reader is initialized once per `VideoTextBlur` instance:

```python
def __init__(self, languages, ...):
    self.reader = easyocr.Reader(languages, gpu=True)  # Expensive operation
    # Reader is reused for all frames
```

---

## Processing Pipeline

### Frame Processing Pipeline

```
┌─────────────┐
│ Input Frame │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Sample Decision │ ◄── sample_rate parameter
└──────┬──────────┘
       │
       ├─── Yes (sample_rate match)
       │    │
       │    ▼
       │  ┌──────────────┐
       │  │ OCR Detection│
       │  └──────┬───────┘
       │         │
       │         ▼
       │  ┌──────────────┐
       │  │Text Filtering│ ◄── confidence_threshold
       │  └──────┬───────┘
       │         │
       │         ▼
       │  ┌──────────────┐
       │  │Word Matching │ ◄── target_words
       │  └──────┬───────┘
       │         │
       │         ▼
       │  ┌──────────────┐
       │  │ Store Boxes  │
       │  └──────┬───────┘
       │         │
       └─────────┘
       │
       ▼
┌─────────────────┐
│  Apply Blur     │ ◄── blur_strength, padding
│  (using boxes)  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Write Frame    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Next Frame     │
└─────────────────┘
```

### OCR Detection Pipeline

```
Frame (BGR) → Convert to RGB → EasyOCR Reader → Raw Detections
                                                       │
                                                       ▼
                                            ┌──────────────────┐
                                            │ For each detection│
                                            └────────┬─────────┘
                                                     │
                                                     ▼
                                            ┌──────────────────┐
                                            │Check confidence  │
                                            └────────┬─────────┘
                                                     │
                                                     ├─── Pass
                                                     │    │
                                                     │    ▼
                                                     │  ┌──────────────┐
                                                     │  │Extract bbox  │
                                                     │  └──────┬───────┘
                                                     │         │
                                                     │         ▼
                                                     │  ┌──────────────┐
                                                     │  │Match words   │
                                                     │  └──────┬───────┘
                                                     │         │
                                                     │         ├─── Match
                                                     │         │    │
                                                     │         │    ▼
                                                     │         │  ┌──────────┐
                                                     │         │  │Add to list│
                                                     │         │  └──────────┘
                                                     │         │
                                                     │         └─── No match
                                                     │              (skip)
                                                     │
                                                     └─── Fail (skip)
```

### Blur Application Pipeline

```
Frame + Boxes → For each box:
                    │
                    ▼
                ┌──────────────┐
                │Add padding   │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │Clamp to frame│
                │  boundaries  │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │Extract ROI   │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │Apply Gaussian│
                │    blur      │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │Replace in    │
                │   frame      │
                └──────┬───────┘
                       │
                       ▼
                Next box or return blurred frame
```

---

## Memory Management

### Memory Usage Patterns

#### Per-Frame Memory

```python
# Single frame (1080p)
frame_size = 1920 * 1080 * 3 bytes = 6.2 MB

# Processing memory
original_frame = 6.2 MB
blurred_frame = 6.2 MB
roi_buffer = variable (typically < 1 MB)
Total per frame ≈ 13-15 MB
```

#### OCR Model Memory

```python
# EasyOCR models (loaded once)
english_model ≈ 100 MB
additional_languages ≈ 50-100 MB each
GPU memory (if available) ≈ 500 MB - 2 GB
```

#### Video Writer Buffer

```python
# OpenCV video writer buffer
buffer_size ≈ 10-20 frames = 60-120 MB (1080p)
```

### Memory Optimization Strategies

1. **Frame-by-Frame Processing**: Only one frame in memory at a time
2. **In-Place Operations**: Modify frames directly when possible
3. **Garbage Collection**: Frames released after writing
4. **Temporary File Cleanup**: Delete intermediate files
5. **Sample Rate**: Reduce OCR frequency to save memory

### Memory Leak Prevention

```python
# Proper resource cleanup
try:
    cap = cv2.VideoCapture(input_path)
    out = cv2.VideoWriter(output_path, ...)
    # Process video
finally:
    cap.release()  # Always release
    out.release()  # Always release
    cv2.destroyAllWindows()  # Clean up OpenCV windows
```

---

## Performance Architecture

### Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Frame Reading | O(1) per frame | O(1) |
| OCR Detection | O(n) where n = text regions | O(m) where m = model size |
| Text Matching | O(k) where k = target words | O(1) |
| Blur Application | O(w*h) where w,h = region size | O(1) |
| Frame Writing | O(1) per frame | O(1) |

### Bottlenecks

1. **OCR Detection** (70-80% of processing time)
   - Solution: Increase sample rate
   - Solution: Use GPU acceleration

2. **Video Encoding** (10-15% of processing time)
   - Solution: Use hardware encoding (if available)
   - Solution: Adjust CRF quality setting

3. **Disk I/O** (5-10% of processing time)
   - Solution: Use SSD storage
   - Solution: Reduce temporary file writes

### Optimization Techniques

#### 1. Frame Sampling

```python
# Process every 5th frame
processor.process_video(
    'input.mp4',
    'output.mp4',
    sample_rate=5  # 5x faster
)
```

#### 2. GPU Acceleration

```python
# Automatic GPU detection
reader = easyocr.Reader(['en'], gpu=True)
# Falls back to CPU if GPU unavailable
```

#### 3. Confidence Filtering

```python
# Higher confidence = fewer false positives = faster
processor = VideoTextBlur(confidence_threshold=0.7)
```

#### 4. Reduced Resolution

```bash
# Pre-process video to lower resolution
ffmpeg -i input.mp4 -vf scale=1280:720 input_720p.mp4
python blur_text_video.py input_720p.mp4 output.mp4
```

### Performance Benchmarks

See [TECHNICAL_DOCUMENTATION.md - Appendix D](TECHNICAL_DOCUMENTATION.md#d-performance-benchmarks) for detailed benchmarks.

---

## Security Architecture

### Security Principles

1. **Local Processing**: All data processed locally, no external servers
2. **No Data Persistence**: No database or permanent storage of video content
3. **Temporary File Cleanup**: Intermediate files deleted after processing
4. **Input Validation**: File existence and format checks
5. **Error Handling**: Graceful failure without exposing sensitive data

### Security Considerations

#### Input Validation

```python
# File existence check
if not input_path.exists():
    raise FileNotFoundError(f"Input video not found: {input_path}")

# Video format validation
cap = cv2.VideoCapture(str(input_path))
if not cap.isOpened():
    raise ValueError(f"Could not open video: {input_path}")
```

#### Temporary File Handling

```python
# Secure temporary file creation
temp_output = output_path.with_suffix('.temp.mp4')

try:
    # Process video
    process_frames()
finally:
    # Always cleanup
    if temp_output.exists():
        temp_output.unlink()
```

#### Error Message Sanitization

```python
# Don't expose full paths in error messages
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)  # Generic error
    # Not: print(f"Error at {full_system_path}: {e}")
```

### Privacy Features

1. **Selective Blurring**: Only blur specified sensitive words
2. **No Logging**: No persistent logs of detected text
3. **No Network**: No external API calls or data transmission
4. **Local Models**: OCR models stored locally

---

## Extensibility

### Extension Points

#### 1. Custom Blur Effects

```python
class VideoTextBlur:
    def blur_regions(self, frame, boxes, padding=10):
        # Current: Gaussian blur
        # Extension: Add pixelation, mosaic, etc.
        for box in boxes:
            roi = self.extract_roi(frame, box, padding)
            blurred_roi = self.apply_blur_effect(roi)  # ← Extension point
            frame = self.replace_roi(frame, blurred_roi, box)
        return frame
```

#### 2. Additional Detection Methods

```python
class VideoTextBlur:
    def detect_text_regions(self, frame):
        # Current: EasyOCR
        # Extension: Add Tesseract, custom models, etc.
        results = self.ocr_engine.detect(frame)  # ← Extension point
        return self.process_results(results)
```

#### 3. Custom Output Formats

```python
class VideoTextBlur:
    def finalize_output(self, temp_output, output_path):
        # Current: H.264 MP4
        # Extension: Add WebM, AV1, etc.
        self.encoder.convert(temp_output, output_path)  # ← Extension point
```

#### 4. Progress Callbacks

```python
class VideoTextBlur:
    def process_video(self, input_path, output_path, 
                     progress_callback=None):  # ← Extension point
        for frame_num in range(total_frames):
            # Process frame
            if progress_callback:
                progress_callback(frame_num, total_frames)
```

### Plugin Architecture (Future)

```python
# Proposed plugin system
class BlurPlugin:
    def apply(self, roi):
        raise NotImplementedError

class GaussianBlurPlugin(BlurPlugin):
    def apply(self, roi):
        return cv2.GaussianBlur(roi, (51, 51), 0)

class PixelatePlugin(BlurPlugin):
    def apply(self, roi):
        # Pixelation implementation
        pass

# Usage
processor = VideoTextBlur(blur_plugin=PixelatePlugin())
```

---

## Deployment Architecture

### Local Deployment

```
User Machine
├── Python 3.8+ Runtime
├── Virtual Environment
│   ├── opencv-python
│   ├── easyocr
│   ├── numpy
│   └── other dependencies
├── FFmpeg Binary
├── Application Code
│   ├── blur_text_video.py
│   ├── example_usage.py
│   └── shell scripts
└── OCR Models (downloaded on first run)
    └── ~/.EasyOCR/
```

### Docker Deployment (Future)

```
Docker Container
├── Base Image: python:3.10-slim
├── System Dependencies
│   ├── FFmpeg
│   └── CUDA (optional)
├── Python Dependencies
│   └── requirements.txt
├── Application Code
└── Entry Point: blur_text_video.py
```

### Cloud Deployment (Future)

```
Cloud Function / Lambda
├── Container Image
├── Input: Video URL
├── Processing: Blur text
├── Output: Processed video URL
└── Storage: Temporary S3/Cloud Storage
```

---

## System Requirements

### Minimum Requirements

- **CPU**: Dual-core 2.0 GHz
- **RAM**: 4 GB
- **Storage**: 500 MB (application + models)
- **OS**: macOS 10.15+, Ubuntu 20.04+, Windows 10+
- **Python**: 3.8+
- **FFmpeg**: Any recent version

### Recommended Requirements

- **CPU**: Quad-core 3.0 GHz or better
- **RAM**: 8 GB or more
- **Storage**: 2 GB (for temporary files)
- **GPU**: NVIDIA GPU with CUDA support (3-5x faster)
- **OS**: Latest stable version
- **Python**: 3.10+
- **FFmpeg**: Latest version

---

## Future Architecture Enhancements

### Planned Improvements

1. **Microservices Architecture**: Separate OCR, blur, and encoding services
2. **Async Processing**: Non-blocking frame processing with asyncio
3. **Distributed Processing**: Multi-machine video processing
4. **Real-Time Processing**: Live video stream support
5. **Web Interface**: Browser-based UI with REST API
6. **Database Integration**: Store processing history and settings
7. **Cloud Storage**: Direct integration with S3, GCS, Azure Blob
8. **Monitoring**: Prometheus metrics and Grafana dashboards

### Scalability Considerations

```
Current: Single-machine, sequential processing
Future: Distributed, parallel processing

┌──────────┐     ┌──────────┐     ┌──────────┐
│ Worker 1 │     │ Worker 2 │     │ Worker 3 │
│ Frames   │     │ Frames   │     │ Frames   │
│ 1-100    │     │ 101-200  │     │ 201-300  │
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │
     └────────────────┴────────────────┘
                      │
                      ▼
              ┌───────────────┐
              │ Merge Results │
              └───────────────┘
```

---

## Version Information

**Architecture Version**: 1.0.0  
**Last Updated**: February 22, 2026  
**Status**: Current

---

## See Also

- [API_REFERENCE.md](API_REFERENCE.md) - API documentation
- [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) - Technical details
- [README.md](README.md) - User guide

---

**End of Architecture Documentation**