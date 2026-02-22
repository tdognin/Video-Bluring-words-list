# Quick Usage Summary

## Your Video
- **Input:** `2 - wx gov - creation Usecase.mp4`
- **Output:** `2 - wx gov - creation Usecase_BLURRED.mp4`

## Current Processing Settings
```bash
python3 blur_text_video.py \
  "2 - wx gov - creation Usecase.mp4" \
  "2 - wx gov - creation Usecase_BLURRED.mp4" \
  --blur 51 \
  --confidence 0.5 \
  --sample-rate 3 \
  --padding 15
```

### Settings Explained:
- `--blur 51`: Moderate blur strength (higher = more blur)
- `--confidence 0.5`: Detects text with 50%+ confidence
- `--sample-rate 3`: Processes every 3rd frame (faster)
- `--padding 15`: 15 pixels padding around detected text

## Quick Commands

### Run with the convenience script:
```bash
./run_blur.sh
```

### Run directly with different settings:
```bash
# Stronger blur
python3 blur_text_video.py "2 - wx gov - creation Usecase.mp4" output.mp4 --blur 71

# Process every frame (slower but more accurate)
python3 blur_text_video.py "2 - wx gov - creation Usecase.mp4" output.mp4 --sample-rate 1

# Lower confidence (detect more text)
python3 blur_text_video.py "2 - wx gov - creation Usecase.mp4" output.mp4 --confidence 0.3

# Multiple languages
python3 blur_text_video.py "2 - wx gov - creation Usecase.mp4" output.mp4 --languages en fr
```

## Troubleshooting

### If text isn't being detected:
- Lower confidence: `--confidence 0.3`
- Process every frame: `--sample-rate 1`
- Add more languages: `--languages en fr es`

### If too much is blurred:
- Raise confidence: `--confidence 0.7`
- Reduce padding: `--padding 5`

### If processing is too slow:
- Increase sample rate: `--sample-rate 5` or `--sample-rate 10`
- This processes fewer frames but is much faster

## Files Created
- `blur_text_video.py` - Main script
- `requirements.txt` - Dependencies
- `run_blur.sh` - Convenience script for your video
- `Documentation/README.md` - Full documentation
- `example_usage.py` - Code examples

## Next Steps
Once processing completes:
1. Check the output video: `2 - wx gov - creation Usecase_BLURRED.mp4`
2. If results aren't perfect, adjust settings and re-run
3. Use `run_blur.sh` for quick re-processing