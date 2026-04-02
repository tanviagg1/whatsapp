import os
from PIL import Image, ImageDraw, ImageFont

IMAGES_DIR = "images"


def add_hello_text(image_path, output_path):
    """Add 'Hello' in red to the center of the image."""
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    width, height = img.size

    # Try to use a system font, fall back to default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=80)
    except Exception:
        font = ImageFont.load_default()

    text = "Hello"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) / 2
    y = (height - text_height) / 2

    # Draw shadow for readability
    draw.text((x + 2, y + 2), text, font=font, fill="black")
    # Draw red text
    draw.text((x, y), text, font=font, fill="red")

    img.save(output_path)
    print(f"Edited image saved: {output_path}")
    return output_path


def edit_all_images(image_paths):
    """Add 'Hello' text to all images and return edited paths."""
    edited_paths = []
    for i, path in enumerate(image_paths):
        output_path = os.path.join(IMAGES_DIR, f"edited_{i + 1}.jpg")
        edit_all = add_hello_text(path, output_path)
        edited_paths.append(edit_all)
    return edited_paths


if __name__ == "__main__":
    paths = [os.path.join(IMAGES_DIR, f"lily_{i}.jpg") for i in range(1, 4)]
    edit_all_images(paths)
