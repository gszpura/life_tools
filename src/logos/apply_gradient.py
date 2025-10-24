#!/usr/bin/env python3
"""
Apply a symmetric creamy gradient to an image:
- The middle stays the main color (unchanged).
- Left side gets slightly darker.
- Right side gets slightly lighter.

Usage:
    python apply_gradient.py input.png output.png --main 255,240,220 --strength 0.1
    python src/logos/apply_gradient.py data/logo.png output.png --main 230,227,219 --strength 0.1
"""

import argparse
from PIL import Image
import numpy as np

def apply_gradient(input_path, output_path, main_color, strength=0.1):
    """
    main_color: tuple (R, G, B)
    strength: how much to darken/lighten sides (e.g., 0.1 = ±10%)
    """
    # Load image and preserve alpha channel
    img = Image.open(input_path)
    has_alpha = img.mode in ('RGBA', 'LA')
    if has_alpha:
        img_rgb = img.convert("RGB")
        alpha_channel = img.split()[-1]  # Get alpha channel
    else:
        img_rgb = img.convert("RGB")

    width, height = img_rgb.size

    # Normalize X coordinates (0..1)
    x = np.linspace(0, 1, width)

    # Create gradient using only the main color
    # Left side: darker version of main color
    # Center: main color
    # Right side: lighter version of main color
    gradient_multiplier = (1 - strength) + x * (2 * strength)
    gradient_multiplier = np.tile(gradient_multiplier, (height, 1))

    # Convert image to array (we'll use this only for shape and alpha)
    img_array = np.asarray(img_rgb, dtype=float)
    main = np.array(main_color, dtype=float)

    # Apply gradient using only the main color
    for c in range(3):
        # Set each channel to the main color modified by the gradient
        img_array[..., c] = main[c] * gradient_multiplier

    # Clip values to valid range
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)

    # Reconstruct image with alpha channel if it existed
    if has_alpha:
        result = Image.fromarray(img_array)
        result.putalpha(alpha_channel)
    else:
        result = Image.fromarray(img_array)

    result.save(output_path)
    print(f"✅ Saved gradient image to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Apply a symmetric creamy gradient to an image.")
    parser.add_argument("input", help="Path to input image")
    parser.add_argument("output", help="Path to output image")
    parser.add_argument("--main", type=str, required=True, help="Main creamy color as R,G,B (e.g., 255,240,220)")
    parser.add_argument("--strength", type=float, default=0.1, help="Gradient strength (e.g., 0.1 = ±10%)")

    args = parser.parse_args()
    main_color = tuple(map(int, args.main.split(",")))
    apply_gradient(args.input, args.output, main_color, args.strength)

if __name__ == "__main__":
    main()
