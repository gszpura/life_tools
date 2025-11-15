Various tools
============

## PDF Tools
* Tool for converting multiple images to PDF
  
-- example usage: **python3** to_pdf --path ~/data/ --resize 0.5 --rotate 90

## Logo Generation Tools

### 1. Generate Triangle Logos
Generate triangular logos with cream gradients:
```bash
python src/logos/logo.py
```

### 2. Add Text to Logos
Add text with various fonts and sizes to your logos:

**Basic usage:**
```bash
python src/logos/add_text_to_logo.py logo.png "Company Name"
```

**With specific parameters:**
```bash
# Fixed font and size
python src/logos/add_text_to_logo.py logo.png "Brand" --font "Roboto Slab" --size 250

# Light font weight
python src/logos/add_text_to_logo.py logo.png "Brand" --font "Roboto Slab Light" --size 280

# Custom margin between logo and text
python src/logos/add_text_to_logo.py logo.png "Brand" --font "Geist" --size 200 --margin 100

# Generate specific number of versions
python src/logos/add_text_to_logo.py logo.png "Brand" -n 50
```

### 3. Create Rotating GIFs
Create animated rotating GIFs from your logos:

```bash
# Basic rotation (30° steps, 0.1s frames)
python src/logos/create_rotating_gif.py logo.png

# Custom rotation and timing
python src/logos/create_rotating_gif.py logo.png -d 0.5 -s 45
```

### 4. Create Rotating GIFs with Slowdown
Create animated GIFs that spin fast and gradually slow down to a smooth stop with customizable deceleration curves:

```bash
python src/logos/create_rotating_gif_spline.py logo.png -l 3.0 -c smooth_stop --initial-speed 1440 --hold-still 0.5
```

### 5. Rotate Static Images
Generate multiple rotated versions of an image:

```bash
# Default 30° rotations (generates 12 images)
python src/logos/rotate_logo.py logo.png

# Custom rotation steps
python src/logos/rotate_logo.py logo.png -d 45
```

### 6. Convert Colors
Convert cream colors to custom target colors:

**Single image conversion:**
```bash
# Convert to brown (default)
python src/logos/convert_to_brown.py logo_final.png

# Convert to custom hex color
python src/logos/convert_to_brown.py logo_final.png -c "#654321"

# Custom output filename
python src/logos/convert_to_brown.py logo_final.png -c "#8B4513" -o logo_brown.png
```


GIF to MP4 conversion 
```
ffmpeg -i logo_rotation_into.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" logo_rotation_intro.mp4
```
