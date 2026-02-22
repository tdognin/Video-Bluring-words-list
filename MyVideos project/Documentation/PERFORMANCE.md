# Performance Optimization Guide

Comprehensive guide to optimizing performance of the Video Text Blur Tool.

---

## Table of Contents

1. [Performance Overview](#performance-overview)
2. [Quick Optimization Tips](#quick-optimization-tips)
3. [Hardware Optimization](#hardware-optimization)
4. [Software Optimization](#software-optimization)
5. [Configuration Tuning](#configuration-tuning)
6. [Benchmarking](#benchmarking)
7. [Advanced Optimization](#advanced-optimization)
8. [Performance Monitoring](#performance-monitoring)

---

## Performance Overview

### Performance Factors

Processing speed depends on:

1. **Video Properties**
   - Resolution (720p, 1080p, 4K)
   - Duration (length in seconds)
   - Frame rate (FPS)
   - Codec and compression

2. **Hardware**
   - CPU speed and cores
   - RAM capacity
   - GPU availability (CUDA)
   - Storage speed (HDD vs SSD)

3. **Configuration**
   - Sample rate (frames processed)
   - Confidence threshold
   - Blur strength
   - Number of languages

4. **Content**
   - Amount of text in video
   - Text complexity
   - Text frequency changes

### Typical Processing Times

**1080p Video (1 minute) on Mid-Range Hardware:**

| Configuration | CPU Time | GPU Time |
|--------------|----------|----------|
| Sample rate 1 (every frame) | 10-15 min | 3-5 min |
| Sample rate 3 | 4-6 min | 1-2 min |
| Sample rate 5 | 2-3 min | 40-60 sec |
| Sample rate 10 | 1-2 min | 20-30 sec |

---

## Quick Optimization Tips

### Fastest Processing (Acceptable Quality)

```bash
python3 blur_text_video.py input.mp4 output.mp4 \
    --sample-rate 10 \
    --confidence 0.6 \
    --blur 51
```

**Expected speedup**: 5-10x faster than default

### Balanced (Good Quality & Speed)

```bash
python3 blur_text_video.py input.mp4 output.mp4 \
    --sample-rate 5 \
    --confidence 0.5 \
    --blur 51
```

**Expected speedup**: 3-5x faster than default

### Best Quality (Slower)

```bash
python3 blur_text_video.py input.mp4 output.mp4 \
    --sample-rate 1 \
    --confidence 0.3 \
    --blur 71
```

**Expected speedup**: Baseline (no speedup)

---

## Hardware Optimization

### CPU Optimization

#### 1. Use Multi-Core Systems

```bash
# Check CPU cores
nproc  # Linux
sysctl -n hw.ncpu  # macOS

# The tool automatically uses available cores for video encoding
```

#### 2. Close Background Applications

```bash
# Linux: Check CPU usage
top
htop

# macOS: Check Activity Monitor
# Windows: Check Task Manager

# Close unnecessary applications before processing
```

#### 3. Increase Process Priority

```bash
# Linux/macOS: Run with higher priority
nice -n -10 python3 blur_text_video.py input.mp4 output.mp4

# Windows: Set priority in Task Manager
# Right-click process → Set Priority → High
```

### GPU Optimization

#### 1. Enable GPU Acceleration

```bash
# Check GPU availability
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# If False, install CUDA toolkit
# Visit: https://developer.nvidia.com/cuda-downloads
```

#### 2. Install CUDA-Enabled PyTorch

```bash
# Uninstall CPU-only version
pip uninstall torch torchvision

# Install CUDA version
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Verify
python3 -c "import torch; print(torch.cuda.is_available())"
```

#### 3. Monitor GPU Usage

```bash
# Check GPU utilization
nvidia-smi

# Watch in real-time
watch -n 1 nvidia-smi

# Expected: 70-100% GPU utilization during OCR
```

#### 4. GPU Memory Management

```bash
# Clear GPU cache before processing
python3 -c "import torch; torch.cuda.empty_cache()"

# Close other GPU applications
# (browsers, games, other ML applications)
```

### Memory Optimization

#### 1. Ensure Sufficient RAM

```bash
# Check available memory
free -h  # Linux
vm_stat  # macOS

# Recommended: 8GB+ for 1080p, 16GB+ for 4K
```

#### 2. Close Memory-Intensive Applications

```bash
# Before processing, close:
# - Web browsers with many tabs
# - IDEs
# - Other video editing software
# - Virtual machines
```

#### 3. Use Swap Space (if needed)

```bash
# Linux: Check swap
swapon --show

# Add swap if needed (8GB example)
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Storage Optimization

#### 1. Use SSD Instead of HDD

- **SSD**: 3-5x faster I/O
- **NVMe SSD**: 5-10x faster I/O
- **HDD**: Slowest option

#### 2. Ensure Sufficient Free Space

```bash
# Check disk space
df -h

# Recommended: 3x video file size free
# Example: 1GB video needs 3GB free space
```

#### 3. Use Fast Storage for Temporary Files

```bash
# Set temp directory to SSD
export TMPDIR=/path/to/ssd/tmp

# Or use RAM disk (Linux)
sudo mount -t tmpfs -o size=4G tmpfs /mnt/ramdisk
export TMPDIR=/mnt/ramdisk
```

---

## Software Optimization

### Python Optimization

#### 1. Use Latest Python Version

```bash
# Python 3.10+ has performance improvements
python3 --version

# Upgrade if needed
# macOS:
brew upgrade python@3.10

# Ubuntu:
sudo apt install python3.10
```

#### 2. Use Virtual Environment

```bash
# Virtual environments are faster than system Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Dependency Optimization

#### 1. Keep Dependencies Updated

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Check for updates
pip list --outdated
```

#### 2. Use Optimized Builds

```bash
# Install optimized NumPy (if available)
pip install numpy --upgrade

# Use Intel MKL for Intel CPUs (faster)
pip install mkl
```

### FFmpeg Optimization

#### 1. Use Latest FFmpeg

```bash
# Check version
ffmpeg -version

# Update
# macOS:
brew upgrade ffmpeg

# Ubuntu:
sudo apt update && sudo apt upgrade ffmpeg
```

#### 2. Hardware Encoding (if available)

```bash
# Check available encoders
ffmpeg -encoders | grep h264

# Use hardware encoder (NVIDIA)
# Modify output encoding in blur_text_video.py:
# -c:v h264_nvenc

# Use hardware encoder (Intel)
# -c:v h264_qsv

# Use hardware encoder (AMD)
# -c:v h264_amf
```

---

## Configuration Tuning

### Sample Rate Optimization

**Impact**: Most significant performance factor

```bash
# Sample rate comparison (1 minute 1080p video):
--sample-rate 1   # 10 min (every frame)
--sample-rate 3   # 4 min (every 3rd frame)
--sample-rate 5   # 2 min (every 5th frame)
--sample-rate 10  # 1 min (every 10th frame)
```

**Recommendations**:

| Video Type | Sample Rate | Reason |
|------------|-------------|--------|
| Static text (presentations) | 10-15 | Text doesn't change often |
| Slow-moving text | 5-7 | Moderate text changes |
| Fast-moving text | 2-3 | Frequent text changes |
| Dynamic content | 1 | Process every frame |

**Example**:

```bash
# For presentation video with static slides
python3 blur_text_video.py slides.mp4 output.mp4 --sample-rate 15

# For screen recording with typing
python3 blur_text_video.py recording.mp4 output.mp4 --sample-rate 3
```

### Confidence Threshold Optimization

**Impact**: Moderate performance factor

```bash
# Higher confidence = fewer detections = faster
--confidence 0.3  # Detect more (slower)
--confidence 0.5  # Balanced (default)
--confidence 0.7  # Detect less (faster)
```

**Recommendations**:

```bash
# For clear, high-quality text
python3 blur_text_video.py input.mp4 output.mp4 --confidence 0.7

# For blurry or small text
python3 blur_text_video.py input.mp4 output.mp4 --confidence 0.3
```

### Language Optimization

**Impact**: Moderate performance factor

```bash
# Fewer languages = faster processing
--languages en           # Fastest
--languages en fr        # Moderate
--languages en fr es de  # Slower
```

**Recommendations**:

```bash
# Only use languages present in video
python3 blur_text_video.py input.mp4 output.mp4 --languages en

# Avoid unnecessary languages
```

### Blur Strength Optimization

**Impact**: Minor performance factor

```bash
# Lower blur = slightly faster
--blur 31   # Light blur (faster)
--blur 51   # Medium blur (default)
--blur 101  # Heavy blur (slower)
```

**Note**: Impact is minimal compared to other factors

---

## Benchmarking

### Benchmark Your System

```bash
# Create test script
cat > benchmark.sh << 'EOF'
#!/bin/bash

echo "=== Video Text Blur Performance Benchmark ==="
echo ""

# Test video (create 30-second sample)
ffmpeg -i your_video.mp4 -t 30 test_30sec.mp4 -y

echo "Test 1: Sample rate 1 (baseline)"
time python3 blur_text_video.py test_30sec.mp4 out1.mp4 --sample-rate 1

echo ""
echo "Test 2: Sample rate 5"
time python3 blur_text_video.py test_30sec.mp4 out2.mp4 --sample-rate 5

echo ""
echo "Test 3: Sample rate 10"
time python3 blur_text_video.py test_30sec.mp4 out3.mp4 --sample-rate 10

echo ""
echo "Test 4: High confidence"
time python3 blur_text_video.py test_30sec.mp4 out4.mp4 --confidence 0.7

# Cleanup
rm test_30sec.mp4 out*.mp4

echo ""
echo "=== Benchmark Complete ==="
EOF

chmod +x benchmark.sh
./benchmark.sh
```

### Compare Configurations

```bash
# Test different configurations
for rate in 1 3 5 10; do
    echo "Testing sample-rate $rate"
    time python3 blur_text_video.py test.mp4 out_$rate.mp4 --sample-rate $rate
done
```

### Measure Processing Speed

```python
# Add timing to your script
import time

start_time = time.time()
processor.process_video('input.mp4', 'output.mp4')
end_time = time.time()

duration = end_time - start_time
print(f"Processing time: {duration:.2f} seconds")
print(f"Processing time: {duration/60:.2f} minutes")
```

---

## Advanced Optimization

### Pre-Processing Video

#### 1. Reduce Resolution

```bash
# Convert 4K to 1080p (4x faster processing)
ffmpeg -i input_4k.mp4 -vf scale=1920:1080 input_1080p.mp4
python3 blur_text_video.py input_1080p.mp4 output.mp4

# Convert 1080p to 720p (2x faster processing)
ffmpeg -i input_1080p.mp4 -vf scale=1280:720 input_720p.mp4
python3 blur_text_video.py input_720p.mp4 output.mp4
```

#### 2. Reduce Frame Rate

```bash
# Convert 60fps to 30fps (2x faster processing)
ffmpeg -i input_60fps.mp4 -r 30 input_30fps.mp4
python3 blur_text_video.py input_30fps.mp4 output.mp4
```

#### 3. Extract Segment

```bash
# Process only relevant portion
ffmpeg -i input.mp4 -ss 00:01:00 -t 00:02:00 segment.mp4
python3 blur_text_video.py segment.mp4 output.mp4
```

### Batch Processing Optimization

```python
# Process multiple videos efficiently
from blur_text_video import VideoTextBlur

# Initialize once (reuse OCR reader)
processor = VideoTextBlur(
    languages=['en'],
    blur_strength=51,
    confidence_threshold=0.5
)

# Process multiple videos
videos = ['video1.mp4', 'video2.mp4', 'video3.mp4']
for video in videos:
    output = f"blurred_{video}"
    processor.process_video(video, output, sample_rate=5)
```

### Parallel Processing

```bash
# Process multiple videos in parallel (use with caution)
# Ensure sufficient RAM and CPU cores

# Process 2 videos simultaneously
python3 blur_text_video.py video1.mp4 out1.mp4 --sample-rate 5 &
python3 blur_text_video.py video2.mp4 out2.mp4 --sample-rate 5 &
wait

# Or use GNU parallel
parallel python3 blur_text_video.py {} blurred_{} --sample-rate 5 ::: *.mp4
```

### Code-Level Optimization

```python
# Optimize imports (in blur_text_video.py)
# Import only what's needed
from cv2 import VideoCapture, VideoWriter, GaussianBlur
# Instead of: import cv2

# Use numpy operations efficiently
import numpy as np
# Vectorized operations are faster than loops

# Cache OCR results
# Store detected boxes and reuse for similar frames
```

---

## Performance Monitoring

### Monitor During Processing

```bash
# Terminal 1: Run processing
python3 blur_text_video.py input.mp4 output.mp4

# Terminal 2: Monitor resources
# CPU and Memory
top
# or
htop

# GPU (if available)
watch -n 1 nvidia-smi

# Disk I/O
iostat -x 1
```

### Profile Performance

```python
# Add profiling to script
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Process video
processor = VideoTextBlur(languages=['en'])
processor.process_video('input.mp4', 'output.mp4')

profiler.disable()

# Print stats
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions

# Save to file
stats.dump_stats('profile_results.prof')
```

### Analyze Bottlenecks

```python
# Identify slow functions
import time

def timed_function(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__}: {end-start:.2f}s")
        return result
    return wrapper

# Apply to methods
@timed_function
def detect_text_regions(self, frame):
    # ... existing code ...
```

---

## Performance Checklist

### Before Processing

- [ ] Close unnecessary applications
- [ ] Ensure sufficient disk space (3x video size)
- [ ] Check GPU is available (if applicable)
- [ ] Use SSD for storage
- [ ] Update dependencies
- [ ] Test with short video first

### Configuration

- [ ] Use appropriate sample rate (5-10 for most videos)
- [ ] Set confidence threshold (0.5-0.7 for clear text)
- [ ] Use only necessary languages
- [ ] Consider pre-processing (resolution, frame rate)

### During Processing

- [ ] Monitor resource usage
- [ ] Watch for errors or warnings
- [ ] Check progress bar movement
- [ ] Ensure system doesn't overheat

### After Processing

- [ ] Verify output quality
- [ ] Check processing time
- [ ] Compare with expectations
- [ ] Adjust settings if needed

---

## Performance Comparison

### Resolution Impact

| Resolution | Relative Speed | Quality |
|------------|---------------|---------|
| 480p | 4x faster | Low |
| 720p | 2x faster | Good |
| 1080p | Baseline | High |
| 4K | 4x slower | Very High |

### Sample Rate Impact

| Sample Rate | Speed | Quality | Use Case |
|-------------|-------|---------|----------|
| 1 | Baseline | Best | Dynamic content |
| 3 | 3x faster | Excellent | General use |
| 5 | 5x faster | Good | Static text |
| 10 | 10x faster | Acceptable | Presentations |
| 15 | 15x faster | Fair | Rare text changes |

### Hardware Impact

| Hardware | Relative Speed |
|----------|---------------|
| CPU only (dual-core) | Baseline |
| CPU only (quad-core) | 1.5x faster |
| CPU only (8-core) | 2x faster |
| GPU (CUDA) | 3-5x faster |
| GPU (CUDA) + SSD | 5-8x faster |

---

## Optimization Examples

### Example 1: Fast Processing for Long Video

```bash
# 2-hour presentation video
python3 blur_text_video.py presentation.mp4 output.mp4 \
    --sample-rate 15 \
    --confidence 0.6 \
    --languages en

# Expected: 10-15 minutes processing time
```

### Example 2: High Quality for Short Video

```bash
# 30-second promotional video
python3 blur_text_video.py promo.mp4 output.mp4 \
    --sample-rate 1 \
    --confidence 0.3 \
    --blur 71 \
    --padding 20

# Expected: 2-3 minutes processing time
```

### Example 3: Balanced for General Use

```bash
# 5-minute tutorial video
python3 blur_text_video.py tutorial.mp4 output.mp4 \
    --sample-rate 5 \
    --confidence 0.5 \
    --blur 51

# Expected: 3-5 minutes processing time
```

---

## Troubleshooting Performance

### Issue: Processing Too Slow

**Solutions**:
1. Increase sample rate
2. Enable GPU acceleration
3. Reduce video resolution
4. Increase confidence threshold
5. Use fewer languages
6. Close background applications

### Issue: Poor Quality Despite Fast Processing

**Solutions**:
1. Decrease sample rate
2. Lower confidence threshold
3. Increase blur strength
4. Add more padding
5. Process at higher resolution

### Issue: System Becomes Unresponsive

**Solutions**:
1. Reduce sample rate (paradoxically)
2. Close other applications
3. Add more RAM
4. Use lower resolution video
5. Process in smaller segments

---

## Future Optimizations

Planned performance improvements:

1. **Multi-threading**: Parallel frame processing
2. **Batch OCR**: Process multiple frames at once
3. **Smart caching**: Reuse detection results
4. **Hardware encoding**: Use GPU for video encoding
5. **Optimized algorithms**: Faster blur implementations

---

**Document Version**: 1.0.0  
**Last Updated**: February 22, 2026

---

**End of Performance Optimization Guide**