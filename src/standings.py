
# Imports
from PIL import Image, ImageDraw, ImageFont
import os
import re
from utils import get_logo_slice, paste_with_outline, draw_text_with_outline, load_and_fit_logo
from constants import TEAM_COLOURS, TEAM_LOGO_Y_OFFSETS, PLAYOFF_GREEN, NO_PLAYOFF_RED
from lists import SEASON, PLAYOFF_ROWS, STANDINGS


ASSETS = {
    'MAIN_FONT': os.path.join('assets', 'fonts', 'main.ttf'),
    'NHL_LOGO_DIR': os.path.join('assets', 'nhl_logos'),
    'IMAGES_DIR': os.path.join('assets', 'images'),
}


def make_standings_graphic(division: str, teams: dict[str, str]) -> None:
    """
    Generate and save a social graphic predicting an 8 team standing rankings.

    :param division: the division name
    :param teams: a dictionary mapping each team's full name to its abbreviation
    :return: None
    """
    sub_title = f'(For the {SEASON} season)'
    division_label = division
    playoff_rows = PLAYOFF_ROWS.get(division, set())

    # Matches custom rank-range group names in STANDINGS
    rank_range_re = re.compile(r'^(\d+)-(\d+)$')

    # For custom rank range groups, label rows with their actual overall rank instead of just 1-8.
    rank_range_match = rank_range_re.match(division)
    start_rank = int(rank_range_match.group(1)) if rank_range_match else 1

    # Load fonts
    header_font = ImageFont.truetype(ASSETS['MAIN_FONT'], 70)
    title_font = ImageFont.truetype(ASSETS['MAIN_FONT'], 75)
    subtitle_font = ImageFont.truetype(ASSETS['MAIN_FONT'], 40)
    team_font = ImageFont.truetype(ASSETS['MAIN_FONT'], 90)

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
    draw_text_with_outline(draw, center_x, PADDING + 110, f'{division_label} Standings Prediction', title_font)
    draw_text_with_outline(draw, center_x, PADDING + 170, sub_title, subtitle_font)

    Y_START = 240
    GAP = 10
    PAD = 30
    TEAM_PAD = 20
    LOGO_PAD = -10
    OUTER_BORDER = 5
    INNER_BORDER = 2
    ROW_BORDER = OUTER_BORDER + INNER_BORDER
    LOGO_OUTLINE = 5

    num_teams = len(teams)
    ROW_H = (HEIGHT - PADDING - Y_START - (num_teams - 1) * GAP) / num_teams
    LINE_H = ROW_H + GAP

    # Add team rows
    for i, (team_name, team) in enumerate(teams.items(), 1):
        rank = start_rank + i - 1
        top = int(Y_START + (i - 1) * LINE_H)
        bottom = int(top + ROW_H)
        max_w = WIDTH - 2 * PAD
        max_h = int(ROW_H - 2 * ROW_BORDER) + 2

        # Add team color background (green border for playoffs, red otherwise)
        color = TEAM_COLOURS.get(team,)
        border_color = PLAYOFF_GREEN if i in playoff_rows else NO_PLAYOFF_RED
        draw.rectangle([PAD, top, WIDTH - PAD, bottom], fill=color, outline=border_color, width=OUTER_BORDER)

        # Add separating line between the playoff border and the fill colour
        draw.rectangle([PAD + OUTER_BORDER, top + OUTER_BORDER, WIDTH - PAD - OUTER_BORDER, bottom - OUTER_BORDER],
                        outline='white', width=INNER_BORDER)

        # Add team logo
        team_logo_path = os.path.join(ASSETS['NHL_LOGO_DIR'], f'{team}.avif')
        y_offset = TEAM_LOGO_Y_OFFSETS.get(team, 0.0)
        team_logo = load_and_fit_logo(team_logo_path, max_w, max_h, y_offset=y_offset)
        offset = (WIDTH - LOGO_PAD - ROW_BORDER - LOGO_OUTLINE - team_logo.width,
                  int(top + (ROW_H - team_logo.height) / 2 + 1))
        paste_with_outline(img, team_logo, offset)

        # Add team name
        name_y = int(top + ROW_H / 2)
        draw_text_with_outline(draw, PAD + TEAM_PAD, name_y, f'{rank}. {team_name}', team_font, anchor='lm')

    # Save graphic
    graphic_name = division.lower().replace(' ', '_')
    os.makedirs(f'graphics/{SEASON}/standings', exist_ok=True)
    img.save(f'graphics/{SEASON}/standings/{graphic_name}.png')


# Run standings graphic generation
if __name__ == '__main__':
    for division, teams in STANDINGS.items():
        make_standings_graphic(division, teams)
