
# ====================TEAM LOGO CROP OFFSETS====================
# Per-team vertical crop adjustment for the logo slice
TEAM_LOGO_Y_OFFSETS = {
    # Atlantic
    'BOS': 0.0,    'BUF': -0.13,  'DET': 0.0,   'FLA': 0.0,
    'MTL': 0.0,    'OTT': 0.05,   'TBL': 0.0,   'TOR': 0.09,
    # Metropolitan
    'CAR': 0.0,    'CBJ': 0.0,    'NJD': 0.0,   'NYI': -0.13,
    'NYR': 0.05,   'PHI': 0.0,    'PIT': -0.2,  'WSH': 0.0,
    # Central
    'CHI': 0.0,    'COL': 0.0,    'DAL': 0.0,   'MIN': -0.05,
    'NSH': -0.05,  'STL': 0.0,    'UTA': 0.0,   'WPG': 0.0,
    # Pacific
    'ANA': -0.02,  'CGY': 0.0,    'EDM': 0.04,  'LAK': -0.19,
    'SEA': -0.1,   'SJS': 0.1,    'VAN': -0.1,  'VGK': 0.0,
}


# ====================TEAM COLOURS====================
# Maps each team abbreviation to its primary colour
TEAM_COLOURS = {
    # Atlantic
    'BOS': (252, 181, 20), 'BUF': (0, 48, 135),   'DET': (206, 17, 38),  'FLA': (200, 16, 46),
    'MTL': (175, 30, 45),  'OTT': (218, 26, 50),  'TBL': (0, 40, 104),   'TOR': (0, 32, 91),
    # Metropolitan
    'CAR': (206, 17, 38),  'CBJ': (0, 38, 84),    'NJD': (206, 17, 38),  'NYI': (244, 125, 48),
    'NYR': (0, 56, 168),   'PHI': (247, 73, 2),   'PIT': (252, 181, 20), 'WSH': (4, 30, 66),
    # Central
    'CHI': (207, 10, 44),  'COL': (111, 38, 61),  'DAL': (0, 104, 71),   'MIN': (2, 73, 48),
    'NSH': (255, 184, 28), 'STL': (0, 47, 135),   'UTA': (105, 179, 231),'WPG': (4, 30, 66),
    # Pacific
    'ANA': (252, 76, 2),   'CGY': (210, 0, 28),   'EDM': (252, 76, 0),   'LAK': (162, 170, 173),
    'SEA': (153, 217, 217),'SJS': (0, 109, 117),  'VAN': (0, 32, 91),    'VGK': (185, 151, 91),
}

# Green colour for playoff teams
PLAYOFF_GREEN = (0, 200, 0)

# Red colour for non playoff teams
NO_PLAYOFF_RED = (200, 0, 0)

# Colours for trophy placements
RANK_COLOURS = {
    1: (255, 215, 0),
    2: (192, 192, 192),
    3: (205, 127, 50),
    4: (64, 64, 64),
    5: (64, 64, 64),
}