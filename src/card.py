from PIL import Image, ImageDraw, ImageFont
import src.utils as utils
import yaml

BORDER_WIDTH = 4


class TroneDrawer(ImageDraw.ImageDraw):
    def __init__(self, image: Image.Image):
        super().__init__(image)
        origin = (0, 0)
        width = image.width
        height = image.height
        end = (width, height)

        # Draw the header
        self.rectangle(
            (origin, end),
            fill="green",
        )

        # Draw the body
        body_origin = (0, height * 0.1)
        self.rectangle(
            (body_origin, end),
            fill="blue",
        )

        # Add line between header and body
        self.line(
            (0, height * 0.1, width, height * 0.1),
            fill="black",
            width=BORDER_WIDTH,
        )

        # Draw the footer
        self.draw_footer(width, height)

        # Draw the borders
        self.rectangle(
            (origin, end),
            outline="black",
            width=BORDER_WIDTH,
        )

        self.line((0, height / 2, width, height / 2), fill="black")
        self.line((width / 2, 0, width / 2, height), fill="black")

    def draw_footer(self, width: int, height: int):
        # Ellipse constants
        x0 = width / 2
        y0 = height * 0.62
        r = 60

        # Other constants
        side_height = height * 0.75

        # Draw the footer text container
        self.polygon(
            [
                0,
                height,
                0,
                side_height,
                x0 - r,
                y0,
                x0 + r,
                y0,
                width,
                side_height,
                width,
                height,
            ],
            fill="red",
        )

        # Draw the sphere on top
        self.ellipse(
            (x0 - r, y0 - r, x0 + r, y0 + r),
            fill="yellow",
            outline="black",
            width=BORDER_WIDTH,
        )

        # Add lines arround the sphere
        self.line(
            (0, side_height, x0 - r, y0),
            fill="black",
            width=BORDER_WIDTH,
        )
        self.line(
            (x0 + r, y0, width, side_height),
            fill="black",
            width=BORDER_WIDTH,
        )


class LayoutProperties:
    def __init__(self, properties: dict):

        self.width_ratio = properties.get("width", 1)
        self.height_ratio = properties["height"]

        self.background_color = properties.get("background_color", "white")
        self.border_color = properties.get("border_color", "black")
        self.border_width = properties.get("border_width", 4)


class TextProperties:
    def __init__(self, properties: dict):
        self.font_type = properties["font"]
        self.font_size = properties["font_size"]
        self.x = properties["x"]
        self.y = properties["y"]
        self.font_color = properties.get("font_color", "black")
        self.align = properties.get("align", "center")
        self.keywords = properties.get("keywords", [])


class Card:

    def __init__(
        self,
        properties: dict,
    ) -> None:

        self.width = properties["width"]
        self.height = properties["height"]

        self.image = Image.new("RGBA", (self.width, self.height), "red")
        self.image_drawer = TroneDrawer(self.image)

    def add_image(
        self,
        image_path: str,
        position: tuple,
        thumbnail: bool = False,
        centered: bool = False,
    ):
        image = Image.open(image_path)
        if thumbnail:
            image.thumbnail((self.width, self.height))

        if centered:
            position = (
                position[0] - image.width // 2,
                position[1] - image.height // 2,
            )
        self.image.paste(
            image, position, image.split()[3] if image.mode == "RGBA" else None
        )

    def write(
        self,
        text: str,
        properties: TextProperties,
        h_center=True,
        v_center=True,
        add_new_lines: bool = False,
        keywords: list = None,
    ):
        font = ImageFont.truetype(properties.font_type, properties.font_size)
        if add_new_lines:
            text = utils.add_new_lines(self.width * 0.9, text, font)

        position = (properties.x * self.width, properties.y * self.height)

        _, _, w, h = self.image_drawer.textbbox((0, 0), text, font=font)
        if h_center:
            position = (position[0] - w // 2, position[1])
        if v_center:
            position = (position[0], position[1] - h // 2)

        self.image_drawer.text(
            position,
            text,
            font=font,
            fill=properties.font_color,
            align=properties.align,
        )

        # Underline specific keywords in the text
        if keywords:
            for keyword in keywords:
                start_idx = text.find(keyword)
                if start_idx != -1:
                    keyword_bbox = font.getbbox(keyword)
                    keyword_width = keyword_bbox[2] - keyword_bbox[0]
                    keyword_height = keyword_bbox[3] - keyword_bbox[1]
                    underline_start = (
                        position[0]
                        + self.image_drawer.textlength(text[:start_idx], font=font),
                        position[1] + keyword_height,
                    )
                    underline_end = (
                        underline_start[0] + keyword_width,
                        underline_start[1],
                    )
                    self.image_drawer.line(
                        [underline_start, underline_end],
                        fill=properties.font_color,
                        width=2,
                    )

    def save(self, path):
        self.image.save(path, "PNG", dpi=(300, 300))
        print("Image saved successfully!")
