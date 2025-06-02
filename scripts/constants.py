from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_CENTER

DPI = 300
WIDTH_PX = 744
HEIGHT_PX = 1039

LANGUAGE = "fr"

pdfmetrics.registerFont(
    TTFont(
        "Gabriola",
        "C:/Windows/Fonts/Gabriola.ttf",
    ),
)

pdfmetrics.registerFont(
    TTFont(
        "Simonetta",
        "assets/font/Simonetta/Simonetta-Regular.ttf",
    )
)

pdfmetrics.registerFont(
    TTFont(
        "Simonetta-Black",
        "assets/font/Simonetta/Simonetta-Black.ttf",
    )
)

pdfmetrics.registerFont(
    TTFont(
        "Cinzel-Bold",
        "assets/font/Cinzel-Bold.ttf",
    )
)

pdfmetrics.registerFont(
    TTFont(
        "Cinzel-ExtraBold",
        "assets/font/Cinzel-ExtraBold.ttf",
    )
)

pdfmetrics.registerFont(
    TTFont(
        "Roboto",
        "assets/font/Roboto/static/Roboto_SemiCondensed-Bold.ttf",
    )
)

EFFECT_STYLE = ParagraphStyle(
    name="EffectStyle",
    fontName="Simonetta",
    fontSize=12,
    textColor=black,
    alignment=TA_CENTER,
)

EFFECT_TYPE_STYLE = ParagraphStyle(
    name="EffectTypeStyle",
    fontName="Cinzel-ExtraBold",
    fontSize=10,
    textColor=black,
    alignment=TA_CENTER,
)

POINTS_STYLE = ParagraphStyle(
    name="PointsStyle",
    fontName="Cinzel-Bold",
    fontSize=38,
    textColor=black,
    alignment=TA_CENTER,
)

COUNT_STYLE = ParagraphStyle(
    name="CountStyle",
    fontName="Cinzel-Bold",
    fontSize=8,
    textColor=black,
    alignment=TA_CENTER,
)
TITLE_STYLE = ParagraphStyle(
    name="TitleStyle",
    fontName="Cinzel-Bold",
    fontSize=12,
    textColor=black,
    alignment=TA_CENTER,
)

CARD_BOXES = {
    "card_overlay": (0, 0),
    "background": (0, 0.05),
    "faction": (0.070, 0.051),
    "position": (0.930, 0.051),
}


UNDERLINED_KEYWORDS = [
    "allié",
    "confrère",
    "ennemi",
    "encouragé",
    "gel",
    "force",
    "protection",
]

ICON_BASE_PATH = "assets/sprites/"
FACTION_BASE_PATH = ICON_BASE_PATH + "factions/"
POSITION_BASE_PATH = ICON_BASE_PATH + "positions/"

ICONS_IN_TEXT = {
    "dead_fac": FACTION_BASE_PATH + "dead.png",
    "humans_fac": FACTION_BASE_PATH + "humans.png",
    "mages_fac": FACTION_BASE_PATH + "mages.png",
    "dwarf_fac": FACTION_BASE_PATH + "dwarf.png",
    "demons_fac": FACTION_BASE_PATH + "demons.png",
    "desert_fac": FACTION_BASE_PATH + "desert.png",
    "mountain_fac": FACTION_BASE_PATH + "mountain.png",
    "robots_fac": FACTION_BASE_PATH + "robots.png",
    "front_icon": POSITION_BASE_PATH + "front_i.png",
    "back_icon": POSITION_BASE_PATH + "back_i.png",
}

CINZEL_EXTRABOLD_STYLE = "font face='Cinzel-ExtraBold' size='10'"

BOLDED_TEXT = {
    "JOUÉ": CINZEL_EXTRABOLD_STYLE,
    "PERMANENT": CINZEL_EXTRABOLD_STYLE,
    "X": CINZEL_EXTRABOLD_STYLE,
}
