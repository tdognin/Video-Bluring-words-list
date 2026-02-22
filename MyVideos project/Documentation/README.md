# Video Text Blur Tool

Automatically detect and blur text in MP4 and MOV videos using OCR (Optical Character Recognition) and OpenCV.

## Features

- 🔍 **Automatic text detection** using EasyOCR
- 🎭 **Gaussian blur** applied to detected text regions
- 🎬 **Supports MP4 and MOV** video formats
- 🌍 **Multi-language support** (English, French, Spanish, etc.)
- ⚡ **Configurable sampling rate** for performance optimization
- 🎨 **Adjustable blur strength** and padding

## Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for video processing)

#### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note:** First run will download OCR models (~100MB), which may take a few minutes.

## Usage

### Basic Usage

```bash
python blur_text_video.py input.mp4 output.mp4
```

### Advanced Options

```bash
# Blur with custom strength (higher = more blur)
python blur_text_video.py input.mp4 output.mp4 --blur 71

# Process every 5th frame for better performance
python blur_text_video.py input.mp4 output.mp4 --sample-rate 5

# Multiple languages (English and French)
python blur_text_video.py input.mp4 output.mp4 --languages en fr

# Adjust confidence threshold (0-1)
python blur_text_video.py input.mp4 output.mp4 --confidence 0.7

# Add more padding around text
python blur_text_video.py input.mp4 output.mp4 --padding 20
```

### All Options

```
positional arguments:
  input                 Input video file (MP4/MOV)
  output                Output video file

optional arguments:
  -h, --help            Show help message
  --languages [LANG ...]
                        OCR languages (default: en)
                        Available: en, fr, es, de, it, pt, ru, ja, ko, zh, etc.
  --blur BLUR           Blur strength - must be odd number (default: 51)
                        Higher values = stronger blur
  --confidence CONF     Text detection confidence threshold 0-1 (default: 0.5)
                        Lower = detect more text (may include false positives)
  --sample-rate N       Process every Nth frame for detection (default: 1)
                        Higher = faster but may miss text changes
  --padding PIXELS      Padding around text regions in pixels (default: 10)
```

## Performance Tips

1. **Use sample-rate for long videos**: Processing every frame is slow. Use `--sample-rate 5` or `--sample-rate 10` for videos where text doesn't change frequently.

2. **Adjust confidence threshold**: If text isn't being detected, lower `--confidence` to 0.3. If too much is being blurred, raise it to 0.7.

3. **GPU acceleration**: EasyOCR will automatically use GPU if available (CUDA for NVIDIA GPUs).

## Examples

### Example 1: Basic blur
```bash
python blur_text_video.py my_video.mp4 blurred_video.mp4
```

### Example 2: Fast processing for long video
```bash
python blur_text_video.py long_video.mp4 output.mp4 --sample-rate 10 --blur 71
```

### Example 3: Multi-language video
```bash
python blur_text_video.py multilingual.mp4 output.mp4 --languages en fr es
```

### Example 4: Sensitive text with extra blur
```bash
python blur_text_video.py sensitive.mp4 output.mp4 --blur 101 --padding 20
```

## How It Works

1. **Text Detection**: Uses EasyOCR to detect text in video frames
2. **Bounding Boxes**: Identifies rectangular regions containing text
3. **Blur Application**: Applies Gaussian blur to detected regions
4. **Frame Processing**: Processes each frame and writes to output video

## Supported Languages

EasyOCR supports 80+ languages including:
- English (en)
- French (fr)
- Spanish (es)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese Simplified (ch_sim)
- Chinese Traditional (ch_tra)
- Arabic (ar)
- And many more...

## Troubleshooting

### "Could not open video"
- Ensure FFmpeg is installed
- Check video file is not corrupted
- Try converting video format: `ffmpeg -i input.mov output.mp4`

### Slow processing
- Increase `--sample-rate` (e.g., 5 or 10)
- Reduce video resolution before processing
- Ensure GPU drivers are installed for CUDA acceleration

### Text not detected
- Lower `--confidence` threshold (e.g., 0.3)
- Add appropriate language with `--languages`
- Check if text is clear and readable in the video

### Too much blurred
- Increase `--confidence` threshold (e.g., 0.7)
- Reduce `--padding` value

## License

MIT License - Feel free to use and modify as needed.

## Requirements

See `requirements.txt` for full list of dependencies.