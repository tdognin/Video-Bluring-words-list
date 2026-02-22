# Updated Features - Video Text Blur Tool

## 🎯 New Features

### 1. Selective Word Blurring
You can now blur **only specific words** instead of all text!

#### Three Modes:

**A) Interactive Mode** (Recommended)
```bash
python3 blur_text_video.py input.mp4 output.mp4
# You'll be prompted to enter words to blur
```

**B) Command Line Mode**
```bash
# Blur specific words
python3 blur_text_video.py input.mp4 output.mp4 --words "password" "email" "secret"

# Blur phrases with spaces (use quotes)
python3 blur_text_video.py input.mp4 output.mp4 --words "John Doe" "confidential data"
```

**C) Blur All Text Mode**
```bash
python3 blur_text_video.py input.mp4 output.mp4 --blur-all
```

### 2. QuickTime Compatibility
Videos are now automatically converted to QuickTime-compatible H.264 format:
- ✅ Works with QuickTime Player on macOS
- ✅ Compatible with iOS devices
- ✅ Standard MP4 format with H.264 codec
- ✅ Optimized with `faststart` flag for web streaming

## 📝 Usage Examples

### Example 1: Blur specific words interactively
```bash
./run_blur_interactive.sh
# Then enter: password, email, secret
```

### Example 2: Blur specific words from command line
```bash
python3 blur_text_video.py "2 - wx gov - creation Usecase.mp4" output.mp4 \
  --words "Usecase" "creation" "gov" \
  --blur 51 \
  --sample-rate 3
```

### Example 3: Blur all text (old behavior)
```bash
python3 blur_text_video.py input.mp4 output.mp4 --blur-all
```

### Example 4: Case-insensitive matching
```bash
# These will match "PASSWORD", "Password", "password", etc.
python3 blur_text_video.py input.mp4 output.mp4 --words "password" "email"
```

### Example 5: Partial word matching
```bash
# "pass" will match "password", "passport", "passing", etc.
python3 blur_text_video.py input.mp4 output.mp4 --words "pass" "mail"
```

## 🔧 Technical Details

### Word Matching
- **Case-insensitive**: "Password" matches "password", "PASSWORD", etc.
- **Substring matching**: "pass" matches "password", "passport", etc.
- **Phrase support**: Can match multi-word phrases like "John Doe"

### Video Format
- **Codec**: H.264 (libx264)
- **Pixel Format**: yuv420p (universal compatibility)
- **Quality**: CRF 23 (high quality, reasonable file size)
- **Optimization**: faststart flag for web streaming

### Processing Flow
1. Process video with OpenCV (creates temporary file)
2. Detect text with EasyOCR
3. Blur only matching words
4. Convert to H.264 with FFmpeg
5. Delete temporary file
6. Output QuickTime-compatible MP4

## 🎬 Current Test

Testing with your video:
```bash
Input:  "2 - wx gov - creation Usecase.mp4"
Output: "test_output.mp4"
Words:  "Usecase", "creation"
```

This will blur only text containing "Usecase" or "creation", leaving all other text visible.

## 📊 Performance Tips

1. **Use sample-rate for speed**: `--sample-rate 5` processes every 5th frame
2. **Lower confidence for more detection**: `--confidence 0.3`
3. **Increase blur for stronger effect**: `--blur 71` or `--blur 101`
4. **Add padding for better coverage**: `--padding 20`

## 🐛 Troubleshooting

### QuickTime still won't play
- Check FFmpeg version: `ffmpeg -version`
- Try manual conversion: `ffmpeg -i input.mp4 -c:v libx264 -pix_fmt yuv420p output.mp4`

### Words not being blurred
- Lower confidence: `--confidence 0.3`
- Check spelling (case doesn't matter)
- Try partial words: "pass" instead of "password"
- Process every frame: `--sample-rate 1`

### Too much being blurred
- Use more specific words
- Increase confidence: `--confidence 0.7`
- Check for partial matches (e.g., "go" matches "go", "got", "going")