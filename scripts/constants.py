from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_CENTER

DPI = 300
WIDTH_PX = 744
HEIGHT_PX = 1039

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
