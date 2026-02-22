# Installation Guide

Comprehensive installation instructions for the Video Text Blur Tool across different platforms and environments.

---

## Table of Contents

1. [Quick Installation](#quick-installation)
2. [System Requirements](#system-requirements)
3. [Platform-Specific Installation](#platform-specific-installation)
4. [Dependency Installation](#dependency-installation)
5. [Verification](#verification)
6. [Troubleshooting Installation](#troubleshooting-installation)
7. [Advanced Installation](#advanced-installation)
8. [Uninstallation](#uninstallation)

---

## Quick Installation

### For Most Users

```bash
# 1. Install FFmpeg (platform-specific, see below)

# 2. Clone or download the repository
git clone https://github.com/your-repo/video-text-blur.git
cd video-text-blur

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Test installation
python blur_text_video.py --help
```

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | macOS 10.15+, Ubuntu 20.04+, Windows 10+, Debian 11+ |
| **Python** | 3.8 or higher |
| **RAM** | 4 GB |
| **Storage** | 500 MB (application + models) |
| **CPU** | Dual-core 2.0 GHz |
| **Internet** | Required for initial setup only |

### Recommended Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Latest stable version |
| **Python** | 3.10 or higher |
| **RAM** | 8 GB or more |
| **Storage** | 2 GB (for temporary files) |
| **CPU** | Quad-core 3.0 GHz or better |
| **GPU** | NVIDIA GPU with CUDA support (3-5x faster) |

### Supported Platforms

- ✅ macOS (Intel and Apple Silicon)
- ✅ Linux (Ubuntu, Debian, CentOS, Fedora)
- ✅ Windows 10/11
- ✅ WSL2 (Windows Subsystem for Linux)

---

## Platform-Specific Installation

### macOS

#### Prerequisites

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3
brew install python@3.10

# Verify Python installation
python3 --version
```

#### Install FFmpeg

```bash
# Install FFmpeg via Homebrew
brew install ffmpeg

# Verify installation
ffmpeg -version
```

#### Install Video Text Blur Tool

```bash
# Clone repository
git clone https://github.com/your-repo/video-text-blur.git
cd video-text-blur

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# First run will download OCR models (~100MB)
python blur_text_video.py --help
```

#### Apple Silicon (M1/M2/M3) Notes

```bash
# For Apple Silicon Macs, ensure you're using ARM64 Python
python3 -c "import platform; print(platform.machine())"
# Should output: arm64

# If using x86_64 Python, install ARM64 version:
arch -arm64 brew install python@3.10
```

---

### Linux (Ubuntu/Debian)

#### Prerequisites

```bash
# Update package list
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

#### Install FFmpeg

```bash
# Install FFmpeg
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

#### Install System Dependencies

```bash
# Install required system libraries for OpenCV
sudo apt install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0

# For GPU support (optional)
# Install CUDA toolkit if you have NVIDIA GPU
# See: https://developer.nvidia.com/cuda-downloads
```

#### Install Video Text Blur Tool

```bash
# Clone repository
git clone https://github.com/your-repo/video-text-blur.git
cd video-text-blur

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Test installation
python blur_text_video.py --help
```

---

### Linux (CentOS/RHEL/Fedora)

#### Prerequisites

```bash
# CentOS/RHEL 8+
sudo dnf install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip python3-virtualenv

# Verify installation
python3 --version
```

#### Install FFmpeg

```bash
# Enable RPM Fusion repository
sudo dnf install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm

# Install FFmpeg
sudo dnf install ffmpeg

# Verify installation
ffmpeg -version
```

#### Install Video Text Blur Tool

```bash
# Follow same steps as Ubuntu/Debian
git clone https://github.com/your-repo/video-text-blur.git
cd video-text-blur
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Windows

#### Prerequisites

1. **Install Python**
   - Download from [python.org](https://www.python.org/downloads/)
   - Version 3.8 or higher
   - ✅ Check "Add Python to PATH" during installation
   - Verify: Open Command Prompt and run `python --version`

2. **Install Git** (optional, for cloning)
   - Download from [git-scm.com](https://git-scm.com/download/win)
   - Or download ZIP from GitHub

#### Install FFmpeg

**Option 1: Using Chocolatey (Recommended)**

```powershell
# Install Chocolatey (if not installed)
# Run PowerShell as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install FFmpeg
choco install ffmpeg

# Verify installation
ffmpeg -version
```

**Option 2: Manual Installation**

1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
2. Extract to `C:\ffmpeg`
3. Add to PATH:
   - Open System Properties → Environment Variables
   - Edit PATH variable
   - Add `C:\ffmpeg\bin`
4. Restart Command Prompt
5. Verify: `ffmpeg -version`

#### Install Video Text Blur Tool

```cmd
# Clone or download repository
git clone https://github.com/your-repo/video-text-blur.git
cd video-text-blur

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test installation
python blur_text_video.py --help
```

---

### Windows Subsystem for Linux (WSL2)

```bash
# Install WSL2 (if not already installed)
# In PowerShell as Administrator:
wsl --install

# Install Ubuntu from Microsoft Store

# In WSL2 Ubuntu terminal:
sudo apt update
sudo apt install python3 python3-pip python3-venv ffmpeg

# Follow Linux installation steps
git clone https://github.com/your-repo/video-text-blur.git
cd video-text-blur
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Dependency Installation

### Python Dependencies

The tool requires the following Python packages:

```txt
opencv-python>=4.8.0
opencv-contrib-python>=4.8.0
easyocr>=1.7.0
pytesseract>=0.3.10
ffmpeg-python>=0.2.0
numpy>=1.24.0
Pillow>=10.0.0
tqdm>=4.65.0
```

#### Install from requirements.txt

```bash
pip install -r requirements.txt
```

#### Install Individually

```bash
pip install opencv-python opencv-contrib-python
pip install easyocr
pip install numpy Pillow tqdm
pip install ffmpeg-python
```

### GPU Support (Optional)

For NVIDIA GPU acceleration:

#### Linux

```bash
# Install CUDA Toolkit
# Visit: https://developer.nvidia.com/cuda-downloads

# Install PyTorch with CUDA support
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Verify GPU is available
python -c "import torch; print(torch.cuda.is_available())"
```

#### Windows

```cmd
# Install CUDA Toolkit from NVIDIA website
# https://developer.nvidia.com/cuda-downloads

# Install PyTorch with CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Verify
python -c "import torch; print(torch.cuda.is_available())"
```

### OCR Models

Models are automatically downloaded on first run:

```bash
# First run downloads models (~100MB)
python blur_text_video.py --help

# Models are stored in:
# Linux/macOS: ~/.EasyOCR/
# Windows: C:\Users\YourName\.EasyOCR\
```

To pre-download models:

```python
import easyocr
reader = easyocr.Reader(['en'])  # Downloads English model
reader = easyocr.Reader(['en', 'fr'])  # Downloads English and French
```

---

## Verification

### Verify Installation

```bash
# 1. Check Python version
python3 --version  # Should be 3.8+

# 2. Check FFmpeg
ffmpeg -version

# 3. Check pip packages
pip list | grep opencv
pip list | grep easyocr

# 4. Test the tool
python blur_text_video.py --help

# 5. Check GPU availability (if applicable)
python -c "import torch; print('GPU available:', torch.cuda.is_available())"
```

### Test Run

```bash
# Create a test video (if you don't have one)
# Or download a sample video

# Run a quick test
python blur_text_video.py test_input.mp4 test_output.mp4 --sample-rate 10

# Check output file
ls -lh test_output.mp4
```

---

## Troubleshooting Installation

### Common Issues

#### 1. Python Not Found

**Error**: `python: command not found`

**Solution**:
```bash
# Try python3 instead
python3 --version

# Or create alias
alias python=python3
```

#### 2. pip Not Found

**Error**: `pip: command not found`

**Solution**:
```bash
# Install pip
# Ubuntu/Debian:
sudo apt install python3-pip

# macOS:
python3 -m ensurepip --upgrade

# Windows: Reinstall Python with pip option checked
```

#### 3. FFmpeg Not Found

**Error**: `ffmpeg: command not found`

**Solution**:
```bash
# Verify FFmpeg is installed
which ffmpeg  # Linux/macOS
where ffmpeg  # Windows

# If not found, install FFmpeg (see platform-specific sections)
```

#### 4. OpenCV Import Error

**Error**: `ImportError: libGL.so.1: cannot open shared object file`

**Solution** (Linux):
```bash
sudo apt install libgl1-mesa-glx
```

#### 5. EasyOCR Model Download Fails

**Error**: `Connection timeout` or `Download failed`

**Solution**:
```bash
# Check internet connection
# Try manual download
mkdir -p ~/.EasyOCR/model
cd ~/.EasyOCR/model
# Download models from: https://github.com/JaidedAI/EasyOCR/releases
```

#### 6. Permission Denied

**Error**: `Permission denied` when installing packages

**Solution**:
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or use --user flag
pip install --user -r requirements.txt
```

#### 7. CUDA Not Available

**Error**: GPU not detected

**Solution**:
```bash
# Check NVIDIA driver
nvidia-smi

# Reinstall PyTorch with CUDA
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

---

## Advanced Installation

### Docker Installation (Future)

```bash
# Build Docker image
docker build -t video-text-blur .

# Run container
docker run -v $(pwd):/workspace video-text-blur \
    python blur_text_video.py input.mp4 output.mp4
```

### Development Installation

```bash
# Clone repository
git clone https://github.com/your-repo/video-text-blur.git
cd video-text-blur

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in editable mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
pytest
```

### Offline Installation

```bash
# On machine with internet:
pip download -r requirements.txt -d packages/

# Transfer packages/ directory to offline machine

# On offline machine:
pip install --no-index --find-links=packages/ -r requirements.txt
```

---

## Uninstallation

### Remove Application

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf video-text-blur

# Remove OCR models (optional)
rm -rf ~/.EasyOCR/
```

### Remove System Dependencies

#### macOS

```bash
# Remove FFmpeg (optional)
brew uninstall ffmpeg

# Remove Python (optional, be careful)
brew uninstall python@3.10
```

#### Linux

```bash
# Remove FFmpeg (optional)
sudo apt remove ffmpeg

# Remove Python packages (optional)
sudo apt remove python3-pip
```

#### Windows

```cmd
# Uninstall FFmpeg via Chocolatey
choco uninstall ffmpeg

# Or manually delete C:\ffmpeg and remove from PATH

# Uninstall Python via Control Panel
```

---

## Post-Installation

### Configuration

Create a configuration file (optional):

```bash
# Create config file
cat > ~/.video-blur-config.json << EOF
{
  "default_blur": 51,
  "default_confidence": 0.5,
  "default_sample_rate": 3,
  "default_languages": ["en"]
}
EOF
```

### Shell Aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Alias for quick access
alias blur-video='python /path/to/video-text-blur/blur_text_video.py'

# Reload shell
source ~/.bashrc
```

### Update PATH

```bash
# Add to PATH for system-wide access
export PATH="$PATH:/path/to/video-text-blur"
```

---

## Getting Help

If you encounter issues:

1. Check [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Search [GitHub Issues](https://github.com/your-repo/issues)
3. Create a new issue with:
   - Operating system and version
   - Python version
   - Error messages
   - Steps to reproduce

---

## Next Steps

After installation:

1. Read [Quick Start Guide](QUICK_START.md)
2. Try [Example Usage](../example_usage.py)
3. Review [API Reference](API_REFERENCE.md)
4. Check [Performance Optimization](PERFORMANCE.md)

---

**Document Version**: 1.0.0  
**Last Updated**: February 22, 2026

---

**End of Installation Guide**