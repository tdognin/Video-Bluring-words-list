#!/usr/bin/env python3
"""
Example usage of the VideoTextBlur class
Demonstrates how to use the tool programmatically
"""

from blur_text_video import VideoTextBlur
from pathlib import Path


def example_basic():
    """Basic usage example"""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    processor = VideoTextBlur(languages=['en'])
    processor.process_video(
        input_path='input.mp4',
        output_path='output_basic.mp4'
    )


def example_custom_settings():
    """Example with custom settings"""
    print("\n" + "=" * 60)
    print("Example 2: Custom Settings")
    print("=" * 60)
    
    processor = VideoTextBlur(
        languages=['en', 'fr'],  # Multiple languages
        blur_strength=71,         # Stronger blur
        confidence_threshold=0.7  # Higher confidence
    )
    
    processor.process_video(
        input_path='input.mp4',
        output_path='output_custom.mp4',
        sample_rate=5,  # Process every 5th frame
        padding=20      # More padding around text
    )


def example_batch_processing():
    """Example: Process multiple videos"""
    print("\n" + "=" * 60)
    print("Example 3: Batch Processing")
    print("=" * 60)
    
    processor = VideoTextBlur(languages=['en'])
    
    video_files = [
        'video1.mp4',
        'video2.mp4',
        'video3.mov'
    ]
    
    for video in video_files:
        if Path(video).exists():
            output = f"blurred_{video}"
            print(f"\nProcessing: {video} -> {output}")
            processor.process_video(
                input_path=video,
                output_path=output,
                sample_rate=3
            )


def example_with_error_handling():
    """Example with proper error handling"""
    print("\n" + "=" * 60)
    print("Example 4: With Error Handling")
    print("=" * 60)
    
    try:
        processor = VideoTextBlur(
            languages=['en'],
            blur_strength=51,
            confidence_threshold=0.5
        )
        
        input_file = 'input.mp4'
        output_file = 'output_safe.mp4'
        
        if not Path(input_file).exists():
            print(f"Error: Input file '{input_file}' not found!")
            return
        
        processor.process_video(
            input_path=input_file,
            output_path=output_file,
            sample_rate=1,
            padding=10
        )
        
        print(f"\n✓ Successfully processed: {output_file}")
        
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    print("Video Text Blur - Example Usage\n")
    print("Note: Make sure you have video files in the current directory")
    print("or modify the paths in the examples.\n")
    
    # Uncomment the example you want to run:
    
    # example_basic()
    # example_custom_settings()
    # example_batch_processing()
    # example_with_error_handling()
    
    print("\nTo run an example, uncomment it in the __main__ section.")

# Made with Bob
