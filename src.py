
# Imports
from PIL import Image, ImageDraw, ImageFont
import os

TITLE = 'Offensive Forwards'

TOP_TEN = {
    'Connor McDavid' : 'EDM',
    'Nathan MacKinnon' : 'COL',
    'Nikita Kucherov' : 'TBL',
    'Leon Draisaitl' : 'EDM',
    'Auston Matthews' : 'TOR',
    'David Pastrnak' : 'BOS',
    'Kirill Kaprizov' : 'MIN',
    'Matthew Tkachuk' : 'FLA',
    'Jack Hughes' : 'NJD',
    'Sidney Crosby' : 'PIT',
}


# Paths
FONT_HEADER_PATH = os.path.join("assets", "fonts", "header.ttf")
FONT_BODY_PATH = os.path.join("assets", "fonts", "basic.ttf")
NHL_LOGO_DIR = os.path.join("assets", "nhl_logos")
IMAGES_DIR = os.path.join("assets", "images")

# Fonts
header_font = ImageFont.truetype(FONT_HEADER_PATH, 50)
title_font = ImageFont.truetype(FONT_HEADER_PATH, 75)
number_font = ImageFont.truetype(FONT_BODY_PATH, 100)
name_font = ImageFont.truetype(FONT_BODY_PATH, 60)

# Make graphic image
graphic_width, graphic_height = 1080, 1350
graphic_image = Image.new("RGB", (graphic_width, graphic_height), color="white")
draw = ImageDraw.Draw(graphic_image)

# Add Analytics With Avery Logo
my_logo = Image.open(os.path.join(IMAGES_DIR, "analyticswithavery_logo.png")).convert("RGBA")
my_logo.thumbnail((150, 150))
logo_x = graphic_width - my_logo.width - 10  # padding from right edge
logo_y = 0  # padding from top
graphic_image.paste(my_logo, (logo_x, logo_y), my_logo)

# Headers
left_margin = 60
draw.text((left_margin, 60), "Analytics With Avery Ranks", fill="black", font=header_font)
draw.text((left_margin, 140), f"Top 10 {TITLE}", fill="black", font=title_font)

# Top 10 player list
y_start = 260
line_height = 105
num_x = left_margin
logo_x = num_x + 110
name_x = logo_x + 150
logo_size = 120

for i, (player, team) in enumerate(TOP_TEN.items(), start=1):
    # vertical baseline for this row
    y = y_start + (i - 1) * line_height

    # Rank number
    draw.text((num_x, y), f"{i}", fill="black", font=number_font)

    # Team logo
    logo_path = os.path.join(NHL_LOGO_DIR, f"{team}.avif")
    team_logo = Image.open(logo_path).convert("RGBA")
    team_logo = team_logo.resize((logo_size, logo_size))

    logo_y = y + (number_font.size - logo_size) // 2
    graphic_image.paste(team_logo, (logo_x, logo_y), team_logo)

    # Player name
    name_y = y + (number_font.size - name_font.size) // 2
    draw.text((name_x, name_y), player, fill="black", font=name_font)

# Save graphic
graphic_image.save("graphics/top10_graphic.png")