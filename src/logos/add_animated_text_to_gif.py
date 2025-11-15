#!/usr/bin/env python3

import argparse
import os
from PIL import Image, ImageDraw, ImageFont

# Font configuration
DEFAULT_FONT = "Roboto Slab"
DEFAULT_FONT_WEIGHT = 300
DEFAULT_FONT_SIZE = 200

# Default color (dark sepia)
DEFAULT_COLOR = (99, 74, 49)  # Dark sepia RGB


def find_font(font_name, size):
    """
    Find and load a font by name.

    Args:
        font_name (str): Name of the font
        size (int): Font size

    Returns:
        ImageFont: Loaded font object
    """
    # Common font paths on Linux
    font_paths = [
        "/usr/share/fonts/truetype/",
        "/usr/share/fonts/opentype/",
        "/usr/share/fonts/TTF/",
        "/usr/local/share/fonts/",
        os.path.expanduser("~/.fonts/"),
        os.path.expanduser("~/.local/share/fonts/"),
    ]

    # Common font filename patterns for Roboto Slab (both .ttf and .otf)
    font_patterns = [
        f"{font_name.replace(' ', '')}-Light.otf",
        f"{font_name.replace(' ', '')}-Regular.otf",
        f"{font_name.replace(' ', '')}-Light.ttf",
        f"{font_name.replace(' ', '')}-{DEFAULT_FONT_WEIGHT}.ttf",
        f"{font_name.replace(' ', '')}.ttf",
        f"{font_name.replace(' ', '-')}-Light.otf",
        f"{font_name.replace(' ', '-')}-Regular.otf",
        f"{font_name.replace(' ', '-')}-Light.ttf",
        f"{font_name.replace(' ', '-')}-{DEFAULT_FONT_WEIGHT}.ttf",
        f"{font_name.replace(' ', '-')}.ttf",
        "RobotoSlab-Light.otf",
        "RobotoSlab-Regular.otf",
        "RobotoSlab-Light.ttf",
        "RobotoSlab-Regular.ttf",
        "RobotoSlab.ttf",
    ]

    # Search for the font
    print(f"Searching for font '{font_name}' (size {size})...")
    for base_path in font_paths:
        if os.path.exists(base_path):
            # Also search recursively in the base path
            for root, dirs, files in os.walk(base_path):
                for pattern in font_patterns:
                    if pattern.lower() in [f.lower() for f in files]:
                        # Find the actual filename with correct case
                        actual_file = [f for f in files if f.lower() == pattern.lower()][0]
                        font_file = os.path.join(root, actual_file)
                        try:
                            font = ImageFont.truetype(font_file, size)
                            print(f"✓ Loaded font: {font_file}")
                            return font
                        except Exception as e:
                            print(f"  Failed to load {font_file}: {e}")
                            continue

    # Try common fallback fonts
    fallback_fonts = [
        "DejaVuSans.ttf",
        "LiberationSans-Regular.ttf",
        "FreeSans.ttf",
        "Ubuntu-R.ttf",
    ]

    print(f"Warning: Could not find '{font_name}', trying fallback fonts...")
    for base_path in font_paths:
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                for fallback in fallback_fonts:
                    if fallback.lower() in [f.lower() for f in files]:
                        actual_file = [f for f in files if f.lower() == fallback.lower()][0]
                        font_file = os.path.join(root, actual_file)
                        try:
                            font = ImageFont.truetype(font_file, size)
                            print(f"✓ Using fallback font: {font_file}")
                            return font
                        except Exception as e:
                            continue

    # Last resort - return None and we'll handle it in the caller
    print(f"ERROR: Could not find any suitable font!")
    print(f"Please install Roboto Slab or another TrueType font.")
    return None


