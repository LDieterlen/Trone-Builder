from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_CENTER


ROOT_FOLDER = Path(__file__).parent.parent

ASSETS_FOLDER = ROOT_FOLDER / "assets"
COMMUN_ASSETS = ASSETS_FOLDER / "commun"
FONT_FOLDER = COMMUN_ASSETS / "fonts"
COMMUN_ICONS_FOLDER = COMMUN_ASSETS / "icons"
ICONS_IN_TEXT_FOLDER = COMMUN_ICONS_FOLDER / "in_text"
POSITION_ICONS_FOLDER = COMMUN_ICONS_FOLDER / "positions"

OUTPUT_FOLDER = ROOT_FOLDER / "output"

DPI = 300
WIDTH_PX = 744
HEIGHT_PX = 1039

ICONS_IN_TEXT = {
    "front_icon": ICONS_IN_TEXT_FOLDER / "front_i.png",
    "back_icon": ICONS_IN_TEXT_FOLDER / "back_i.png",
}

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

CINZEL_EXTRABOLD_STYLE = "font face='Cinzel-ExtraBold' size='10'"

BOLDED_TEXT = {
    "JOUÉ": CINZEL_EXTRABOLD_STYLE,
    "PERMANENT": CINZEL_EXTRABOLD_STYLE,
    "X": CINZEL_EXTRABOLD_STYLE,
}


def load_fonts(font_folder: Path, debug: bool = False) -> str:
    font_paths = list(font_folder.glob("**/*.ttf"))
    print(f"Found {len(font_paths)} font files...", end=" ")

    font_names = []
    for font_path in font_paths:
        if debug:
            print(f"Loading font: {font_path.stem}...")
        pdfmetrics.registerFont(TTFont(font_path.stem, str(font_path)))
        font_names.append(font_path.stem)
    print("loaded.")


EFFECT_STYLE = ParagraphStyle(
    name="EffectStyle",
    fontName="Simonetta-Regular",
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
