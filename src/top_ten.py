
# Imports
from PIL import Image, ImageDraw, ImageFont
import os
from utils import get_logo_slice, paste_with_outline, draw_text_with_outline, load_and_fit_logo


# Set players
TITLE = "Overall Defensemen"
SUB_TITLE = "(Before the 2025-2026 season)"

TOP_TEN = {
    "Cale Makar": "COL",
    "Quinn Hughes": "VAN",
    "Adam Fox": "NYR",
    "Rasmus Dahlin": "BUF",
    "Zach Werenski": "CBJ",
    "Miro Heiskanen": "DAL",
    "Evan Bouchard": "EDM",
    "Jaccob Slavin": "CAR",
    "Josh Morrissey": "WPG",
    "Roman Josi": "NSH",
}

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
title_font    = ImageFont.truetype(ASSETS["MAIN_FONT"], 85)
subtitle_font = ImageFont.truetype(ASSETS["MAIN_FONT"], 40)
name_font     = ImageFont.truetype(ASSETS["MAIN_FONT"], 100)


# Make graphic image
WIDTH, HEIGHT = 1080, 1360
img = Image.new("RGB", (WIDTH, HEIGHT), "white")
draw = ImageDraw.Draw(img)
center_x = WIDTH // 2


# Make header
HEADER_TOP, HEADER_BOTTOM, PADDING = 20, 240, 30
BORDER_WIDTH = 3
header_box = [PADDING, HEADER_TOP, WIDTH - PADDING, HEADER_BOTTOM]
draw.rectangle(header_box, fill="white", outline="black", width=BORDER_WIDTH)

# Add team logo
rect_w = WIDTH - 2 * PADDING - 2 * BORDER_WIDTH + 10
rect_h = HEADER_BOTTOM - HEADER_TOP - 2 * BORDER_WIDTH + 1
logo_path = os.path.join(ASSETS["IMAGES_DIR"], "analyticswithavery_logo.png")
logo_resized = get_logo_slice(logo_path, rect_w, rect_h, zoom=0.65)
offset_x = PADDING + BORDER_WIDTH + (rect_w - logo_resized.width) // 2 - 5
offset_y = HEADER_TOP + BORDER_WIDTH + (rect_h - logo_resized.height) // 2
paste_with_outline(img, logo_resized, (offset_x, offset_y))

# Add header text
draw_text_with_outline(draw, center_x, HEADER_TOP + 50, "Analytics With Avery", header_font)
draw_text_with_outline(draw, center_x, HEADER_TOP + 120, f"Top 10 {TITLE}", title_font)
draw_text_with_outline(draw, center_x, HEADER_TOP + 180, SUB_TITLE, subtitle_font)


# Add player rows
Y_START = 250
ROW_H = 100
LINE_H = 110
PAD = 30
BORDER = 5

for i, (player, team) in enumerate(TOP_TEN.items(), 1):
    top = Y_START + (i - 1) * LINE_H
    bottom = top + ROW_H
    max_w = WIDTH - 2 * PAD
    max_h = int(ROW_H - BORDER)

    # Row background
    color = TEAM_COLOURS.get(team, (200, 200, 200))
    draw.rectangle([PAD, top, WIDTH - PAD, bottom], fill=color, outline="black", width=3)

    # Team logo slice
    team_logo_path = os.path.join(ASSETS["NHL_LOGO_DIR"], f"{team}.avif")
    team_logo = load_and_fit_logo(team_logo_path, max_w, max_h)
    offset = (PAD + (max_w - team_logo.width) // 2,
              top + (ROW_H - team_logo.height) // 2 + 1)  # center vertically in row
    paste_with_outline(img, team_logo, offset)

    # Player name
    name_y = top + ROW_H - name_font.size // 2
    draw_text_with_outline(draw, center_x, name_y, player, name_font)


# Save graphic
graphic_name = TITLE.lower().replace(' ', '_')
os.makedirs("graphics/top_ten", exist_ok=True)
img.save(f"graphics/top_ten/{graphic_name}.png")