def add_animated_text_to_gif(
    input_gif_path,
    text,
    letter_duration=0.1,
    font_size=DEFAULT_FONT_SIZE,
    colors=None,
    text_margin=80,
    hold_still=0.0
):
    """
    Add animated text that unrolls letter by letter to an existing rotating GIF.

    Args:
        input_gif_path (str): Path to the input rotating GIF
        text (str): Text to animate (e.g., "Lexero")
        letter_duration (float): Time in seconds each letter takes to appear
        font_size (int): Font size for the text
        colors (list): List of RGB tuples for each letter color (None = use default for all)
        text_margin (int): Margin between logo and text in pixels
        hold_still (float): Time in seconds to hold complete text at end (default: 0.0)
    """
    if not os.path.exists(input_gif_path):
        print(f"Error: File '{input_gif_path}' not found")
        return

    # Load the input GIF
    try:
        img = Image.open(input_gif_path)
    except Exception as e:
        print(f"Error loading GIF: {e}")
        return

    # Extract all frames from the input GIF
    original_frames = []
    original_duration = img.info.get('duration', 50)  # Get frame duration in ms

    try:
        while True:
            original_frames.append(img.copy().convert('RGBA'))
            img.seek(img.tell() + 1)
    except EOFError:
        pass  # End of frames

    num_original_frames = len(original_frames)
    print(f"Loaded {num_original_frames} frames from input GIF")
    print(f"Original frame duration: {original_duration}ms")

    # Get original dimensions
    orig_width, orig_height = original_frames[0].size

    # Load font
    font = find_font(DEFAULT_FONT, font_size)
    if font is None:
        print("ERROR: Cannot proceed without a font. Exiting.")
        return

    # Set up colors for each letter
    if colors is None:
        colors = [DEFAULT_COLOR] * len(text)
    elif len(colors) < len(text):
        # Pad with default color if not enough colors provided
        colors = colors + [DEFAULT_COLOR] * (len(text) - len(colors))

    # Calculate text dimensions to determine new canvas width
    # We'll use a temporary draw context to measure text
    temp_img = Image.new('RGBA', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)

    # Measure the full text width
    text_bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calculate new canvas dimensions (double width or more if text is very long)
    new_width = max(orig_width * 2, orig_width + text_width + text_margin + 100)
    new_height = max(orig_height, text_height + 100)

    print(f"Original size: {orig_width}x{orig_height}")
    print(f"New canvas size: {new_width}x{new_height}")
    print(f"Text: '{text}' ({len(text)} letters)")

    # Position for logo (centered vertically, on the left)
    logo_x = (orig_width - orig_width) // 2  # Keep original position
    logo_y = (new_height - orig_height) // 2

    # Starting position for text (to the right of the logo)
    # For proper vertical centering, we need to account for the bbox offset
    text_start_x = orig_width + text_margin

    # Calculate Y position for perfect vertical centering
    # The bbox gives us (left, top, right, bottom) relative to the draw position
    # To center: canvas_center - (visual_top + visual_bottom) / 2
    canvas_center_y = new_height // 2
    text_visual_center = (text_bbox[1] + text_bbox[3]) / 2
    text_y = canvas_center_y - text_visual_center

    # Step 1: Re-render all original frames on the new wider canvas
    expanded_frames = []
    for frame in original_frames:
        # Create new wider canvas
        canvas = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
        # Paste the logo frame
        canvas.paste(frame, (logo_x, logo_y), frame)
        expanded_frames.append(canvas)

    # Step 2: Create text unroll frames (letter by letter)
    text_frames = []
    for i in range(len(text) + 1):  # +1 to show complete text in final frame
        # Start with the last rotation frame (logo at rest)
        canvas = expanded_frames[-1].copy()
        draw = ImageDraw.Draw(canvas)

        # Draw letters one by one
        current_text = text[:i]
        if current_text:
            # Draw each letter with its color
            x_offset = text_start_x
            for j, char in enumerate(current_text):
                # Draw this letter
                draw.text((x_offset, text_y), char, font=font, fill=colors[j])
                # Move x position for next letter
                char_bbox = draw.textbbox((x_offset, text_y), char, font=font)
                x_offset = char_bbox[2]

        text_frames.append(canvas)

    # Step 3: Add hold_still frames (showing complete text)
    hold_still_frames = []
    if hold_still > 0:
        num_hold_frames = int(hold_still / (letter_duration if letter_duration > 0 else 0.1))
        # Use the last text frame (complete text) for all hold frames
        complete_text_frame = text_frames[-1]
        for _ in range(num_hold_frames):
            hold_still_frames.append(complete_text_frame.copy())

    # Combine all frames: rotation + text unroll + hold still
    all_frames = expanded_frames + text_frames + hold_still_frames

    print(f"Total frames: {len(all_frames)} ({num_original_frames} rotation + {len(text_frames)} text + {len(hold_still_frames)} hold)")

    # Calculate durations for each frame
    # Original frames keep their duration, text frames use letter_duration, hold frames use letter_duration
    letter_duration_ms = int(letter_duration * 1000)
    durations = [original_duration] * num_original_frames + [letter_duration_ms] * len(text_frames) + [letter_duration_ms] * len(hold_still_frames)

    # Get output filename
    dir_path = os.path.dirname(input_gif_path)
    filename = os.path.basename(input_gif_path)
    name, _ = os.path.splitext(filename)
    output_path = os.path.join(dir_path, f"{name}_with_text.gif")

    # Save as GIF
    try:
        all_frames[0].save(
            output_path,
            save_all=True,
            append_images=all_frames[1:],
            duration=durations,
            loop=0,  # Infinite loop
            disposal=2  # Clear frame before drawing next one
        )
        print(f"✅ GIF with animated text created: {output_path}")
        print(f"   Animation: {num_original_frames} rotation frames + {len(text_frames)} text frames")
        print(f"   Total duration: {sum(durations) / 1000:.2f} seconds")
    except Exception as e:
        print(f"Error saving GIF: {e}")


