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

**Available fonts:**
- Roboto, Roboto Condensed, Roboto Slab, Roboto Slab Light
- Open Sans, Montserrat, Lato
- Geist, Geist Mono, Clear Sans, Comfortaa
- Fira Code, JetBrains Mono, Cascadia Code
- Ubuntu, DejaVu Sans, Liberation Sans
- And many more...

### 3. Create Rotating GIFs
Create animated rotating GIFs from your logos:

```bash
# Basic rotation (30° steps, 0.1s frames)
python src/logos/create_rotating_gif.py logo.png

# Custom rotation and timing
python src/logos/create_rotating_gif.py logo.png -d 0.5 -s 45
```

### 4. Rotate Static Images
Generate multiple rotated versions of an image:

```bash
# Default 30° rotations (generates 12 images)
python src/logos/rotate_logo.py logo.png

# Custom rotation steps
python src/logos/rotate_logo.py logo.png -d 45
```

### 5. Convert Colors
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

**Batch directory conversion:**
```bash
# Convert all images in directory
python src/logos/convert_to_brown.py logo_folder/ -b -c "#5D4037"

# With custom output directory
python src/logos/convert_to_brown.py logo_folder/ -b -c "#704214" -o brown_logos/
```

**Popular color examples:**
- `#8B4513` - Saddle Brown
- `#654321` - Dark Brown
- `#704214` - Sepia
- `#5D4037` - Brown Grey
- `#800020` - Burgundy
- `#2F4F2F` - Dark Slate Gray


**STEPS**
In main dir:
- python src/logos/apply_gradient.py data/logo_wide.png logo_wide_creamy.png --main 230,227,219 --strength 0.1 
- python src/logos/apply_gradient.py data/logo_wide.png logo_wide_sepia.png --main 96,72,48 --strength 0.1 
- python src/logos/create_rotating_gif.py logo_wide_creamy.png -d 0.05 -s 5
- python src/logos/create_rotating_gif.py logo_wide_sepia.png -d 0.05 -s 5
- python src/logos/add_text_to_logo.py logo_wide_sepia.png "Lexero" -n 1 --font "Roboto Slab" --size 320 --margin 160 --color 99,74,49
- python src/logos/add_text_to_logo.py logo_wide_creamy.png "Lexero" -n 1 --font "Roboto Slab" --size 320 --margin 160
- cp files from subfolders and pack
