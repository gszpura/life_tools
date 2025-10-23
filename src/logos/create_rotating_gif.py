#!/usr/bin/env python3

import argparse
import os
from PIL import Image

def create_rotating_gif(input_path, frame_duration=0.1, rotation_step=30):
    """
    Create a rotating GIF from a PNG image.
    
    Args:
        input_path (str): Path to the input PNG file
        frame_duration (float): Duration of each frame in seconds (default: 0.1)
        rotation_step (int): Degrees to rotate for each frame (default: 30)
    """
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found")
        return
    
    # Load the image
    try:
        img = Image.open(input_path)
    except Exception as e:
        print(f"Error loading image: {e}")
        return
    
    # Calculate number of frames needed for full rotation
    num_frames = 360 // rotation_step
    
    # Get output filename
    dir_path = os.path.dirname(input_path)
    filename = os.path.basename(input_path)
    name, _ = os.path.splitext(filename)
    output_path = os.path.join(dir_path, f"{name}_rotating.gif")
    
    print(f"Creating GIF with {num_frames} frames, {rotation_step} degrees per frame...")
    print(f"Frame duration: {frame_duration} seconds")
    
    # Get original image dimensions
    orig_width, orig_height = img.size
    
    # Generate frames
    frames = []
    for i in range(num_frames):
        rotation_angle = i * rotation_step
        
        # Create a clean transparent canvas for each frame
        canvas = Image.new('RGBA', (orig_width, orig_height), (0, 0, 0, 0))
        
        # Rotate image around center without expanding
        rotated_img = img.rotate(rotation_angle, expand=False)
        
        # Paste only the rotated image onto the clean canvas
        canvas.paste(rotated_img, (0, 0))
        frames.append(canvas)
    
    # Convert frame duration to milliseconds for PIL
    duration_ms = int(frame_duration * 1000)
    
    # Save as GIF with disposal method to clear previous frame
    try:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration_ms,
            loop=0,  # 0 means infinite loop
            disposal=2  # Clear frame before drawing next one
        )
        print(f"✅ GIF created: {output_path}")
    except Exception as e:
        print(f"Error saving GIF: {e}")

def main():
    parser = argparse.ArgumentParser(description='Create a rotating GIF from a PNG image')
    parser.add_argument('input_file', help='Path to the input PNG file')
    parser.add_argument('-d', '--duration', type=float, default=0.1, 
                       help='Duration of each frame in seconds (default: 0.1)')
    parser.add_argument('-s', '--step', type=int, default=30, 
                       help='Rotation degrees for each frame (default: 30)')
    
    args = parser.parse_args()
    
    create_rotating_gif(args.input_file, args.duration, args.step)

if __name__ == "__main__":
    main()