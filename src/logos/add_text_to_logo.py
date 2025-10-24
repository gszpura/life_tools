#!/usr/bin/env python3

import argparse
import os
import random
import colorsys
from PIL import Image, ImageDraw, ImageFont
import math

def hsl_to_rgb(h, s, l):
    """Convert HSL to RGB format string"""
    h = h / 360.0
    s = s / 100.0
    l = l / 100.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r*255), int(g*255), int(b*255))

def create_gradient_text(draw, text, position, font, base_hue, base_saturation):
    """Create text with gradient effect using multiple text layers"""
    x, y = position

    # Create gradient colors
    color1 = hsl_to_rgb(base_hue, base_saturation, random.uniform(85, 95))
    color2 = hsl_to_rgb(base_hue + random.uniform(-10, 10),
                       base_saturation + random.uniform(-5, 5),
                       random.uniform(75, 85))

    # Get text dimensions
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Draw text with gradient simulation (multiple passes with slightly different colors)
    for i in range(10):
        # Interpolate between the two colors
        ratio = i / 9.0
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)

        # Draw text with slight offset for gradient effect
        offset_x = int(text_width * ratio * 0.1)
        draw.text((x + offset_x, y), text, font=font, fill=(r, g, b, 150))

def add_text_to_logo(input_path, text, num_versions=200, fixed_font=None, fixed_size=None, margin=60, text_color=(255, 255, 255)):
    """
    Add text to a logo image with various fonts, sizes, and positions.

    Args:
        input_path (str): Path to the input image file
        text (str): Text to add to the logo
        num_versions (int): Number of versions to generate (default: 200)
        fixed_font (str): Fix font to specific family (e.g., "Montserrat")
        fixed_size (int): Fix font size to specific value (e.g., 250)
        margin (int): Margin between logo and text in pixels (default: 60)
        text_color (tuple): RGB color for text as (R, G, B) (default: (255, 255, 255))
    """
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found")
        return

    # Load the image
    try:
        base_img = Image.open(input_path).convert('RGBA')
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Get file path components
    dir_path = os.path.dirname(input_path)
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)

    # Create output directory
    output_dir = os.path.join(dir_path, f"{name}_with_text")
    os.makedirs(output_dir, exist_ok=True)

    # All fonts available on the system
    font_families = [
        # DejaVu family
        "DejaVu Sans", "DejaVu Serif", "DejaVu Sans Mono",
        # Liberation family  
        "Liberation Sans", "Liberation Serif", "Liberation Sans Narrow", "Liberation Mono",
        # Ubuntu family
        "Ubuntu", "Ubuntu Mono",
        # Free fonts
        "Free Sans", "Free Serif", "Free Mono",
        # Droid fonts
        "Droid Sans", "Droid Serif",
        # Google fonts
        "Roboto", "Roboto Condensed", "Roboto Slab", "Roboto Slab Light", "Open Sans", "Montserrat", "Montserrat Alternates", "Lato",
        # Modern coding fonts
        "Fira Code", "JetBrains Mono", "Cascadia Code",
        # Clean modern fonts
        "Clear Sans", "Comfortaa", "Geist", "Geist Mono",
        # Serif fonts
        "Vollkorn", "Noto Serif", "Noto Serif Display",
        # Noto Sans variants
        "Noto Sans", "Noto Sans Display", "Noto Sans Mono", "Noto Music"
    ]

    print(f"Generating {num_versions} versions with text '{text}'...")

    for i in range(num_versions):
        # Create a copy of the base image
        img = base_img.copy()
        draw = ImageDraw.Draw(img)

        # Random or fixed parameters
        font_size = fixed_size if fixed_size else random.randint(150, 380)
        font_family = fixed_font if fixed_font else random.choice(font_families)

        # Try to load the chosen font family, fallback to others
        font = None
        used_font_name = "default"
        
        # Map font families to actual font file paths that exist on the system
        font_mappings = {
            # DejaVu family
            "DejaVu Sans": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
            "DejaVu Serif": ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
            "DejaVu Sans Mono": ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"],
            
            # Liberation family
            "Liberation Sans": ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"],
            "Liberation Serif": ["/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"],
            "Liberation Sans Narrow": ["/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf"],
            "Liberation Mono": ["/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"],
            
            # Ubuntu family
            "Ubuntu": ["/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf", "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf"],
            "Ubuntu Mono": ["/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf", "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf"],
            
            # Free fonts
            "Free Sans": ["/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", "/usr/share/fonts/truetype/freefont/FreeSans.ttf"],
            "Free Serif": ["/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf", "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"],
            "Free Mono": ["/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", "/usr/share/fonts/truetype/freefont/FreeMono.ttf"],
            
            # Droid fonts
            "Droid Sans": ["/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf", "/usr/share/fonts/truetype/droid/DroidSans.ttf"],
            "Droid Serif": ["/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf", "/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf"],
            
            # Google fonts
            "Roboto": ["/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Bold.ttf", "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Regular.ttf", "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Medium.ttf"],
            "Roboto Condensed": ["/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf", "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Regular.ttf", "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Medium.ttf"],
            "Roboto Slab": ["/usr/share/fonts/opentype/roboto/slab/RobotoSlab-Regular.otf"],
            "Roboto Slab Light": ["/usr/share/fonts/opentype/roboto/slab/RobotoSlab-Light.otf"],
            "Open Sans": ["/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf", "/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf", "/usr/share/fonts/truetype/open-sans/OpenSans-ExtraBold.ttf"],
            "Montserrat": ["/usr/share/fonts/truetype/montserrat/Montserrat-Bold.ttf", "/usr/share/fonts/truetype/montserrat/Montserrat-Regular.ttf", "/usr/share/fonts/truetype/montserrat/Montserrat-Medium.ttf", "/usr/share/fonts/truetype/montserrat/Montserrat-SemiBold.ttf"],
            "Montserrat Alternates": ["/usr/share/fonts/truetype/montserrat/MontserratAlternates-Bold.ttf", "/usr/share/fonts/truetype/montserrat/MontserratAlternates-Regular.ttf", "/usr/share/fonts/truetype/montserrat/MontserratAlternates-Medium.ttf"],
            "Lato": ["/usr/share/fonts/truetype/lato/Lato-Bold.ttf", "/usr/share/fonts/truetype/lato/Lato-Regular.ttf", "/usr/share/fonts/truetype/lato/Lato-Medium.ttf"],
            
            # Modern coding fonts
            "Fira Code": ["/usr/share/fonts/truetype/firacode/FiraCode-Bold.ttf", "/usr/share/fonts/truetype/firacode/FiraCode-Regular.ttf", "/usr/share/fonts/truetype/firacode/FiraCode-Medium.ttf", "/usr/share/fonts/truetype/firacode/FiraCode-SemiBold.ttf"],
            "JetBrains Mono": ["/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf", "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf", "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf"],
            "Cascadia Code": ["/usr/share/fonts/truetype/cascadia-code/CascadiaCode-Bold.ttf", "/usr/share/fonts/truetype/cascadia-code/CascadiaCode-Regular.ttf"],
            
            # Clean modern fonts
            "Clear Sans": ["/usr/share/fonts/truetype/clear-sans/ClearSans-Bold.ttf", "/usr/share/fonts/truetype/clear-sans/ClearSans-Regular.ttf", "/usr/share/fonts/truetype/clear-sans/ClearSans-Medium.ttf"],
            "Comfortaa": ["/usr/share/fonts/truetype/comfortaa/Comfortaa-Bold.ttf", "/usr/share/fonts/truetype/comfortaa/Comfortaa-Regular.ttf"],
            "Geist": ["/home/greg/.fonts/geist-font-main/fonts/Geist/ttf/Geist-Bold.ttf", "/home/greg/.fonts/geist-font-main/fonts/Geist/ttf/Geist-Regular.ttf", "/home/greg/.fonts/geist-font-main/fonts/Geist/ttf/Geist-SemiBold.ttf"],
            "Geist Mono": ["/home/greg/.fonts/geist-font-main/fonts/GeistMono/ttf/GeistMono-Bold.ttf", "/home/greg/.fonts/geist-font-main/fonts/GeistMono/ttf/GeistMono-Regular.ttf", "/home/greg/.fonts/geist-font-main/fonts/GeistMono/ttf/GeistMono-SemiBold.ttf"],
            
            # Serif fonts
            "Vollkorn": ["/usr/share/fonts/truetype/vollkorn/Vollkorn-Bold.ttf", "/usr/share/fonts/truetype/vollkorn/Vollkorn-Regular.ttf", "/usr/share/fonts/truetype/vollkorn/Vollkorn-Medium.ttf", "/usr/share/fonts/truetype/vollkorn/Vollkorn-SemiBold.ttf"],
            "Noto Serif": ["/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf", "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"],
            "Noto Serif Display": ["/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf", "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf"],
            
            # Noto Sans variants
            "Noto Sans": ["/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"],
            "Noto Sans Display": ["/usr/share/fonts/truetype/noto/NotoSansDisplay-Bold.ttf", "/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf"],
            "Noto Sans Mono": ["/usr/share/fonts/truetype/noto/NotoSansMono-Bold.ttf", "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf"],
            "Noto Music": ["/usr/share/fonts/truetype/noto/NotoMusic-Regular.ttf"]
        }
        
        # Try the selected font family first
        if font_family in font_mappings:
            for font_path in font_mappings[font_family]:
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    used_font_name = f"{font_family} ({os.path.basename(font_path)})"
                    break
                except:
                    continue
        
        # If selected font failed, try all other fonts as fallback
        if font is None:
            all_font_paths = []
            for paths in font_mappings.values():
                all_font_paths.extend(paths)
            
            for font_path in all_font_paths:
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    used_font_name = f"fallback ({os.path.basename(font_path)})"
                    break
                except:
                    continue
        
        # Last resort: default font
        if font is None:
            font = ImageFont.load_default()
            used_font_name = "system_default"


        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Position text to the right of the logo
        img_width, img_height = img.size

        # Calculate text position starting at 3/4 of original image width and positioned higher
        x = int(img_width * 3/4) + margin
        y = (img_height - text_height) // 2 - font_size // 2

        # Expand canvas to fit text on the right
        new_width = x + text_width + margin
        new_height = max(img_height, text_height + margin * 2)
        
        # Create new larger canvas
        new_img = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
        new_img.paste(img, (0, 0))
        
        # Update image and draw objects
        img = new_img
        draw = ImageDraw.Draw(img)

        # Draw text with specified color
        draw.text((x, y), text, font=font, fill=(*text_color, 255))

        # Save the image
        output_filename = f"{name}_text_{i:03d}{ext}"
        output_path = os.path.join(output_dir, output_filename)
        img.save(output_path)

        # Print font info for this image
        print(f"Generated {output_filename}: {used_font_name}, size {font_size}")

        if (i + 1) % 50 == 0:
            print(f"--- Progress: {i + 1}/{num_versions} versions ---")

    print(f"✅ Generated {num_versions} logo versions with text in '{output_dir}'")

def main():
    parser = argparse.ArgumentParser(description='Add text to logo with various fonts and styles')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('text', help='Text to add to the logo')
    parser.add_argument('-n', '--num-versions', type=int, default=200,
                       help='Number of versions to generate (default: 200)')
    parser.add_argument('--font', type=str, help='Fix font to specific family (e.g., "Montserrat")')
    parser.add_argument('--size', type=int, help='Fix font size to specific value (e.g., 250)')
    parser.add_argument('--margin', type=int, default=60, help='Margin between logo and text in pixels (default: 60)')
    parser.add_argument('--color', type=str, default='255,255,255', help='Text color as R,G,B (e.g., 255,255,255 for white)')

    args = parser.parse_args()
    
    # Parse color argument
    text_color = tuple(map(int, args.color.split(',')))

    add_text_to_logo(args.input_file, args.text, args.num_versions, args.font, args.size, args.margin, text_color)

if __name__ == "__main__":
    main()
