# API Reference

Complete API documentation for the Video Text Blur Tool.

---

## Table of Contents

1. [VideoTextBlur Class](#videotextblur-class)
2. [Methods](#methods)
3. [Command-Line Interface](#command-line-interface)
4. [Python API Examples](#python-api-examples)
5. [Return Values and Exceptions](#return-values-and-exceptions)

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

## Version Information

**API Version**: 1.0.0  
**Last Updated**: February 22, 2026  
**Compatibility**: Python 3.8+

---

## See Also

- [README.md](README.md) - Quick start guide
- [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) - Comprehensive technical reference
- [UPDATED_FEATURES.md](UPDATED_FEATURES.md) - Feature documentation
- [example_usage.py](../example_usage.py) - Code examples

---

**End of API Reference**