# Troubleshooting Guide

Comprehensive troubleshooting guide for the Video Text Blur Tool.

---

## Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Installation Issues](#installation-issues)
3. [Runtime Errors](#runtime-errors)
4. [Performance Issues](#performance-issues)
5. [Output Quality Issues](#output-quality-issues)
6. [Platform-Specific Issues](#platform-specific-issues)
7. [Advanced Troubleshooting](#advanced-troubleshooting)
8. [Getting Help](#getting-help)

---

## Quick Diagnostics

### Run System Check

```bash
# Check Python version
python3 --version

# Check FFmpeg
ffmpeg -version

# Check installed packages
pip list | grep -E "opencv|easyocr|numpy"

# Check GPU availability
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# Test basic functionality
python3 blur_text_video.py --help
```

### Common Quick Fixes

```bash
# 1. Update all dependencies
pip install --upgrade -r requirements.txt

# 2. Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 3. Reinstall in clean environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Clear OCR model cache
rm -rf ~/.EasyOCR/
```

---

## Installation Issues

### Issue: Python Not Found

**Symptoms**:
```
python: command not found
```

**Solutions**:

```bash
# Try python3
python3 --version

# Install Python (Ubuntu/Debian)
sudo apt install python3 python3-pip

# Install Python (macOS)
brew install python@3.10

# Windows: Download from python.org
```

### Issue: pip Not Found

**Symptoms**:
```
pip: command not found
```

**Solutions**:

```bash
# Use python3 -m pip
python3 -m pip --version

# Install pip (Ubuntu/Debian)
sudo apt install python3-pip

# Install pip (macOS)
python3 -m ensurepip --upgrade

# Windows: Reinstall Python with pip option
```

### Issue: FFmpeg Not Found

**Symptoms**:
```
ffmpeg: command not found
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**Solutions**:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# CentOS/RHEL
sudo dnf install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg

# Verify installation
ffmpeg -version
which ffmpeg  # Should show path
```

### Issue: OpenCV Import Error

**Symptoms**:
```
ImportError: libGL.so.1: cannot open shared object file
ImportError: libgthread-2.0.so.0: cannot open shared object file
```

**Solutions**:

```bash
# Ubuntu/Debian
sudo apt install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    libgl1-mesa-glx

# CentOS/RHEL
sudo yum install mesa-libGL

# Verify
python3 -c "import cv2; print(cv2.__version__)"
```

### Issue: EasyOCR Model Download Fails

**Symptoms**:
```
Connection timeout
Download failed
Unable to download model
```

**Solutions**:

```bash
# 1. Check internet connection
ping google.com

# 2. Try manual download
mkdir -p ~/.EasyOCR/model
cd ~/.EasyOCR/model

# Download from GitHub releases
# https://github.com/JaidedAI/EasyOCR/releases

# 3. Use proxy if needed
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port

# 4. Retry with increased timeout
python3 -c "import easyocr; reader = easyocr.Reader(['en'], download_enabled=True)"
```

### Issue: Permission Denied

**Symptoms**:
```
PermissionError: [Errno 13] Permission denied
```

**Solutions**:

```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or use --user flag
pip install --user -r requirements.txt

# Fix file permissions
chmod +x blur_text_video.py
chmod +x run_blur.sh
```

---

## Runtime Errors

### Issue: "Could not open video"

**Symptoms**:
```
ValueError: Could not open video: input.mp4
```

**Causes & Solutions**:

1. **File doesn't exist**
   ```bash
   # Check file exists
   ls -l input.mp4
   
   # Use absolute path
   python3 blur_text_video.py /full/path/to/input.mp4 output.mp4
   ```

2. **Corrupted video file**
   ```bash
   # Test with FFmpeg
   ffmpeg -v error -i input.mp4 -f null -
   
   # Try to repair
   ffmpeg -i input.mp4 -c copy repaired.mp4
   ```

3. **Unsupported format**
   ```bash
   # Convert to MP4
   ffmpeg -i input.mov -c:v libx264 -c:a aac input.mp4
   ```

4. **FFmpeg not in PATH**
   ```bash
   # Check FFmpeg
   which ffmpeg
   
   # Add to PATH (Linux/macOS)
   export PATH=$PATH:/path/to/ffmpeg/bin
   ```

### Issue: Out of Memory

**Symptoms**:
```
MemoryError
Killed
Process terminated
```

**Solutions**:

```bash
# 1. Increase sample rate (process fewer frames)
python3 blur_text_video.py input.mp4 output.mp4 --sample-rate 10

# 2. Reduce video resolution first
ffmpeg -i input.mp4 -vf scale=1280:720 input_720p.mp4
python3 blur_text_video.py input_720p.mp4 output.mp4

# 3. Close other applications

# 4. Check available memory
free -h  # Linux
vm_stat  # macOS

# 5. Use CPU instead of GPU
# Edit blur_text_video.py line 29: gpu=False
```

### Issue: CUDA Out of Memory

**Symptoms**:
```
RuntimeError: CUDA out of memory
```

**Solutions**:

```bash
# 1. Use CPU instead
# Edit blur_text_video.py line 29: gpu=False

# 2. Reduce batch size (if applicable)

# 3. Clear GPU memory
python3 -c "import torch; torch.cuda.empty_cache()"

# 4. Check GPU memory
nvidia-smi

# 5. Close other GPU applications
```

### Issue: "Empty ROI" or Blur Crash

**Symptoms**:
```
cv2.error: OpenCV(4.x.x) error: (-215:Assertion failed)
Empty region of interest
```

**Causes & Solutions**:

1. **Text at frame edges**
   ```bash
   # Increase padding to avoid edge cases
   python3 blur_text_video.py input.mp4 output.mp4 --padding 20
   ```

2. **Invalid bounding boxes**
   ```bash
   # Lower confidence threshold
   python3 blur_text_video.py input.mp4 output.mp4 --confidence 0.3
   ```

### Issue: Process Hangs or Freezes

**Symptoms**:
- No progress for extended time
- CPU/GPU at 100%
- No error messages

**Solutions**:

```bash
# 1. Check if actually processing (may be slow)
# Look for progress bar updates

# 2. Interrupt and restart with higher sample rate
# Press Ctrl+C
python3 blur_text_video.py input.mp4 output.mp4 --sample-rate 10

# 3. Check system resources
top  # or htop

# 4. Test with shorter video
ffmpeg -i input.mp4 -t 10 test_10sec.mp4
python3 blur_text_video.py test_10sec.mp4 output.mp4
```

---

## Performance Issues

### Issue: Very Slow Processing

**Symptoms**:
- Takes hours for short videos
- Progress bar barely moves

**Solutions**:

```bash
# 1. Increase sample rate
python3 blur_text_video.py input.mp4 output.mp4 --sample-rate 5

# 2. Use GPU if available
# Check: python3 -c "import torch; print(torch.cuda.is_available())"

# 3. Reduce video resolution
ffmpeg -i input.mp4 -vf scale=1280:720 input_720p.mp4

# 4. Increase confidence threshold (fewer detections)
python3 blur_text_video.py input.mp4 output.mp4 --confidence 0.7

# 5. Use fewer languages
python3 blur_text_video.py input.mp4 output.mp4 --languages en
```

### Issue: GPU Not Being Used

**Symptoms**:
- GPU usage at 0%
- Processing slow despite having GPU

**Solutions**:

```bash
# 1. Check CUDA availability
python3 -c "import torch; print('CUDA:', torch.cuda.is_available())"

# 2. Install CUDA toolkit
# Visit: https://developer.nvidia.com/cuda-downloads

# 3. Reinstall PyTorch with CUDA
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 4. Check NVIDIA driver
nvidia-smi

# 5. Verify GPU parameter in code
# blur_text_video.py line 29 should have: gpu=True
```

### Issue: High CPU Usage

**Symptoms**:
- CPU at 100%
- System becomes unresponsive

**Solutions**:

```bash
# 1. Increase sample rate
python3 blur_text_video.py input.mp4 output.mp4 --sample-rate 10

# 2. Lower process priority
nice -n 19 python3 blur_text_video.py input.mp4 output.mp4

# 3. Limit CPU cores (Linux)
taskset -c 0-3 python3 blur_text_video.py input.mp4 output.mp4

# 4. Process during off-hours
```

---

## Output Quality Issues

### Issue: Text Not Detected

**Symptoms**:
- No blur applied
- Text clearly visible in output

**Solutions**:

```bash
# 1. Lower confidence threshold
python3 blur_text_video.py input.mp4 output.mp4 --confidence 0.3

# 2. Process every frame
python3 blur_text_video.py input.mp4 output.mp4 --sample-rate 1

# 3. Add appropriate language
python3 blur_text_video.py input.mp4 output.mp4 --languages en fr es

# 4. Check if text is clear in video
# Blurry or small text may not be detected

# 5. Test with specific words
python3 blur_text_video.py input.mp4 output.mp4 --words "password"
```

### Issue: Too Much Blurred

**Symptoms**:
- Non-text areas blurred
- False positives

**Solutions**:

```bash
# 1. Increase confidence threshold
python3 blur_text_video.py input.mp4 output.mp4 --confidence 0.7

# 2. Use specific words only
python3 blur_text_video.py input.mp4 output.mp4 --words "password" "email"

# 3. Reduce padding
python3 blur_text_video.py input.mp4 output.mp4 --padding 5
```

### Issue: Blur Not Strong Enough

**Symptoms**:
- Text still partially readable
- Blur too weak

**Solutions**:

```bash
# Increase blur strength (must be odd number)
python3 blur_text_video.py input.mp4 output.mp4 --blur 71
python3 blur_text_video.py input.mp4 output.mp4 --blur 101

# Increase padding for larger blur area
python3 blur_text_video.py input.mp4 output.mp4 --blur 71 --padding 20
```

### Issue: Flickering Blur

**Symptoms**:
- Blur appears and disappears
- Inconsistent blurring

**Solutions**:

```bash
# 1. Reduce sample rate (process more frames)
python3 blur_text_video.py input.mp4 output.mp4 --sample-rate 1

# 2. Lower confidence threshold
python3 blur_text_video.py input.mp4 output.mp4 --confidence 0.4

# 3. Increase padding
python3 blur_text_video.py input.mp4 output.mp4 --padding 20
```

### Issue: QuickTime Won't Play Output

**Symptoms**:
```
QuickTime Player can't open the file
File format not supported
```

**Solutions**:

```bash
# 1. Ensure FFmpeg conversion completed
# Check for success message in output

# 2. Manual conversion
ffmpeg -i output.mp4 -c:v libx264 -pix_fmt yuv420p -movflags +faststart output_qt.mp4

# 3. Check FFmpeg version
ffmpeg -version  # Should be recent version

# 4. Try different player
vlc output.mp4
```

---

## Platform-Specific Issues

### macOS Issues

#### Issue: "Developer Cannot Be Verified"

**Solution**:
```bash
# Allow app in System Preferences > Security & Privacy
# Or use:
xattr -d com.apple.quarantine blur_text_video.py
```

#### Issue: Apple Silicon (M1/M2) Compatibility

**Solution**:
```bash
# Ensure using ARM64 Python
python3 -c "import platform; print(platform.machine())"
# Should output: arm64

# Install ARM64 Python
arch -arm64 brew install python@3.10

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Linux Issues

#### Issue: "libGL.so.1 not found"

**Solution**:
```bash
sudo apt install libgl1-mesa-glx
```

#### Issue: Permission Denied on Scripts

**Solution**:
```bash
chmod +x blur_text_video.py
chmod +x run_blur.sh
chmod +x run_blur_interactive.sh
```

### Windows Issues

#### Issue: "python is not recognized"

**Solution**:
```cmd
# Add Python to PATH
# System Properties > Environment Variables > PATH
# Add: C:\Python310\
# Add: C:\Python310\Scripts\

# Or use py launcher
py -3 blur_text_video.py input.mp4 output.mp4
```

#### Issue: FFmpeg Not Found

**Solution**:
```cmd
# Check PATH
echo %PATH%

# Add FFmpeg to PATH
# System Properties > Environment Variables > PATH
# Add: C:\ffmpeg\bin

# Restart Command Prompt
```

#### Issue: Long Path Names

**Solution**:
```cmd
# Enable long paths in Windows
# Run as Administrator:
reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1

# Or use shorter paths
cd C:\
mkdir work
cd work
```

---

## Advanced Troubleshooting

### Enable Debug Mode

```python
# Add to blur_text_video.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Verbose Output

```bash
# Run with Python verbose mode
python3 -v blur_text_video.py input.mp4 output.mp4

# Check FFmpeg output
ffmpeg -v verbose -i input.mp4 output.mp4
```

### Test Individual Components

```python
# Test OpenCV
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"

# Test EasyOCR
python3 -c "import easyocr; print('EasyOCR imported successfully')"

# Test video reading
python3 << EOF
import cv2
cap = cv2.VideoCapture('input.mp4')
print('Video opened:', cap.isOpened())
print('FPS:', cap.get(cv2.CAP_PROP_FPS))
print('Frames:', cap.get(cv2.CAP_PROP_FRAME_COUNT))
cap.release()
EOF
```

### Check System Resources

```bash
# Linux
free -h  # Memory
df -h    # Disk space
top      # CPU usage

# macOS
vm_stat  # Memory
df -h    # Disk space
top      # CPU usage

# Windows
# Task Manager (Ctrl+Shift+Esc)
```

### Profile Performance

```python
# Add to script
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here
processor.process_video('input.mp4', 'output.mp4')

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

---

## Getting Help

### Before Asking for Help

1. **Check existing documentation**
   - Documentation/README.md
   - This troubleshooting guide
   - GitHub issues

2. **Gather information**
   ```bash
   # System info
   uname -a  # Linux/macOS
   systeminfo  # Windows
   
   # Python info
   python3 --version
   pip list
   
   # FFmpeg info
   ffmpeg -version
   
   # Error messages
   # Copy full error output
   ```

3. **Create minimal reproduction**
   - Use shortest video that shows the issue
   - Use simplest command that fails
   - Remove unnecessary options

### Where to Get Help

1. **GitHub Issues**
   - Search existing issues first
   - Create new issue with template
   - Include system information and error messages

2. **GitHub Discussions**
   - For questions and general discussion
   - Share experiences and solutions

3. **Stack Overflow**
   - Tag: `video-text-blur`
   - Include minimal reproducible example

### Issue Template

```markdown
**System Information**
- OS: [e.g., macOS 12.0, Ubuntu 22.04]
- Python version: [e.g., 3.10.0]
- FFmpeg version: [e.g., 4.4.0]
- GPU: [Yes/No, model if yes]

**Command Used**
```bash
python3 blur_text_video.py input.mp4 output.mp4 --blur 51
```

**Expected Behavior**
Video should be processed with text blurred

**Actual Behavior**
Error message appears: [paste error]

**Error Messages**
```
[Paste full error output]
```

**Additional Context**
- Video format: MP4
- Video duration: 30 seconds
- Video resolution: 1920x1080
- First time running: Yes/No
```

---

## Common Error Messages

### Error: "No module named 'cv2'"

**Solution**:
```bash
pip install opencv-python opencv-contrib-python
```

### Error: "No module named 'easyocr'"

**Solution**:
```bash
pip install easyocr
```

### Error: "CUDA error: out of memory"

**Solution**:
```bash
# Use CPU instead
# Edit blur_text_video.py line 29: gpu=False
```

### Error: "ffmpeg: command not found"

**Solution**:
```bash
# Install FFmpeg (see Installation section)
```

### Error: "Permission denied"

**Solution**:
```bash
chmod +x blur_text_video.py
# Or use: python3 blur_text_video.py
```

---

## Preventive Measures

### Best Practices

1. **Always use virtual environments**
2. **Keep dependencies updated**
3. **Test with short videos first**
4. **Backup original videos**
5. **Monitor system resources**
6. **Use appropriate sample rates**
7. **Start with default settings**

### Regular Maintenance

```bash
# Update dependencies monthly
pip list --outdated
pip install --upgrade -r requirements.txt

# Clear cache periodically
find . -type d -name __pycache__ -exec rm -rf {} +
rm -rf ~/.EasyOCR/  # Redownload models if needed

# Check for updates
git pull origin main
```

---

## Still Having Issues?

If you've tried everything and still have problems:

1. **Create a detailed bug report** on GitHub
2. **Include all diagnostic information**
3. **Provide sample video** (if possible)
4. **Be patient** - maintainers will respond

---

**Document Version**: 1.0.0  
**Last Updated**: February 22, 2026

---

**End of Troubleshooting Guide**