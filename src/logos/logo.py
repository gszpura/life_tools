import svgwrite
import random
import math
import os
import colorsys


def generate_triangle_logo(output_dir="./logo_results", n=100):
    os.makedirs(output_dir, exist_ok=True)

    for i in range(n):
        # --- Random parameters ---
        size = 300
        stroke_width = random.uniform(1, 15)
        dot_radius = random.uniform(10, 35)

        # Cream base color with variance (convert HSL to RGB)
        def hsl_to_rgb(h, s, l):
            h = h / 360.0
            s = s / 100.0
            l = l / 100.0
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"

        # Cream colors with slight variations
        base_hue = random.uniform(35, 55)  # Yellow-orange range for cream
        base_saturation = random.uniform(15, 35)
        
        color1 = hsl_to_rgb(base_hue, base_saturation, random.uniform(85, 95))
        color2 = hsl_to_rgb(base_hue + random.uniform(-10, 10), 
                           base_saturation + random.uniform(-5, 5), 
                           random.uniform(75, 85))

        # --- Create SVG ---
        dwg = svgwrite.Drawing(f"{output_dir}/logo_{i:03d}.svg", size=(size, size))
        grad = dwg.linearGradient(start=(0, 0), end=(1, 1))
        grad.add_stop_color(0, color1)
        grad.add_stop_color(1, color2)
        dwg.defs.add(grad)

        # --- Triangle coordinates ---
        cx, cy = size / 2, size / 2
        r = size * 0.35
        points = [
            (cx + r * math.cos(math.radians(angle)), cy + r * math.sin(math.radians(angle)))
            for angle in [90, 210, 330]
        ]

        # --- Draw triangle edges only (no fill) ---
        dwg.add(dwg.polygon(points=points,
                            fill="none",
                            stroke=grad.get_paint_server(),
                            stroke_width=stroke_width))

        # --- Add dots at vertices ---
        for x, y in points:
            dwg.add(dwg.circle(center=(x, y), r=dot_radius, fill=grad.get_paint_server()))

        dwg.save()

    print(f"✅ Generated {n} logos in '{output_dir}'")


if __name__ == "__main__":
    generate_triangle_logo()
