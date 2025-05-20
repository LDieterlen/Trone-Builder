from PIL import Image, ImageDraw, ImageFont
import scripts.utils as utils
import scripts.constant as C
import pytesseract
import math


class CardTemplate:
    def __init__(self):
        self.width = C.CARD_WIDTH
        self.height = C.CARD_HEIGHT

        self.card = Image.new("RGBA", (self.width, self.height), "red")
        self.drawer = ImageDraw.ImageDraw(self.card)

    def add_image(
        self,
        image_path: str,
        identifier: str,
        centered: bool = False,
        fit_method: str = "crop",
        h_location: float = None,
    ):
        image = Image.open(image_path)
        # Load the position of the image on the card
        layer_location = C.LAYERS_LOCATIONS[identifier]
        if h_location is not None:
            layer_location = (layer_location[0], math.floor(self.height * h_location))
        # Resize the image
        if fit_method == "thumbnail":
            # Complete resizing while preserving aspect ratio
            image.thumbnail((self.width, self.height))
        elif fit_method == "fill":
            # Complete resizing without preserving aspect ratio
            image = image.resize((self.width, self.height))
        elif fit_method == "crop":
            # Resize the image proportionally then crop it to fill the frame
            img_ratio = image.width / image.height
            card_ratio = self.width / self.height

            if img_ratio > card_ratio:
                # Image wider than the frame
                new_width = int(self.height * img_ratio)
                image = image.resize((new_width, self.height))
                # Crop to center
                left = (image.width - self.width) // 2
                image = image.crop((left, 0, left + self.width, self.height))
            else:
                # Image taller than the frame
                new_height = int(self.width / img_ratio)
                image = image.resize((self.width, new_height))
                # Crop to center
                top = (image.height - self.height) // 2
                image = image.crop((0, top, self.width, top + self.height))

        if centered:
            layer_location = (
                layer_location[0] - image.width // 2,
                layer_location[1] - image.height // 2,
            )
        self.card.paste(
            image, layer_location, image.split()[3] if image.mode == "RGBA" else None
        )

    def add_text(
        self,
        text: str,
        identifier: str,
        h_center=True,
        v_center=True,
        auto_indentation: bool = False,
        keywords: list = None,
    ):
        properties = C.TEXT_PROPERTIES[identifier]

        font = ImageFont.truetype(properties.font, properties.font_size)
        if auto_indentation:
            text = utils.add_new_lines(self.width * 0.9, text, font)

        position = (properties.x * self.width, properties.y * self.height)

        _, _, w, h = self.drawer.textbbox((0, 0), text, font=font)
        if h_center:
            position = (position[0] - w // 2, position[1])
        if v_center:
            position = (position[0], position[1] - h // 2)

        self.drawer.text(
            position,
            text,
            font=font,
            fill=properties.color,
            align=properties.align,
            spacing=12,
        )
        # Underline specific keywords in the text
        if keywords:
            for keyword in keywords:
                start_idx = text.find(keyword)
                if start_idx != -1:
                    before_keyword = text[:start_idx]
                    lines = before_keyword.split("\n")
                    keyword_line_idx = len(lines) - 1
                    keyword_line_start = sum(len(line) + 1 for line in lines[:-1])
                    keyword_in_line_idx = start_idx - keyword_line_start
                    text_lines = text.split("\n")
                    # Position de départ de la ligne
                    line_y = position[1] + sum(
                        font.getbbox(line)[3] - font.getbbox(line)[1] + 12
                        for line in text_lines[:keyword_line_idx]
                    )
                    line_text = text_lines[keyword_line_idx]
                    prefix = line_text[:keyword_in_line_idx]
                    prefix_width = font.getlength(prefix)
                    keyword_bbox = font.getbbox(keyword)
                    keyword_width = keyword_bbox[2] - keyword_bbox[0]
                    keyword_height = keyword_bbox[3] - keyword_bbox[1]
                    # Correction align center
                    line_width = font.getlength(line_text)
                    x_offset = 0
                    if properties.align == "center":
                        x_offset = (w - line_width) / 2
                    underline_start = (
                        position[0] + x_offset + prefix_width,
                        line_y + keyword_height,
                    )
                    underline_end = (
                        underline_start[0] + keyword_width,
                        underline_start[1],
                    )
                    self.drawer.line(
                        [underline_start, underline_end],
                        fill=properties.color,
                        width=2,
                    )

    def insert_icons(self, icon_order: list):
        # pytesseract.pytesseract.tesseract_cmd = (
        #     r"C:\Users\E115606\AppData\Local\Programs\Tesseract-OCR\tesseract"
        # )

        boxes = pytesseract.image_to_data(
            self.card, output_type=pytesseract.Output.DICT
        )

        import re

        pattern = re.compile(r"><")

        pattern_count = 0
        for i, word in enumerate(boxes["text"]):
            if re.fullmatch(pattern, word):
                x = boxes["left"][i]
                y = boxes["top"][i]
                w = boxes["width"][i]
                h = boxes["height"][i]

                print("Icon found at:", x, y, w, h)
                icon = icon_order[pattern_count]
                max_size = max(w, h) + 15
                icon.thumbnail((max_size, max_size), Image.LANCZOS)

                # Calculate position to center the icon at (x,y)
                x_centered = x - (icon.width // 2) + (w // 2)
                y_centered = y - (icon.height // 2) + (h // 2) - 5

                self.card.paste(icon, (x_centered, y_centered), icon)

    def save(self, path):
        self.card.save(path, "PNG", dpi=(300, 300))
