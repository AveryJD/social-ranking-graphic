
# Imports
from PIL import Image, ImageDraw, ImageFont
import os
from utils import get_logo_slice, paste_with_outline, draw_text_with_outline, load_and_fit_logo


# Set teams
DIVISION = "Pacific"
SUB_TITLE = "(Before the 2025-2026 season)"

ORDER = {
    "Vegas Golden Knights": "VGK",
    "Edmonton Oilers":   "EDM",
    "Vancouver Canucks": "VAN",
    "Seattle Kraken":    "SEA",
    "Los Angeles Kings": "LAK",
    "Anaheim Ducks":     "ANA",
    "Calgary Flames":    "CGY",
    "San Jose Sharks":   "SJS",
}

PLAYOFF_TEAMS = 3


TEAM_COLOURS = {
    "ANA": (252, 76, 2),   "ARI": (140, 38, 51),  "BOS": (252, 181, 20),
    "BUF": (0, 48, 135),   "CGY": (210, 0, 28),   "CAR": (206, 17, 38),
    "CHI": (207, 10, 44),  "COL": (111, 38, 61),  "CBJ": (0, 38, 84),
    "DAL": (0, 104, 71),   "DET": (206, 17, 38),  "EDM": (252, 76, 0),
    "FLA": (200, 16, 46),  "LAK": (162, 170, 173),"MIN": (2, 73, 48),
    "MTL": (175, 30, 45),  "NSH": (255, 184, 28), "NJD": (206, 17, 38),
    "NYI": (244, 125, 48), "NYR": (0, 56, 168),   "OTT": (218, 26, 50),
    "PHI": (247, 73, 2),   "PIT": (252, 181, 20), "SJS": (0, 109, 117),
    "SEA": (153, 217, 217),"STL": (0, 47, 135),   "TBL": (0, 40, 104),
    "TOR": (0, 32, 91),    "VAN": (0, 32, 91),    "UTA": (105, 179, 231),
    "VGK": (185, 151, 91), "WSH": (4, 30, 66),    "WPG": (4, 30, 66),
}

ASSETS = {
    "MAIN_FONT": os.path.join("assets", "fonts", "main.ttf"),
    "NHL_LOGO_DIR": os.path.join("assets", "nhl_logos"),
    "IMAGES_DIR": os.path.join("assets", "images"),
}


# Fonts
header_font   = ImageFont.truetype(ASSETS["MAIN_FONT"], 70)
title_font    = ImageFont.truetype(ASSETS["MAIN_FONT"], 75)
subtitle_font = ImageFont.truetype(ASSETS["MAIN_FONT"], 40)
team_font     = ImageFont.truetype(ASSETS["MAIN_FONT"], 100)


# Make graphic image
WIDTH, HEIGHT = 1080, 1360
img = Image.new("RGB", (WIDTH, HEIGHT), "white")
draw = ImageDraw.Draw(img)
center_x = WIDTH // 2


# Make header
HEADER_TOP = 20
HEADER_BOTTOM = 240
PADDING = 30
BORDER_WIDTH = 3
header_box = [PADDING, HEADER_TOP, WIDTH - PADDING, HEADER_BOTTOM]
draw.rectangle(header_box, fill="white", outline="black", width=BORDER_WIDTH)

# Add Logo
rect_w = WIDTH - 2 * PADDING - 2 * BORDER_WIDTH + 10
rect_h = HEADER_BOTTOM - HEADER_TOP - 2 * BORDER_WIDTH + 1
logo_path = os.path.join(ASSETS["IMAGES_DIR"], "analyticswithavery_logo.png")
logo_resized = get_logo_slice(logo_path, rect_w, rect_h, zoom=0.65)
offset_x = PADDING + BORDER_WIDTH + (rect_w - logo_resized.width) // 2 - 5
offset_y = HEADER_TOP + BORDER_WIDTH + (rect_h - logo_resized.height) // 2
paste_with_outline(img, logo_resized, (offset_x, offset_y))

# Add header text
draw_text_with_outline(draw, center_x, HEADER_TOP + 50, "Analytics With Avery", header_font)
draw_text_with_outline(draw, center_x, HEADER_TOP + 120, f"{DIVISION} Standings Prediction", title_font)
draw_text_with_outline(draw, center_x, HEADER_TOP + 180, SUB_TITLE, subtitle_font)


# Make team rows
Y_START = 250
ROW_H = 128
LINE_H = ROW_H + 10
PAD = 27
BORDER = 13


for i, (team, team_abreviation) in enumerate(ORDER.items(), 1):
    top = Y_START + (i - 1) * LINE_H
    bottom = top + ROW_H
    max_w = WIDTH - 2 * PAD
    max_h = int(ROW_H - BORDER) - 6

    # base rectangle
    color = TEAM_COLOURS.get(team_abreviation, (200, 200, 200))
    draw.rectangle([PAD, top, WIDTH - PAD, bottom],
                fill=color, outline="white", width=10)

    # second outline slightly inside, thinner
    if i <= PLAYOFF_TEAMS:
        inner_color = (0, 200, 0)
    else:
        inner_color = (200, 0, 0)

    draw.rectangle(
        [PAD + 3, top + 3, WIDTH - PAD - 3, bottom - 3],  # inset by a few pixels
        outline=inner_color,
        width=6
    )

    # Add team logo slice
    team_logo_path = os.path.join(ASSETS["NHL_LOGO_DIR"], f"{team_abreviation}.avif")
    team_logo = load_and_fit_logo(team_logo_path, max_w, max_h)
    offset = (PAD + (max_w - team_logo.width) // 2,
              top + (ROW_H - team_logo.height) // 2 + 1)
    paste_with_outline(img, team_logo, offset)

    # Add team name
    name_y = top + ROW_H - team_font.size // 2 - 10
    draw_text_with_outline(draw, center_x, name_y, team, team_font)


# Save graphic
graphic_name = DIVISION.lower().replace(' ', '_')
os.makedirs("graphics/standings", exist_ok=True)
img.save(f"graphics/standings/{graphic_name}.png")