def parse_color(color_str):
    """Parse color string in format 'R,G,B' to tuple (R, G, B)"""
    parts = color_str.split(',')
    if len(parts) != 3:
        raise ValueError(f"Invalid color format: {color_str}. Use 'R,G,B' format.")
    return tuple(int(p.strip()) for p in parts)


def main():
    parser = argparse.ArgumentParser(
        description='Add animated text that unrolls letter by letter to a rotating GIF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add "Lexero" with default settings
  %(prog)s logo_rotating_spline.gif "Lexero"

  # Custom letter duration (slower unroll)
  %(prog)s logo_rotating_spline.gif "Lexero" -d 0.2

  # Custom font size
  %(prog)s logo_rotating_spline.gif "Brand" -s 250

  # Custom color for all letters (burgundy)
  %(prog)s logo_rotating_spline.gif "Lexero" --color 128,32,32

  # Different color for each letter
  %(prog)s logo_rotating_spline.gif "RGB" \\
    --colors "255,0,0" "0,255,0" "0,0,255"

  # Custom margin between logo and text
  %(prog)s logo_rotating_spline.gif "Lexero" --margin 120

  # Hold complete text for 1 second before looping
  %(prog)s logo_rotating_spline.gif "Lexero" --hold-still 1.0
        """)

    parser.add_argument('input_gif', help='Path to the input rotating GIF')
    parser.add_argument('text', help='Text to animate (e.g., "Lexero")')
    parser.add_argument('-d', '--duration', type=float, default=0.1,
                       help='Duration for each letter to appear in seconds (default: 0.1)')
    parser.add_argument('-s', '--size', type=int, default=DEFAULT_FONT_SIZE,
                       help=f'Font size (default: {DEFAULT_FONT_SIZE})')
    parser.add_argument('--color', type=str,
                       help='Color for all letters in R,G,B format (e.g., "99,74,49")')
    parser.add_argument('--colors', type=str, nargs='+',
                       help='Different color for each letter in R,G,B format')
    parser.add_argument('--margin', type=int, default=80,
                       help='Margin between logo and text in pixels (default: 80)')
    parser.add_argument('--hold-still', type=float, default=0.0,
                       help='Time in seconds to hold complete text at end before looping (default: 0.0)')

    args = parser.parse_args()

    # Parse colors
    colors = None
    if args.colors:
        colors = [parse_color(c) for c in args.colors]
    elif args.color:
        single_color = parse_color(args.color)
        colors = [single_color] * len(args.text)

    add_animated_text_to_gif(
        args.input_gif,
        args.text,
        args.duration,
        args.size,
        colors,
        args.margin,
        args.hold_still
    )


if __name__ == "__main__":
    main()
