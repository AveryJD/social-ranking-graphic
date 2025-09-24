

# Imports
from PIL import Image, ImageDraw, ImageFilter

def draw_text_with_outline(draw, x, y, text, font, fill="black",
                           outline="white", width=2, anchor="mm"):
    """Draw text with a thin outline for better contrast."""
    for dx in range(-width, width + 1):
        for dy in range(-width, width + 1):
            if dx or dy:
                draw.text((x + dx, y + dy), text, font=font,
                          fill=outline, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)


def paste_with_outline(base, overlay, pos, outline_color=(255, 255, 255, 255), outline_size=5):
    """Paste `overlay` onto `base` with an outline following alpha channel."""
    alpha = overlay.split()[3]
    outline = Image.new("RGBA", overlay.size, (255, 255, 255, 0))
    ImageDraw.Draw(outline).bitmap((0, 0),
                                   alpha.filter(ImageFilter.MaxFilter(outline_size)),
                                   fill=outline_color)
    base.paste(outline, pos, outline)
    base.paste(overlay, pos, overlay)

def load_and_fit_logo(path, max_w, max_h, slice_ratio=0.2):
    """
    Load an image, optionally crop a horizontal slice,
    and scale it to fit within (max_w, max_h) while preserving aspect ratio.
    Returns a RGBA image with alpha channel.
    """
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    slice_h = int(h * slice_ratio)
    upper = h // 2 - slice_h // 2
    lower = upper + slice_h
    img = img.crop((0, upper, w, lower))

    scale = min(max_w / img.width, max_h / img.height)
    new_size = (int(img.width * scale), int(img.height * scale))
    return img.resize(new_size, Image.LANCZOS)


def get_logo_slice(path, rect_w, rect_h, zoom=0.65):
    """
    Load logo, crop a centered horizontal slice, scale proportionally
    to fit inside a rectangle of size rect_w x rect_h.
    """
    logo = Image.open(path).convert("RGBA")

    # Crop vertical slice
    slice_h = int(rect_h / zoom)
    slice_h = min(slice_h, logo.height)
    upper = logo.height // 2 - slice_h // 2
    lower = upper + slice_h
    logo_slice = logo.crop((0, upper, logo.width, lower))

    # Crop horizontal slice if needed
    slice_w = int(rect_w / zoom)
    slice_w = min(slice_w, logo_slice.width)
    left = logo_slice.width // 2 - slice_w // 2
    right = left + slice_w
    logo_slice = logo_slice.crop((left, 0, right, slice_h))

    # Scale proportionally
    scale = min(rect_w / logo_slice.width, rect_h / logo_slice.height)
    new_size = (int(logo_slice.width * scale), int(logo_slice.height * scale))
    return logo_slice.resize(new_size, Image.LANCZOS)