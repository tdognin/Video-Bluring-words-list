#!/bin/bash
# Interactive script to blur specific words in your video

INPUT_VIDEO="2 - wx gov - creation Usecase.mp4"
OUTPUT_VIDEO="2 - wx gov - creation Usecase_BLURRED.mp4"

echo "=========================================="
echo "Video Text Blur Tool - Interactive Mode"
echo "=========================================="
echo ""
echo "Input:  $INPUT_VIDEO"
echo "Output: $OUTPUT_VIDEO"
echo ""

# Run the script in interactive mode
python3 blur_text_video.py "$INPUT_VIDEO" "$OUTPUT_VIDEO" \
    --blur 51 \
    --confidence 0.5 \
    --sample-rate 3 \
    --padding 15

echo ""
echo "=========================================="
echo "Done! Check the output file:"
echo "$OUTPUT_VIDEO"
echo "=========================================="

# Made with Bob
