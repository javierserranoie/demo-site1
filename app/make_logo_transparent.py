#!/usr/bin/env python3
"""Make logo white background transparent"""

try:
    from PIL import Image
    import sys
    
    input_file = "/home/js/Pictures/logos/logo004.png"
    output_file = "/home/js/workspace/personal/personal-site/app/logo004.png"
    
    # Open the image
    img = Image.open(input_file)
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Get image data
    data = img.getdata()
    
    # Create new image data with transparency
    new_data = []
    for item in data:
        r, g, b = item[0], item[1], item[2]
        # If pixel is white (or very close to white), make it transparent
        # Threshold: RGB values all above 240 (very light/white)
        if r > 240 and g > 240 and b > 240:
            # Make transparent
            new_data.append((255, 255, 255, 0))
        else:
            # Keep original pixel with alpha
            if len(item) == 4:
                new_data.append(item)
            else:
                new_data.append((r, g, b, 255))
    
    # Update image with new data
    img.putdata(new_data)
    
    # Save as PNG with transparency
    img.save(output_file, 'PNG')
    print(f"✓ Logo processed and saved to {output_file}")
    print("  White background replaced with transparency")
    
except ImportError:
    print("PIL/Pillow not available. Please install: pip install Pillow")
    print("Or manually process the logo using ImageMagick:")
    print(f"  convert {input_file} -transparent white {output_file}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    print(f"Please manually copy {input_file} to {output_file}")
    sys.exit(1)
