#!/usr/bin/env python3
"""
Video Text Blur Tool
Detects and blurs specific text/words in MP4/MOV videos using OCR and OpenCV
"""

import cv2
import easyocr
import numpy as np
from pathlib import Path
import argparse
from tqdm import tqdm
import sys
import subprocess


class VideoTextBlur:
    def __init__(self, languages=['en'], blur_strength=51, confidence_threshold=0.5, target_words=None):
        """
        Initialize the video text blur processor
        
        Args:
            languages: List of languages for OCR (e.g., ['en', 'fr'])
            blur_strength: Blur kernel size (must be odd number, higher = more blur)
            confidence_threshold: Minimum confidence for text detection (0-1)
            target_words: List of words/phrases to blur (case-insensitive). If None, blur all text.
        """
        print("Initializing EasyOCR reader...")
        self.reader = easyocr.Reader(languages, gpu=True)
        self.blur_strength = blur_strength if blur_strength % 2 == 1 else blur_strength + 1
        self.confidence_threshold = confidence_threshold
        self.target_words = [word.lower() for word in target_words] if target_words else None
        
        if self.target_words:
            print(f"\nTarget words to blur: {', '.join(self.target_words)}")
        else:
            print("\nMode: Blur ALL detected text")
        
    def should_blur_text(self, detected_text):
        """
        Check if detected text should be blurred based on target words
        
        Args:
            detected_text: Text detected by OCR
            
        Returns:
            True if text should be blurred, False otherwise
        """
        if self.target_words is None:
            return True  # Blur all text if no specific words provided
        
        detected_lower = detected_text.lower()
        
        # Check if any target word is in the detected text
        for target in self.target_words:
            if target in detected_lower:
                return True
        
        return False
        
    def detect_text_regions(self, frame):
        """
        Detect text regions in a frame that match target words
        
        Returns:
            List of tuples: [(x1, y1, x2, y2, detected_text), ...]
        """
        results = self.reader.readtext(frame)
        boxes = []
        
        for detection in results:
            bbox, text, confidence = detection
            # Ensure confidence is a float for comparison
            if float(confidence) >= self.confidence_threshold:
                if self.should_blur_text(text):
                    # Convert bbox to x1, y1, x2, y2 format
                    points = np.array(bbox, dtype=np.int32)
                    x1, y1 = points.min(axis=0)
                    x2, y2 = points.max(axis=0)
                    boxes.append((x1, y1, x2, y2, text))
                
        return boxes
    
    def blur_regions(self, frame, boxes, padding=10):
        """
        Apply blur to specified regions in the frame
        
        Args:
            frame: Input frame
            boxes: List of tuples (x1, y1, x2, y2, text) to blur
            padding: Extra pixels around detected text
        """
        blurred_frame = frame.copy()
        
        for box_data in boxes:
            x1, y1, x2, y2 = box_data[:4]  # Extract coordinates, ignore text
            
            # Add padding
            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)
            x2 = min(frame.shape[1], x2 + padding)
            y2 = min(frame.shape[0], y2 + padding)
            
            # Extract region
            roi = frame[y1:y2, x1:x2]
            
            # Apply Gaussian blur
            blurred_roi = cv2.GaussianBlur(roi, (self.blur_strength, self.blur_strength), 0)
            
            # Replace region in frame
            blurred_frame[y1:y2, x1:x2] = blurred_roi
            
        return blurred_frame
    
    def process_video(self, input_path, output_path, sample_rate=1, padding=10):
        """
        Process video and blur detected text
        
        Args:
            input_path: Path to input video
            output_path: Path to output video
            sample_rate: Process every Nth frame for text detection (1 = every frame)
            padding: Padding around detected text regions
        """
        input_path = Path(input_path)
        output_path = Path(output_path)
        temp_output = output_path.with_suffix('.temp.mp4')
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input video not found: {input_path}")
        
        # Open video
        cap = cv2.VideoCapture(str(input_path))
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {input_path}")
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"\nVideo Info:")
        print(f"  Resolution: {width}x{height}")
        print(f"  FPS: {fps}")
        print(f"  Total Frames: {total_frames}")
        print(f"  Duration: {total_frames/fps:.2f} seconds")
        
        # Setup video writer with H.264 codec for QuickTime compatibility
        fourcc = cv2.VideoWriter_fourcc(*'avc1')  # type: ignore  # H.264 codec
        out = cv2.VideoWriter(str(temp_output), fourcc, fps, (width, height))
        
        if not out.isOpened():
            raise ValueError(f"Could not create output video: {output_path}")
        
        print(f"\nProcessing video (sampling every {sample_rate} frame(s))...")
        
        frame_count = 0
        last_boxes = []
        
        with tqdm(total=total_frames, unit='frame') as pbar:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Detect text on sampled frames
                if frame_count % sample_rate == 0:
                    last_boxes = self.detect_text_regions(frame)
                
                # Apply blur using last detected boxes
                if last_boxes:
                    frame = self.blur_regions(frame, last_boxes, padding)
                
                out.write(frame)
                frame_count += 1
                pbar.update(1)
        
        # Cleanup
        cap.release()
        out.release()
        
        # Convert to QuickTime-compatible format using FFmpeg
        print(f"\nConverting to QuickTime-compatible format...")
        try:
            subprocess.run([
                'ffmpeg', '-i', str(temp_output),
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart',
                '-y',
                str(output_path)
            ], check=True, capture_output=True)
            
            # Remove temporary file
            temp_output.unlink()
            
            print(f"\n✓ Video processed successfully!")
            print(f"  Output saved to: {output_path}")
            print(f"  Processed {frame_count} frames")
            print(f"  Format: QuickTime-compatible H.264")
            
        except subprocess.CalledProcessError as e:
            print(f"\n⚠ Warning: FFmpeg conversion failed. Using temporary output.")
            print(f"  You can manually convert with: ffmpeg -i {temp_output} -c:v libx264 {output_path}")
            if temp_output.exists():
                temp_output.rename(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Blur specific words/text in videos (MP4/MOV)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Blur specific words (interactive mode)
  python blur_text_video.py input.mp4 output.mp4
  
  # Blur specific words (command line)
  python blur_text_video.py input.mp4 output.mp4 --words "password" "secret" "confidential"
  
  # Blur ALL text
  python blur_text_video.py input.mp4 output.mp4 --blur-all
  
  # With custom settings
  python blur_text_video.py input.mov output.mov --words "email" --blur 71 --sample-rate 5
  
  # Multiple languages
  python blur_text_video.py input.mp4 output.mp4 --words "mot" "texte" --languages en fr
        """
    )
    
    parser.add_argument('input', help='Input video file (MP4/MOV)')
    parser.add_argument('output', help='Output video file')
    parser.add_argument('--words', nargs='*', default=None,
                        help='Specific words/phrases to blur (case-insensitive). If not provided, will prompt interactively.')
    parser.add_argument('--blur-all', action='store_true',
                        help='Blur ALL detected text (ignores --words)')
    parser.add_argument('--languages', nargs='+', default=['en'],
                        help='OCR languages (default: en)')
    parser.add_argument('--blur', type=int, default=51,
                        help='Blur strength (odd number, default: 51)')
    parser.add_argument('--confidence', type=float, default=0.5,
                        help='Text detection confidence threshold 0-1 (default: 0.5)')
    parser.add_argument('--sample-rate', type=int, default=1,
                        help='Process every Nth frame for detection (default: 1)')
    parser.add_argument('--padding', type=int, default=10,
                        help='Padding around text regions in pixels (default: 10)')
    
    args = parser.parse_args()
    
    try:
        # Determine target words
        target_words = None
        
        if args.blur_all:
            print("\n🔍 Mode: Blur ALL detected text")
            target_words = None
        elif args.words:
            target_words = args.words
            print(f"\n🔍 Mode: Blur specific words")
        else:
            # Interactive mode - prompt user for words
            print("\n" + "="*60)
            print("INTERACTIVE MODE: Specify Words to Blur")
            print("="*60)
            print("\nEnter the words or phrases you want to blur in the video.")
            print("Separate multiple words with commas.")
            print("Leave empty to blur ALL text.\n")
            
            user_input = input("Words to blur (or press Enter for all text): ").strip()
            
            if user_input:
                # Split by comma and clean up
                target_words = [word.strip() for word in user_input.split(',') if word.strip()]
                if not target_words:
                    target_words = None
            else:
                target_words = None
        
        # Initialize processor
        processor = VideoTextBlur(
            languages=args.languages,
            blur_strength=args.blur,
            confidence_threshold=args.confidence,
            target_words=target_words
        )
        
        # Process video
        processor.process_video(
            input_path=args.input,
            output_path=args.output,
            sample_rate=args.sample_rate,
            padding=args.padding
        )
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
