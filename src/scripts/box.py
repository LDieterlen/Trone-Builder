from abc import ABC
from enum import Enum
from typing import Optional
from scripts.coordinates import (
    Position,
    Dimension,
)
from pathlib import Path
from scripts import utils
from reportlab.lib.styles import ParagraphStyle


class Layer:
    def __init__(
        self,
        position: Position,
        dimension: Dimension,
        from_center: bool = True,
    ):
        self.dimension = dimension
        self.position = position

        if from_center:
            dx = dimension.width / 2
            dy = dimension.height / 2
            self.position.translate_by(-dx, -dy)

    @property
    def size(self):
        return (self.dimension.width, self.dimension.height)

    @property
    def center(self):
        return Position(
            self.position.x + self.dimension.width / 2,
            self.position.y + self.dimension.height / 2,
        )

    @property
    def width(self):
        return self.dimension.width

    @property
    def height(self):
        return self.dimension.height


class FitMethod(Enum):
    NONE = "none"
    CROP = "crop"
    THUMBNAIL = "thumbnail"
    RESIZE = "resize"


class ImageLayer(Layer):

    def __init__(
        self,
        position: Position,
        dim: Dimension,
        image_path: Path,
        from_center: bool = True,
    ):
        self.image = utils.load_image(image_path)
        super().__init__(position, dim, from_center)

    def resize(self, fit_method: FitMethod):
        image = self.image
        width = self.width
        height = self.height
        size = (width, height)

        if isinstance(fit_method, FitMethod):
            fit_method = fit_method.value

        if fit_method == "thumbnail":
            image.thumbnail(size)
        elif fit_method == "fill":
            image = image.resize(size)
        elif fit_method == "crop":
            img_ratio = image.width / image.height
            card_ratio = width / height

            if img_ratio > card_ratio:
                new_width = int(height * img_ratio)
                image = image.resize((new_width, height))

                left = (image.width - width) // 2
                image = image.crop((left, 0, left + width, height))
            else:
                new_height = int(width / img_ratio)
                image = image.resize((width, new_height))

                top = (image.height - height) // 2
                image = image.crop((0, top, width, top + height))

        self.image = image


class TextLayer(Layer):
    def __init__(
        self,
        position: Position,
        dim: Dimension,
        text: str,
        from_center: bool = True,
    ):
        self.text = text
        super().__init__(position, dim, from_center)

    # def add_text(
    #     self,
    #     text: str,
    #     x_offset_ratio: float,
    #     y_offset_ratio: float,
    #     style: ParagraphStyle,
    #     reverse=True,
    # ):
    #     if reverse:
    #         y_offset_ratio = 1 - y_offset_ratio

    #     font = style.fontName
    #     size = style.fontSize
    #     text_cleaned = remove_html_tags(text)

    #     # Find the longest word in the text
    #     words = text_cleaned.split()
    #     space_len = stringWidth(" ", font, size)
    #     words_length = [stringWidth(word, font, size) + space_len for word in words]
    #     total_length = sum(words_length)

    #     box_height = self.height_pt

    #     box_width = smart_box_size(
    #         total_length,
    #         words_length,
    #         self.width_pt * 0.95,
    #     )

    #     x_center = self.width_pt * x_offset_ratio
    #     y_center = self.height_pt * y_offset_ratio

    #     para = Paragraph(text, style)
    #     w, h = para.wrap(box_width, box_height)

    #     x = x_center - w / 2
    #     y = y_center - h / 2
    #     para.drawOn(
    #         self.canvas,
    #         x,
    #         y,
    #     )


class MainLayer(Layer):
    def __init__(self, width: float, height: float):
        super().__init__(
            Position(0, 0),
            Dimension(width, height),
            name="Main Layer",
            from_center=False,
        )
        self.children = []

    def add_layer(self, layer: Layer):
        if not isinstance(layer, Layer):
            raise TypeError("Layer must be an instance of Layer class")
        self.add_child(layer)
