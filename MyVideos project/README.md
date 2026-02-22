# Video Text Blur Tool

Automatically detect and blur text in MP4 and MOV videos using OCR (Optical Character Recognition) and OpenCV.

## 📚 Documentation

All documentation has been moved to the **[Documentation](./Documentation/)** folder.

### Quick Links

- **[Main Documentation](./Documentation/README.md)** - Complete project documentation
- **[Quick Start Guide](./Documentation/QUICK_START.md)** - Get started quickly
- **[Installation Guide](./Documentation/INSTALLATION.md)** - Setup instructions
- **[API Reference](./Documentation/API_REFERENCE.md)** - API documentation
- **[Troubleshooting](./Documentation/TROUBLESHOOTING.md)** - Common issues and solutions

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Basic usage
python blur_text_video.py input.mp4 output.mp4

# With options
python blur_text_video.py input.mp4 output.mp4 --blur 71 --sample-rate 5
```

For detailed usage instructions, see the [Documentation](./Documentation/) folder.

## Features

- 🔍 Automatic text detection using EasyOCR
- 🎭 Gaussian blur applied to detected text regions
- 🎬 Supports MP4 and MOV video formats
- 🌍 Multi-language support
- ⚡ Configurable sampling rate for performance
- 🎨 Adjustable blur strength and padding

## License

MIT License - See [LICENSE](./LICENSE) file for details.