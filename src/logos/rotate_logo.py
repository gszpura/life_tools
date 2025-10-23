#!/usr/bin/env python3

import argparse
import os
from PIL import Image

def rotate_image(input_path, rotation_degrees=30):
    """
    Rotate an image by specified degrees and save multiple rotated versions.
    
    Args:
        input_path (str): Path to the input PNG file
        rotation_degrees (int): Degrees to rotate for each step (default: 30)
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
    
    # Calculate number of rotations needed for full circle
    num_rotations = 360 // rotation_degrees
    
    # Get file path components
    dir_path = os.path.dirname(input_path)
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    
    print(f"Rotating image {num_rotations} times by {rotation_degrees} degrees each...")
    
    # Generate rotated images
    for i in range(num_rotations):
        rotation_angle = i * rotation_degrees
        
        # Rotate image (PIL rotates counter-clockwise)
        rotated_img = img.rotate(rotation_angle, expand=True, fillcolor=(255, 255, 255, 0))
        
        # Create output filename
        output_filename = f"{name}_{rotation_angle}{ext}"
        output_path = os.path.join(dir_path, output_filename)
        
        # Save rotated image
        rotated_img.save(output_path)
        print(f"Saved: {output_filename}")
    
    print(f" Generated {num_rotations} rotated images")

def main():
    parser = argparse.ArgumentParser(description='Rotate a PNG image by specified degrees')
    parser.add_argument('input_file', help='Path to the input PNG file')
    parser.add_argument('-d', '--degrees', type=int, default=30, 
                       help='Rotation degrees for each step (default: 30)')
    
    args = parser.parse_args()
    
    rotate_image(args.input_file, args.degrees)

if __name__ == "__main__":
    main()