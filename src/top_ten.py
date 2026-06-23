
# Imports
from PIL import Image, ImageDraw, ImageFont
import os
from utils import get_logo_slice, paste_with_outline, draw_text_with_outline, load_and_fit_logo
from constants import SEASON, TOP_TENS, TEAM_COLOURS

ASSETS = {
    'MAIN_FONT': os.path.join('assets', 'fonts', 'main.ttf'),
    'NHL_LOGO_DIR': os.path.join('assets', 'nhl_logos'),
    'IMAGES_DIR': os.path.join('assets', 'images'),
}


def make_top_ten_graphic(title, top_ten):

    sub_title = f'(Before the {SEASON} season)'

    # Fonts
    header_font   = ImageFont.truetype(ASSETS['MAIN_FONT'], 70)
    title_font    = ImageFont.truetype(ASSETS['MAIN_FONT'], 85)
    subtitle_font = ImageFont.truetype(ASSETS['MAIN_FONT'], 40)
    name_font     = ImageFont.truetype(ASSETS['MAIN_FONT'], 100)

    # Make graphic image
    WIDTH, HEIGHT = 1080, 1360
    BACKKGROUND_COLOR = (19, 19, 19)
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    center_x = WIDTH // 2

    # Make header
    HEADER_TOP, HEADER_BOTTOM, PADDING = 20, 240, 30
    BORDER_WIDTH = 3

    # Add Analytics With Avery logo
    rect_w = WIDTH - 2 * PADDING - 2 * BORDER_WIDTH 
    rect_h = HEADER_BOTTOM - HEADER_TOP - BORDER_WIDTH
    logo_path = os.path.join(ASSETS['IMAGES_DIR'], 'analyticswithavery_logo.png')
    logo_resized = get_logo_slice(logo_path, rect_w, rect_h, zoom=0.65)
    offset_x = PADDING + BORDER_WIDTH + (rect_w - logo_resized.width) // 2
    offset_y = HEADER_TOP + BORDER_WIDTH + (rect_h - logo_resized.height) // 2
    paste_with_outline(img, logo_resized, (offset_x, offset_y))

    header_box = [PADDING, HEADER_TOP, WIDTH - PADDING, HEADER_BOTTOM]
    draw.rectangle(header_box, outline='white', width=BORDER_WIDTH)

    # Add header text
    draw_text_with_outline(draw, center_x, HEADER_TOP + 50, 'Analytics With Avery', header_font)
    draw_text_with_outline(draw, center_x, HEADER_TOP + 120, f'Top 10 {title}', title_font)
    draw_text_with_outline(draw, center_x, HEADER_TOP + 180, sub_title, subtitle_font)


    # Add player rows
    Y_START = 250
    ROW_H = 100
    LINE_H = 110
    PAD = 30
    BORDER = 5

    for i, (player, team) in enumerate(top_ten.items(), 1):
        top = Y_START + (i - 1) * LINE_H
        bottom = top + ROW_H
        max_w = WIDTH - 2 * PAD
        max_h = int(ROW_H - BORDER)

        # Row background
        color = TEAM_COLOURS.get(team, (200, 200, 200))
        draw.rectangle([PAD, top, WIDTH - PAD, bottom], fill=color, outline='white', width=3)

        # Team logo slice
        team_logo_path = os.path.join(ASSETS['NHL_LOGO_DIR'], f'{team}.avif')
        team_logo = load_and_fit_logo(team_logo_path, max_w, max_h)
        offset = (PAD + (max_w - team_logo.width) // 2,
                top + (ROW_H - team_logo.height) // 2 + 1)  # center vertically in row
        paste_with_outline(img, team_logo, offset)

        # Player name
        name_y = top + ROW_H - name_font.size // 2
        draw_text_with_outline(draw, center_x, name_y, player, name_font)


    # Save graphic
    graphic_name = title.lower().replace(' ', '_')
    os.makedirs(f'graphics/{SEASON}/top_ten', exist_ok=True)
    img.save(f'graphics/{SEASON}/top_ten/{graphic_name}.png')


if __name__ == "__main__":
    for title, top_ten in TOP_TENS.items():
        make_top_ten_graphic(title, top_ten)

