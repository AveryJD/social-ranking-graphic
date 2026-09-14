
# Imports
from PIL import Image, ImageDraw, ImageFont
import os
from utils import get_logo_slice, paste_with_outline, draw_text_with_outline, load_and_fit_logo
from constants import TEAM_COLOURS, TEAM_LOGO_Y_OFFSETS
from lists import SEASON, TOP_TENS


ASSETS = {
    'MAIN_FONT': os.path.join('assets', 'fonts', 'main.ttf'),
    'NHL_LOGO_DIR': os.path.join('assets', 'nhl_logos'),
    'IMAGES_DIR': os.path.join('assets', 'images'),
}


def make_top_ten_graphic(title: str, top_ten: dict[str, str]) -> None:
    """
    Generate and save a social graphic predicting a top ten ranking.

    :param title: the ranking's category name
    :param top_ten: a dictionary mapping each player's full name to their team abbreviation
    :return: None
    """
    sub_title = f'(Before the {SEASON} season)'

    # Load fonts
    header_font   = ImageFont.truetype(ASSETS['MAIN_FONT'], 70)
    title_font    = ImageFont.truetype(ASSETS['MAIN_FONT'], 85)
    subtitle_font = ImageFont.truetype(ASSETS['MAIN_FONT'], 40)
    name_font     = ImageFont.truetype(ASSETS['MAIN_FONT'], 90)

    # Make graphic image
    WIDTH, HEIGHT = 1080, 1360
    BACKGROUND_COLOR = (19, 19, 19)
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    center_x = WIDTH // 2

    # Make header
    PADDING = 30
    BORDER_WIDTH = 4
    HEADER_WIDTH = WIDTH - 2 * PADDING - 2 * BORDER_WIDTH
    HEADER_HEIGHT = 200

    # Add Analytics With Avery logo
    logo_path = os.path.join(ASSETS['IMAGES_DIR'], 'analyticswithavery_logo.png')
    logo_resized = get_logo_slice(logo_path, HEADER_WIDTH, HEADER_HEIGHT, zoom=0.65)
    offset_x = PADDING + ((WIDTH - 2 * PADDING) - logo_resized.width) // 2
    offset_y = PADDING + (HEADER_HEIGHT - logo_resized.height) // 2
    paste_with_outline(img, logo_resized, (offset_x, offset_y))

    header_box = [PADDING, PADDING, WIDTH - PADDING, PADDING + HEADER_HEIGHT]
    draw.rectangle(header_box, outline='white', width=BORDER_WIDTH)

    # Add header text
    draw_text_with_outline(draw, center_x, PADDING + 40, 'Analytics With Avery', header_font)
    draw_text_with_outline(draw, center_x, PADDING + 110, f'Top 10 {title}', title_font)
    draw_text_with_outline(draw, center_x, PADDING + 170, sub_title, subtitle_font)

    Y_START = 240
    ROW_H = 100
    LINE_H = 110
    PAD = 30
    ROW_BORDER = 4
    LOGO_OUTLINE = 5
    PLAYER_PAD = 20
    LOGO_PAD = -10

    # Add player rows
    for i, (player, team) in enumerate(top_ten.items(), 1):
        top = Y_START + (i - 1) * LINE_H
        bottom = top + ROW_H
        max_w = WIDTH - 2 * PAD
        max_h = int(ROW_H - 2 * ROW_BORDER) + 1

        # Add team color background
        color = TEAM_COLOURS.get(team, (200, 200, 200))
        draw.rectangle([PAD, top, WIDTH - PAD, bottom], fill=color, outline='white', width=ROW_BORDER)

        # Add team logo
        team_logo_path = os.path.join(ASSETS['NHL_LOGO_DIR'], f'{team}.avif')
        y_offset = TEAM_LOGO_Y_OFFSETS.get(team, 0.0)
        team_logo = load_and_fit_logo(team_logo_path, max_w, max_h, y_offset=y_offset)
        offset = (WIDTH - LOGO_PAD - ROW_BORDER - LOGO_OUTLINE - team_logo.width,
                  top + (ROW_H - team_logo.height) // 2 + 1)
        paste_with_outline(img, team_logo, offset)

        # Add player name
        if i < 10:
            player_text = f'{i}.  {player}'
        else:
            player_text = f'{i}. {player}'
        name_y = top + ROW_H // 2
        draw_text_with_outline(draw, PAD + PLAYER_PAD, name_y, player_text, name_font, anchor='lm')

    # Save graphic
    graphic_name = title.lower().replace(' ', '_')
    os.makedirs(f'graphics/{SEASON}/top_ten', exist_ok=True)
    img.save(f'graphics/{SEASON}/top_ten/{graphic_name}.png')


# Run top ten graphic generation
if __name__ == '__main__':
    for title, top_ten in TOP_TENS.items():
        make_top_ten_graphic(title, top_ten)
