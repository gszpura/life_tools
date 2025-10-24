#!/usr/bin/env python3

import argparse
import os
import numpy as np
from PIL import Image
import colorsys

def rgb_to_hsl(r, g, b):
    """Convert RGB to HSL"""
    return colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)

def hsl_to_rgb(h, l, s):
    """Convert HSL to RGB"""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return int(r*255), int(g*255), int(b*255)

def is_cream_color(r, g, b, tolerance=50):
    """Check if a color is in the cream/beige range"""
    h, l, s = rgb_to_hsl(r, g, b)
    
    # Cream colors typically have:
    # - Hue in yellow-orange range (30-60 degrees, normalized to 0.08-0.17)
    # - High lightness (75-95%)
    # - Low to medium saturation (10-40%)
    
    cream_hue_min = 30/360.0  # 0.08
    cream_hue_max = 60/360.0  # 0.17
    cream_lightness_min = 0.70
    cream_lightness_max = 0.98
    cream_saturation_min = 0.05
    cream_saturation_max = 0.45
    
    return (cream_hue_min <= h <= cream_hue_max and 
            cream_lightness_min <= l <= cream_lightness_max and 
            cream_saturation_min <= s <= cream_saturation_max)

def hex_to_rgb(hex_color):
    """Convert hex color to RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def convert_cream_to_target(r, g, b, target_hex="#8B4513"):
    """Convert cream color to target color equivalent"""
    if not is_cream_color(r, g, b):
        return r, g, b  # Return unchanged if not cream
    
    # Get original cream color properties
    original_h, original_l, original_s = rgb_to_hsl(r, g, b)
    
    # Get target color properties
    target_r, target_g, target_b = hex_to_rgb(target_hex)
    target_h, target_l, target_s = rgb_to_hsl(target_r, target_g, target_b)
    
    # Map cream lightness range (70-98%) to target-based range
    cream_lightness_range = (0.70, 0.98)
    
    # Calculate relative position in cream lightness range
    lightness_position = (original_l - cream_lightness_range[0]) / (cream_lightness_range[1] - cream_lightness_range[0])
    lightness_position = max(0, min(1, lightness_position))
    
    # Create target lightness range around the target color
    target_lightness_min = max(0.1, target_l - 0.2)
    target_lightness_max = min(0.9, target_l + 0.3)
    
    # Map to target lightness range
    new_lightness = target_lightness_min + lightness_position * (target_lightness_max - target_lightness_min)
    
    # Use target hue with slight variation based on original
    hue_variation = (original_h - 45/360.0) * 0.1  # Small variation based on original hue
    new_hue = target_h + hue_variation
    new_hue = new_hue % 1.0  # Keep in 0-1 range
    
    # Blend saturation between original and target
    saturation_blend = 0.7  # 70% target, 30% original
    new_saturation = target_s * saturation_blend + original_s * (1 - saturation_blend)
    new_saturation = max(0.1, min(0.9, new_saturation))
    
    return hsl_to_rgb(new_hue, new_lightness, new_saturation)

def convert_image_to_target(input_path, target_hex="#8B4513", output_path=None):
    """Convert cream colors in an image to brown/sepia tones"""
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found")
        return
    
    # Load image
    try:
        img = Image.open(input_path).convert('RGBA')
    except Exception as e:
        print(f"Error loading image: {e}")
        return
    
    # Convert to numpy array for processing
    img_array = np.array(img)
    
    # Process each pixel
    height, width = img_array.shape[:2]
    converted_count = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = img_array[y, x]
            
            # Skip transparent pixels
            if a == 0:
                continue
                
            # Convert cream colors to target color
            new_r, new_g, new_b = convert_cream_to_target(r, g, b, target_hex)
            
            if (new_r, new_g, new_b) != (r, g, b):
                img_array[y, x] = [new_r, new_g, new_b, a]
                converted_count += 1
    
    # Convert back to PIL Image
    converted_img = Image.fromarray(img_array, 'RGBA')
    
    # Determine output path
    if output_path is None:
        name, ext = os.path.splitext(input_path)
        output_path = f"{name}_brown{ext}"
    
    # Save converted image
    converted_img.save(output_path)
    
    print(f"✅ Converted {converted_count} cream pixels to target color {target_hex}")
    print(f"💾 Saved as: {output_path}")
    
    return output_path

def batch_convert_directory(input_dir, target_hex="#8B4513", output_dir=None):
    """Convert all images in a directory"""
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' not found")
        return
    
    if output_dir is None:
        output_dir = f"{input_dir}_brown"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Supported image formats
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')
    
    converted_files = []
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            print(f"Converting: {filename}")
            result = convert_image_to_target(input_path, target_hex, output_path)
            if result:
                converted_files.append(result)
    
    print(f"\n✅ Batch conversion complete!")
    print(f"📁 Converted {len(converted_files)} files to '{output_dir}'")

def main():
    parser = argparse.ArgumentParser(description='Convert cream colors to custom target color in images')
    parser.add_argument('input', help='Input image file or directory')
    parser.add_argument('-c', '--color', default='#8B4513', 
                       help='Target hex color (default: #8B4513 - saddle brown)')
    parser.add_argument('-o', '--output', help='Output file or directory path')
    parser.add_argument('-b', '--batch', action='store_true', 
                       help='Batch process all images in input directory')
    
    args = parser.parse_args()
    
    if args.batch or os.path.isdir(args.input):
        batch_convert_directory(args.input, args.color, args.output)
    else:
        convert_image_to_target(args.input, args.color, args.output)

if __name__ == "__main__":
    main()