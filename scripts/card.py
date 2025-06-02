from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas

from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
import io
import math
from scripts.utils import (
    resize_image,
    smart_box_size_old,
    smart_box_size,
    remove_html_tags,
)
from scripts.constants import (
    WIDTH_PX,
    HEIGHT_PX,
    DPI,
)
from pdf2image import convert_from_bytes


class Card:
    def __init__(self, path=None):

        self.width = WIDTH_PX
        self.height = HEIGHT_PX
        self.dpi = DPI

        self.width_pt = self.width * 72 / self.dpi
        self.height_pt = self.height * 72 / self.dpi

        self.card_buffer = io.BytesIO()
        self.pdf_buffer = io.BytesIO()

        if path:
            self.card = Image.open(path).convert("RGBA")
        else:
            self.card = Image.new("RGBA", (self.width, self.height), "red")
        self.drawer = ImageDraw.ImageDraw(self.card)

        self.canvas = canvas.Canvas(
            self.pdf_buffer, pagesize=(self.width_pt, self.height_pt)
        )

    def add_image(
        self,
        image_path: str,
        box: tuple,
        centered: bool = False,
        fit_method: str = "crop",
        h_location: float = None,
    ):
        image = Image.open(image_path)
        # Load the position of the image on the card
        layer_box = (math.floor(self.width * box[0]), math.floor(self.height * box[1]))
        if h_location is not None:
            layer_box = (layer_box[0], math.floor(self.height * h_location))

        image = resize_image(image, self.width, self.height, fit_method)

        if centered:
            layer_box = (
                layer_box[0] - image.width // 2,
                layer_box[1] - image.height // 2,
            )
        self.card.paste(
            image, layer_box, image.split()[3] if image.mode == "RGBA" else None
        )

    def pdf_from_card(self):
        self.card.save(self.card_buffer, format="PNG")
        self.card_buffer.seek(0)

        self.canvas.drawImage(
            ImageReader(self.card_buffer),
            0,
            0,
            width=self.width_pt,
            height=self.height_pt,
        )

    def card_from_pdf(self):
        self.canvas.save()
        pdf_bytes = self.pdf_buffer.getvalue()
        poppler_path = (
            "C:/Users/E115606/Documents/Perso/Programs/poppler-24.08.0/Library/bin"
        )

        self.card = convert_from_bytes(
            pdf_bytes, poppler_path=poppler_path, size=(self.width, self.height)
        )[0]

    def add_text(
        self,
        text,
        x_offset_ratio,
        y_offset_ratio,
        style: ParagraphStyle,
        reverse=True,
    ):
        if reverse:
            y_offset_ratio = 1 - y_offset_ratio

        font = style.fontName
        size = style.fontSize
        text_cleaned = remove_html_tags(text)

        # Find the longest word in the text
        words = text_cleaned.split()
        space_len = stringWidth(" ", font, size)
        words_length = [stringWidth(word, font, size) + space_len for word in words]
        total_length = sum(words_length)

        box_height = self.height_pt

        box_width = smart_box_size(
            total_length, words_length, self.width_pt * 0.95, words
        )

        x_center = self.width_pt * x_offset_ratio
        y_center = self.height_pt * y_offset_ratio

        para = Paragraph(text, style)
        w, h = para.wrap(box_width, box_height)

        x = x_center - w / 2
        y = y_center - h / 2
        para.drawOn(self.canvas, x, y)

    def save(self, path, format="PNG"):
        self.card.save(path, format, dpi=(self.dpi, self.dpi))
