from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create base image sizes for macOS icon
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    
    # Create the base image (highest resolution)
    size = 1024
    background_color = "#2C3E50"  # Dark blue-gray
    text_color = "#ECF0F1"  # Light gray
    
    img = Image.new('RGB', (size, size), background_color)
    draw = ImageDraw.Draw(img)
    
    # Draw a simple "DL" text
    text = "DL"
    # Use a basic font since we can't assume any specific font is installed
    font_size = int(size * 0.5)  # 50% of icon size
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
        
    # Get text size
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center the text
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Draw the text
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Save as PNG
    if not os.path.exists('resources'):
        os.makedirs('resources')
        
    img.save('resources/icon.png')
    
    # Create .icns for macOS
    os.system(f'sips -s format icns resources/icon.png --out resources/icon.icns')

if __name__ == "__main__":
    create_icon()
