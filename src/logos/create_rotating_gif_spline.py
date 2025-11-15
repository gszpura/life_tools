#!/usr/bin/env python3

import argparse
import os
from PIL import Image
import math

def create_rotating_gif_spline(input_path, slowdown_curve, animation_length, frame_duration=0.05, hold_still=0.0):
    """
    Create a rotating GIF from a PNG image with a custom slowdown curve.

    The animation starts fast and gradually slows down according to the slowdown curve,
    completing multiple rotations over the animation length and ending at the starting position.

    Args:
        input_path (str): Path to the input PNG file
        slowdown_curve (callable): Function that takes (time, animation_length) and returns
                                   rotation speed in degrees per second
        animation_length (float): Total length of animation in seconds
        frame_duration (float): Duration of each frame in seconds (default: 0.05)
        hold_still (float): Time in seconds to hold the logo still at the end (default: 0.0)
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

    # Calculate frames and rotations using numerical integration
    frames = []
    angles = []
    times = []

    current_time = 0.0
    total_angle = 0.0

    # Generate frames for the entire animation length
    while current_time <= animation_length:
        times.append(current_time)
        angles.append(total_angle)  # Store raw angles for now

        # Calculate velocity at current time
        velocity = slowdown_curve(current_time, animation_length)  # degrees per second

        # Calculate angle change for this frame
        angle_delta = velocity * frame_duration

        # Update for next iteration
        total_angle += angle_delta
        current_time += frame_duration

    # Scale angles so the rotation ends at exactly the nearest multiple of 360 degrees
    # This ensures smooth looping without jumps

    # Explicit check: if total rotation is less than 270°, keep partial rotation
    # Otherwise scale to nearest multiple of 360° (to avoid missing almost-full circles)
    if total_angle < 270.0:
        print(f"Note: Total rotation ({total_angle:.1f}°) is less than 270°")
        print(f"  Keeping partial rotation - there will be a jump when looping")
        # Don't scale - keep original angles as-is
        # Apply modulo to keep angles in [0, 360) range
        angles = [angle % 360.0 for angle in angles]
    else:
        # We have enough rotation - scale to nearest multiple of 360
        num_full_rotations = round(total_angle / 360.0)
        target_angle = num_full_rotations * 360.0

        scale_factor = target_angle / total_angle
        angles = [angle * scale_factor for angle in angles]
        total_angle = target_angle

        # Now apply modulo to keep angles in [0, 360) range for rendering
        angles = [angle % 360.0 for angle in angles]

    # The last frame should be at 0 degrees for looping
    angles[-1] = 0.0

    # Add hold_still frames at the end (all at 0 degrees)
    if hold_still > 0:
        num_hold_frames = int(hold_still / frame_duration)
        for _ in range(num_hold_frames):
            angles.append(0.0)
            times.append(current_time)
            current_time += frame_duration

    num_frames = len(angles)
    num_rotations = total_angle / 360.0
    total_duration = animation_length + hold_still

    # Get output filename
    dir_path = os.path.dirname(input_path)
    filename = os.path.basename(input_path)
    name, _ = os.path.splitext(filename)
    output_path = os.path.join(dir_path, f"{name}_rotating_spline.gif")

    print(f"Creating GIF with {num_frames} frames")
    print(f"Frame duration: {frame_duration} seconds")
    print(f"Animation length: {animation_length:.2f} seconds")
    if hold_still > 0:
        print(f"Hold still duration: {hold_still:.2f} seconds")
        print(f"Total duration: {total_duration:.2f} seconds")
    print(f"Total rotation: {total_angle:.2f} degrees ({num_rotations:.2f} rotations)")

    # Get original image dimensions
    orig_width, orig_height = img.size

    # Generate frames
    for i, angle in enumerate(angles):
        # Create a clean transparent canvas for each frame
        canvas = Image.new('RGBA', (orig_width, orig_height), (0, 0, 0, 0))

        # Rotate image around center without expanding
        rotated_img = img.rotate(-angle, expand=False)  # Negative for clockwise rotation

        # Paste only the rotated image onto the clean canvas
        canvas.paste(rotated_img, (0, 0))
        frames.append(canvas)

        if (i + 1) % 20 == 0 or i == 0:
            velocity = slowdown_curve(times[i], animation_length)
            print(f"  Frame {i+1}/{num_frames}: {angle:.1f}° at t={times[i]:.2f}s (speed: {velocity:.1f}°/s)")

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


# Example slowdown curves

def exponential_slowdown(t, animation_length, initial_speed=720, decay_factor=3.0):
    """
    Exponential decay slowdown curve.

    Args:
        t (float): Time in seconds
        animation_length (float): Total animation length in seconds
        initial_speed (float): Initial rotation speed in degrees/second
        decay_factor (float): Controls how quickly it slows down (higher = faster decay)

    Returns:
        float: Rotation speed in degrees/second at time t
    """
    # Normalize decay by animation length so it works across different durations
    decay_rate = decay_factor / animation_length
    return initial_speed * math.exp(-decay_rate * t)


def exponential_slowdown_with_min(t, animation_length, initial_speed=720, decay_factor=3.0):
    """
    Exponential decay slowdown curve but don't run slower than a threshold.

    Args:
        t (float): Time in seconds
        animation_length (float): Total animation length in seconds
        initial_speed (float): Initial rotation speed in degrees/second
        decay_factor (float): Controls how quickly it slows down (higher = faster decay)

    Returns:
        float: Rotation speed in degrees/second at time t
    """
    # Normalize decay by animation length so it works across different durations
    decay_rate = decay_factor / animation_length
    res = initial_speed * math.exp(-decay_rate * t)
    threshold = 0.7 * animation_length
    if t > threshold:
        res = initial_speed * math.exp(-decay_rate * threshold)
    return res


def linear_slowdown(t, animation_length, initial_speed=720):
    """
    Linear slowdown curve - constant deceleration.

    Args:
        t (float): Time in seconds
        animation_length (float): Total animation length in seconds
        initial_speed (float): Initial rotation speed in degrees/second

    Returns:
        float: Rotation speed in degrees/second at time t
    """
    # Linear decrease from initial_speed to 0 over animation_length
    slowdown_rate = initial_speed / animation_length
    speed = initial_speed - slowdown_rate * t
    return max(speed, 0.0)


def quadratic_slowdown(t, animation_length, initial_speed=720):
    """
    Quadratic slowdown curve - accelerating deceleration.

    Args:
        t (float): Time in seconds
        animation_length (float): Total animation length in seconds
        initial_speed (float): Initial rotation speed in degrees/second

    Returns:
        float: Rotation speed in degrees/second at time t
    """
    # Normalize time to [0, 1]
    t_norm = t / animation_length
    # Quadratic decay: starts at 1, ends at 0
    factor = (1 - t_norm) ** 2
    return initial_speed * factor


def cosine_slowdown(t, animation_length, initial_speed=720):
    """
    Smooth cosine-based slowdown curve.

    Args:
        t (float): Time in seconds
        animation_length (float): Total animation length in seconds
        initial_speed (float): Initial rotation speed in degrees/second

    Returns:
        float: Rotation speed in degrees/second at time t
    """
    # Map time to [0, π] range over the animation length
    phase = min(t / animation_length, 1.0) * math.pi
    # Use (1 + cos(phase))/2 to get smooth decay from 1 to 0
    factor = (1 + math.cos(phase)) / 2
    return initial_speed * factor


def smooth_stop_slowdown(t, animation_length, initial_speed=1080):
    """
    Very smooth slowdown that comes to a gentle stop.
    Uses a sigmoid-like curve for natural deceleration.

    Args:
        t (float): Time in seconds
        animation_length (float): Total animation length in seconds
        initial_speed (float): Initial rotation speed in degrees/second

    Returns:
        float: Rotation speed in degrees/second at time t
    """
    # Normalize time to [0, 1]
    t_norm = t / animation_length
    # Smooth cubic easing: (1-t)^3
    factor = (1 - t_norm) ** 3
    return initial_speed * factor


def main():
    parser = argparse.ArgumentParser(
        description='Create a rotating GIF with custom slowdown curve from a PNG image',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available slowdown curves:
  exponential  - Exponential decay (smooth, natural deceleration)
  linear       - Linear slowdown (constant deceleration)
  quadratic    - Quadratic slowdown (accelerating deceleration)
  cosine       - Cosine-based slowdown (very smooth, natural)
  smooth_stop  - Very smooth stop with cubic easing

Examples:
  # Create 3-second animation with exponential slowdown
  %(prog)s logo.png -l 3.0 -c exponential -d 0.05

  # Fast spinning (5 rotations/sec initially) that slows over 4 seconds
  %(prog)s logo.png -l 4.0 -c smooth_stop -d 0.04 --initial-speed 1800

  # Linear slowdown over 2.5 seconds with 30fps, hold still for 1 second
  %(prog)s logo.png -l 2.5 -c linear -d 0.033 --initial-speed 900 --hold-still 1.0
        """)

    parser.add_argument('input_file', help='Path to the input PNG file')
    parser.add_argument('-l', '--length', type=float, required=True,
                       help='Total animation length in seconds')
    parser.add_argument('-d', '--duration', type=float, default=0.05,
                       help='Duration of each frame in seconds (default: 0.05)')
    parser.add_argument('-c', '--curve', type=str, default='exponential',
                       choices=['exponential', 'linear', 'quadratic', 'cosine', 'smooth_stop'],
                       help='Slowdown curve type (default: exponential)')
    parser.add_argument('--initial-speed', type=float, default=720,
                       help='Initial rotation speed in degrees/second (default: 720)')
    parser.add_argument('--decay-factor', type=float, default=3.0,
                       help='Decay factor for exponential curve (default: 3.0)')
    parser.add_argument('--hold-still', type=float, default=0.0,
                       help='Time in seconds to hold logo still at end before looping (default: 0.0)')

    args = parser.parse_args()

    # Select the slowdown curve based on user choice
    if args.curve == 'exponential':
        curve = lambda t, length: exponential_slowdown(t, length, args.initial_speed, args.decay_factor)
    elif args.curve == 'linear':
        curve = lambda t, length: linear_slowdown(t, length, args.initial_speed)
    elif args.curve == 'quadratic':
        curve = lambda t, length: quadratic_slowdown(t, length, args.initial_speed)
    elif args.curve == 'cosine':
        curve = lambda t, length: cosine_slowdown(t, length, args.initial_speed)
    elif args.curve == 'smooth_stop':
        curve = lambda t, length: smooth_stop_slowdown(t, length, args.initial_speed)

    create_rotating_gif_spline(args.input_file, curve, args.length, args.duration, args.hold_still)


if __name__ == "__main__":
    main()
