
# Imports
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ====================DRAWING HELPERS====================
def draw_text_with_outline(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, font: ImageFont.FreeTypeFont,
                            fill: str = 'black', outline: str = 'white', width: int = 2, anchor: str = 'mm') -> None:
    """
    Draw text with a thin outline for better contrast against busy backgrounds.

    :param draw: the ImageDraw object to draw onto
    :param x: the x coordinate to draw the text at
    :param y: the y coordinate to draw the text at
    :param text: the text string to draw
    :param font: the PIL font to draw the text with
    :param fill: the fill colour of the text
    :param outline: the colour of the outline drawn behind the text
    :param width: the outline thickness (in pixels)
    :param anchor: the PIL text anchor to align the text with
    :return: None
    """
    # Draw the outline by repeatedly drawing the text offset in every direction around the outline width
    for dx in range(-width, width + 1):
        for dy in range(-width, width + 1):
            if dx or dy:
                draw.text((x + dx, y + dy), text, font=font, fill=outline, anchor=anchor)

    # Draw the actual text on top of the outline
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)


def paste_with_outline(base: Image.Image, overlay: Image.Image, pos: tuple[int, int],
                        outline_color: tuple[int, int, int, int] = (255, 255, 255, 255), outline_size: int = 5) -> None:
    """
    Paste `overlay` onto `base` with an outline that follows the overlay's alpha channel (its shape).

    :param base: the base image to paste onto
    :param overlay: the RGBA image being pasted, whose alpha channel defines the outline shape
    :param pos: the (x, y) position to paste the overlay at
    :param outline_color: the RGBA colour of the outline
    :param outline_size: the outline thickness (in pixels)
    :return: None
    """
    # Grow the overlay's alpha channel outward to create the outline shape, then paste the outline before the overlay
    alpha = overlay.split()[3]
    outline = Image.new('RGBA', overlay.size, (255, 255, 255, 0))
    ImageDraw.Draw(outline).bitmap((0, 0), alpha.filter(ImageFilter.MaxFilter(outline_size)), fill=outline_color)
    base.paste(outline, pos, outline)
    base.paste(overlay, pos, overlay)


# ====================LOGO HELPERS====================
def load_and_fit_logo(path: str, max_w: int, max_h: int, slice_ratio: float = 0.26, y_offset: float = 0.0) -> Image.Image:
    """
    Load a logo image, crop a horizontal slice out of its vertical centre, and scale it to fit within
    (max_w, max_h) while preserving aspect ratio.

    :param path: the file path of the logo image to load
    :param max_w: the maximum width (in pixels) the logo can be scaled to
    :param max_h: the maximum height (in pixels) the logo can be scaled to
    :param slice_ratio: the height of the cropped slice, as a fraction of the source image's full height
    :param y_offset: shifts the crop window vertically, as a fraction of the source image's height (negative shifts
        the window up, toward the top of the image; positive shifts it down). Use this to bring a specific part of a
        logo into the slice
    :return logo: the cropped and scaled logo, as an RGBA image
    """
    img = Image.open(path).convert('RGBA')
    w, h = img.size

    # Crop a horizontal slice out of the image's vertical centre, shifted by y_offset
    slice_h = int(h * slice_ratio)
    upper = h // 2 - slice_h // 2 + int(y_offset * h)
    upper = max(0, min(upper, h - slice_h))
    lower = upper + slice_h
    img = img.crop((0, upper, w, lower))

    # Scale the slice to fit within the given bounds, preserving aspect ratio
    scale = min(max_w / img.width, max_h / img.height)
    new_size = (int(img.width * scale), int(img.height * scale))
    return img.resize(new_size, Image.LANCZOS)


def get_logo_slice(path: str, rect_w: int, rect_h: int, zoom: float) -> Image.Image:
    """
    Load a logo image, crop a centred slice matching the aspect ratio of a target rectangle, and scale it to fit
    inside that rectangle. Used to zoom into a logo rather than showing it in full.

    :param path: the file path of the logo image to load
    :param rect_w: the width (in pixels) of the target rectangle to fit the logo into
    :param rect_h: the height (in pixels) of the target rectangle to fit the logo into
    :param zoom: how far to zoom into the logo before fitting it (higher values crop in tighter)
    :return logo_slice: the cropped and scaled logo, as an RGBA image
    """
    logo = Image.open(path).convert('RGBA')

    # Crop a vertical slice out of the logo's centre
    slice_h = int(rect_h / zoom)
    slice_h = min(slice_h, logo.height)
    upper = logo.height // 2 - slice_h // 2
    lower = upper + slice_h
    logo_slice = logo.crop((0, upper, logo.width, lower))

    # Crop a horizontal slice out of the result, if the target rectangle's width requires it
    slice_w = int(rect_w / zoom)
    slice_w = min(slice_w, logo_slice.width)
    left = logo_slice.width // 2 - slice_w // 2
    right = left + slice_w
    logo_slice = logo_slice.crop((left, 0, right, slice_h))

    # Scale the slice to fit within the target rectangle, preserving aspect ratio
    scale = min(rect_w / logo_slice.width, rect_h / logo_slice.height)
    new_size = (int(logo_slice.width * scale), int(logo_slice.height * scale))
    return logo_slice.resize(new_size, Image.LANCZOS)
