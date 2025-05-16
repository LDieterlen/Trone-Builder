from PIL import Image, ImageDraw, ImageFont
import scripts.utils as utils
import scripts.constant as C


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
    ):
        image = Image.open(image_path)
        # Load the position of the image on the card
        layer_location = C.LAYERS_LOCATIONS[identifier]

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

    def add_text_with_icons(
        self,
        text: str,
        identifier: str,
        h_center=True,
        v_center=True,
        auto_indentation: bool = False,
        icons_info: list = None,
        global_data: dict = None,
    ):
        """
        Add text with embedded icons to the card.
        
        Args:
            text: Text to add
            identifier: Identifier for text properties
            h_center: Whether to horizontally center the text
            v_center: Whether to vertically center the text
            auto_indentation: Whether to add line breaks automatically
            icons_info: List of tuples (icon_path, position) for icons to embed in text
            global_data: Global data for keywords
        """
        try:
            properties = C.TEXT_PROPERTIES[identifier]
        except KeyError:
            raise ValueError(
                f"Invalid identifier: {identifier}. Valid identifiers are: {list(C.TEXT_PROPERTIES.keys())}"
            )

        font = ImageFont.truetype(properties.font, properties.font_size)

        # Apply auto-indentation if needed
        if auto_indentation:
            text = utils.add_new_lines(self.width * 0.9, text, font)

        position = (properties.x * self.width, properties.y * self.height)

        # Adjust position for centering
        _, _, w, h = self.drawer.textbbox((0, 0), text, font=font)
        if h_center:
            position = (position[0] - w // 2, position[1])
        if v_center:
            position = (position[0], position[1] - h // 2)

        # Draw the text
        self.drawer.text(
            position,
            text,
            font=font,
            fill=properties.color,
            align=properties.align,
        )

        # Add icons if provided
        if icons_info and len(icons_info) > 0:
            font_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
            icon_size = int(font_height * 1.2)  # Make the icon slightly larger than text height
            
            for icon_path, pos_in_text in icons_info:
                # Calculate icon position based on text position and position in text
                lines = text[:pos_in_text].split('\n')
                line_number = len(lines) - 1
                pos_in_line = len(lines[-1])
                
                icon_x = position[0] + self.drawer.textlength(lines[-1][:pos_in_line], font=font)
                icon_y = position[1] + line_number * font_height
                
                # Load and resize icon
                try:
                    icon = Image.open(icon_path)
                    icon.thumbnail((icon_size, icon_size))
                    # Center the icon vertically with the text line
                    icon_y = icon_y - (icon.height - font_height) // 2
                    
                    # Paste the icon
                    self.card.paste(
                        icon, 
                        (int(icon_x), int(icon_y)), 
                        icon.split()[3] if icon.mode == "RGBA" else None
                    )
                except Exception as e:
                    print(f"Error embedding icon {icon_path}: {e}")

    def add_text(
        self,
        text: str,
        identifier: str,
        h_center=True,
        v_center=True,
        auto_indentation: bool = False,
        keywords: list = None,
        global_data: dict = None,
    ):
        """Original add_text method for backwards compatibility"""
        # If global_data is provided, process keywords
        if global_data:
            processed_text, icons_info = utils.process_keywords(text, global_data)
            return self.add_text_with_icons(
                processed_text, 
                identifier, 
                h_center, 
                v_center, 
                auto_indentation, 
                icons_info, 
                global_data
            )

        try:
            properties = C.TEXT_PROPERTIES[identifier]
        except KeyError:
            raise ValueError(
                f"Invalid identifier: {identifier}. Valid identifiers are: {list(C.TEXT_PROPERTIES.keys())}"
            )

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
                        + self.drawer.textlength(text[:start_idx], font=font),
                        position[1] + keyword_height,
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

    def save(self, path):
        self.card.save(path, "PNG", dpi=(300, 300))
