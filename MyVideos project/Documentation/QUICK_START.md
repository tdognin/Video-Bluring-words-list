# Quick Start Guide

## 🚀 Fastest Way to Use

### Option 1: Interactive Mode (Easiest)
```bash
./run_blur_interactive.sh
```
Then enter the words you want to blur when prompted (e.g., `password, email, secret`)

### Option 2: Command Line
```bash
python3 blur_text_video.py "your-video.mp4" "output.mp4" --words "word1" "word2"
```

## 📋 Common Commands

### Blur specific words
```bash
python3 blur_text_video.py input.mp4 output.mp4 --words "password" "email"
```

### Blur all text
```bash
python3 blur_text_video.py input.mp4 output.mp4 --blur-all
```

### Faster processing (every 5th frame)
```bash
python3 blur_text_video.py input.mp4 output.mp4 --words "secret" --sample-rate 5
```

### Stronger blur
```bash
python3 blur_text_video.py input.mp4 output.mp4 --words "data" --blur 71
```

### Multiple languages
```bash
python3 blur_text_video.py input.mp4 output.mp4 --words "mot" --languages en fr
```

## ✅ What's New

1. **Selective Blurring**: Only blur specific words you choose
2. **QuickTime Compatible**: Output works with QuickTime Player
3. **Interactive Mode**: Easy-to-use prompts for word selection
4. **Case-Insensitive**: "Password" matches "password", "PASSWORD", etc.

## 📁 Your Files

- `run_blur_interactive.sh` - Run with interactive prompts
- `blur_text_video.py` - Main script
- `UPDATED_FEATURES.md` - Detailed feature documentation
- `README.md` - Full documentation

## 🎬 Current Video

Your video: `2 - wx gov - creation Usecase.mp4`

Test command being run:
```bash
python3 blur_text_video.py \
  "2 - wx gov - creation Usecase.mp4" \
  "test_output.mp4" \
  --words "Usecase" "creation" \
  --sample-rate 5
```

This will create `test_output.mp4` with only "Usecase" and "creation" blurred.

## 💡 Tips

- Start with `--sample-rate 5` for faster testing
- Use `--confidence 0.3` if words aren't detected
- Use `--blur 71` or higher for stronger blur
- Words are matched as substrings (case-insensitive)
- Output is always QuickTime-compatible H.264

## 🆘 Need Help?

See `UPDATED_FEATURES.md` for detailed examples and troubleshooting.