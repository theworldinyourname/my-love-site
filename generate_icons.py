
#!/usr/bin/env python3
"""
Generate PWA icons from a base image
Run this script to create all the required icon sizes for the PWA
"""

import os
from PIL import Image, ImageDraw

def create_icon(size, color_bg="#075e54", color_text="white"):
    """Create a simple icon with the app initial"""
    img = Image.new('RGB', (size, size), color_bg)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default
    try:
        from PIL import ImageFont
        font_size = int(size * 0.6)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            from PIL import ImageFont
            font_size = int(size * 0.6)
            font = ImageFont.load_default()
        except:
            font = None
    
    # Draw heart emoji or "L" for Love
    text = "💕"
    if font:
        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), text, fill=color_text, font=font)
    else:
        # Fallback: draw a simple heart shape
        draw.ellipse([size//4, size//3, 3*size//4, 2*size//3], fill=color_text)
    
    return img

def generate_all_icons():
    """Generate all required PWA icon sizes"""
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    icons_dir = "static/icons"
    
    # Create icons directory if it doesn't exist
    os.makedirs(icons_dir, exist_ok=True)
    
    for size in sizes:
        icon = create_icon(size)
        filename = f"icon-{size}x{size}.png"
        filepath = os.path.join(icons_dir, filename)
        icon.save(filepath, "PNG")
        print(f"Created {filename}")
    
    # Create screenshot placeholders
    # Wide screenshot (1280x720)
    wide_screenshot = Image.new('RGB', (1280, 720), "#075e54")
    draw = ImageDraw.Draw(wide_screenshot)
    try:
        from PIL import ImageFont
        font = ImageFont.load_default()
        draw.text((400, 300), "Love Chat App - Desktop View", fill="white", font=font)
    except:
        pass
    wide_screenshot.save(os.path.join(icons_dir, "screenshot-wide.png"))
    print("Created screenshot-wide.png")
    
    # Narrow screenshot (640x1136)
    narrow_screenshot = Image.new('RGB', (640, 1136), "#075e54")
    draw = ImageDraw.Draw(narrow_screenshot)
    try:
        from PIL import ImageFont
        font = ImageFont.load_default()
        draw.text((200, 500), "Love Chat App", fill="white", font=font)
        draw.text((220, 550), "Mobile View", fill="white", font=font)
    except:
        pass
    narrow_screenshot.save(os.path.join(icons_dir, "screenshot-narrow.png"))
    print("Created screenshot-narrow.png")
    
    print(f"\nAll PWA icons generated in {icons_dir}/")
    print("Your app is now ready to be installed as a PWA!")

if __name__ == "__main__":
    generate_all_icons()
