import math

# Card dimensions in pixels
CARD_WIDTH = 750
CARD_HEIGHT = 1050

BORDER_WIDTH = 10

LAYERS_LOCATIONS = {
    "core": (0, 0),
    "character": (0, math.floor(CARD_HEIGHT * 0.1)),
    "faction": (math.ceil(CARD_WIDTH * 0.071), math.ceil(CARD_HEIGHT * 0.05)),
    "position": (math.floor(CARD_WIDTH * 0.929), math.ceil(CARD_HEIGHT * 0.05)),
}


# Text configurations
class TextProperties:
    def __init__(self, x, y, font_size, color, font, align):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.color = color
        self.font = font
        self.align = align


# Text configurations
TITLE_CONFIG = TextProperties(
    x=0.5,
    y=0.05,
    font_size=48,
    color="black",
    font="font/Cinzel-Bold.ttf",
    align="center",
)

COUNT_CONFIG = TextProperties(
    x=0.83,
    y=0.015,
    font_size=36,
    color="black",
    font="font/Cinzel-ExtraBold.ttf",
    align="center",
)

SCORE_CONFIG = TextProperties(
    x=0.50,
    y=0.635,
    font_size=160,
    color="black",
    font="font/Cinzel-Bold.ttf",
    align="center",
)

EFFECT_TYPE_CONFIG = TextProperties(
    x=0.5,
    y=0.77,
    font_size=48,
    color="black",
    font="font/Cinzel-Bold.ttf",
    align="center",
)

EFFECT_CONFIG = TextProperties(
    x=0.5, y=0.88, font_size=60, color="black", font="Gabriola", align="center"
)

LEGEND_CONFIG = TextProperties(
    x=0.5, y=0.985, font_size=24, color="black", font="Gabriola", align="center"
)

TEXT_PROPERTIES = {
    "title": TITLE_CONFIG,
    "count": COUNT_CONFIG,
    "score": SCORE_CONFIG,
    "effect_type": EFFECT_TYPE_CONFIG,
    "effect": EFFECT_CONFIG,
    "legend": LEGEND_CONFIG,
}
