# Blur Specific Words Example

## Command Executed
```bash
python3 blur_text_video.py \
  "input_video.mp4" \
  "output_blurred.mp4" \
  --words "CompanyName" "SecretWord" \
  --blur 51 \
  --confidence 0.5 \
  --sample-rate 3 \
  --padding 15
```

## What This Does
- **Input Video**: `input_video.mp4`
- **Output Video**: `output_blurred.mp4`
- **Target Words**: "CompanyName", "SecretWord" (case-insensitive)
- **Behavior**: Only text containing the specified words will be blurred
- **All other text**: Remains visible and unblurred
- **Output Format**: QuickTime-compatible H.264 MP4

## Settings
- **Blur Strength**: 51 (moderate blur)
- **Confidence**: 0.5 (50% OCR confidence threshold)
- **Sample Rate**: 3 (processes every 3rd frame for speed)
- **Padding**: 15 pixels around detected text

## Expected Result
The output video will have:
- ✅ Specified words blurred wherever they appear
- ✅ All other text visible and clear
- ✅ QuickTime Player compatibility
- ✅ Same resolution and FPS as original

## If You Need to Adjust

### Blur more aggressively
```bash
python3 blur_text_video.py "input_video.mp4" output.mp4 \
  --words "CompanyName" "SecretWord" --blur 71 --padding 20
```

### Process every frame (slower but more accurate)
```bash
python3 blur_text_video.py "input_video.mp4" output.mp4 \
  --words "CompanyName" "SecretWord" --sample-rate 1
```

### Lower confidence (detect more instances)
```bash
python3 blur_text_video.py "input_video.mp4" output.mp4 \
  --words "CompanyName" "SecretWord" --confidence 0.3
```

### Add more words to blur
```bash
python3 blur_text_video.py "input_video.mp4" output.mp4 \
  --words "CompanyName" "SecretWord" "Confidential" "Password"
```

## Usage Tips
- Replace "CompanyName" and "SecretWord" with your actual target words
- Words are case-insensitive (will match "companyname", "COMPANYNAME", etc.)
- You can specify as many words as needed
- Use quotes around words with spaces: --words "Company Name" "Secret Phrase"