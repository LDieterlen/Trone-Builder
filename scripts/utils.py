from typing import List
from PIL.ImageFont import FreeTypeFont, Image
import math
import re
import scripts.constants as C
import pytesseract


def remove_html_tags(text):
    return re.sub(r"<[^>]*>", "", text)


def smart_box_size(text_lenght, box_min_lenght, box_max_length):
    if text_lenght < box_max_length:
        return box_max_length

    nb_lines = math.ceil(text_lenght / box_max_length)
    line_size = text_lenght / nb_lines

    return max(box_min_lenght, line_size)


def replace_keywords_with_icons(text, replacements, img_width=12, img_height=12):

    def replacer(match: re.Match):
        word = match.group(0)
        img_path = replacements[word]
        return f"<img src='{img_path}' width='{img_width}' height='{img_height}' valign='bottom'/>"

    # Construire l'expression régulière pour tous les mots-clés
    pattern = r"\b(" + "|".join(map(re.escape, replacements.keys())) + r")\b"
    return re.sub(pattern, replacer, text)


def replace_keywords_with_bold(text, replacements):
    """Remplace les mots-clés par du texte enrichi."""
    for keyword, style in replacements.items():
        # Utiliser une expression régulière pour trouver le mot entier
        pattern = re.compile(rf"\b{re.escape(keyword)}\b")
        text = pattern.sub(f"<{style}>{keyword}</{style}>", text)
    return text


def resize_image(
    image: Image.Image, width: int, height: int, fit_method="crop"
) -> Image.Image:
    # Resize the image
    if fit_method == "thumbnail":
        # Complete resizing while preserving aspect ratio
        image.thumbnail((width, height))
    elif fit_method == "fill":
        # Complete resizing without preserving aspect ratio
        image = image.resize((width, height))
    elif fit_method == "crop":
        # Resize the image proportionally then crop it to fill the frame
        img_ratio = image.width / image.height
        card_ratio = width / height

        if img_ratio > card_ratio:
            # Image wider than the frame
            new_width = int(height * img_ratio)
            image = image.resize((new_width, height))
            # Crop to center
            left = (image.width - width) // 2
            image = image.crop((left, 0, left + width, height))
        else:
            # Image taller than the frame
            new_height = int(width / img_ratio)
            image = image.resize((width, new_height))
            # Crop to center
            top = (image.height - height) // 2
            image = image.crop((0, top, width, top + height))
    return image


def add_new_lines(width: int, text: str, font: FreeTypeFont):
    text_lenght = font.getlength(text)
    line_count = 1 + (text_lenght // width)
    size_per_line = math.ceil(text_lenght / line_count)
    text_with_new_lines = ""
    current_text = ""
    splited_text = text.split(" ")
    forbidden_start = [
        ",",
        ".",
        "!",
        "?",
        ";",
        ":",
        "-",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
    ]
    for i, word in enumerate(splited_text):
        forbidden_new_line = False
        next_word = ""
        if i + 1 < len(splited_text):
            next_word = splited_text[i + 1]
        if next_word in forbidden_start:
            forbidden_new_line = True

        lenght = font.getlength(current_text + word)
        trailling_text_length = font.getlength(" ".join(splited_text[i + 1 :]))

        if lenght + trailling_text_length <= size_per_line * 1.1:
            forbidden_new_line = True
        if lenght <= size_per_line or forbidden_new_line:
            current_text += word + " "
        else:
            if lenght < width:
                current_text += word
                text_with_new_lines += current_text + "\n"
                current_text = ""
            else:
                text_with_new_lines += current_text + "\n"
                current_text = word + " "
    text_with_new_lines += current_text
    return text_with_new_lines


def replace_icons(text: str, global_data: dict, count=0) -> str:
    processed_text = text

    # Only handle {{text:key}} format
    pattern = r"{{icon:([^}]+)}}"

    patterns_to_find = {}
    # Find and process each match
    for match in re.finditer(pattern, processed_text):
        key = match.group(1)
        keyword = match.group(0)

        # Text replacement
        if key in global_data.get("icon", {}):
            current_pattern = C.PATTERNS[count]
            replacement = f"{current_pattern}"
            icon_path = global_data["icon"][key]
            patterns_to_find[current_pattern] = icon_path

            processed_text = processed_text.replace(keyword, replacement, 1)
            count += 1
    return processed_text, patterns_to_find, count


def replace_text(text: str, global_data: dict) -> str:
    processed_text = text

    # Only handle {{text:key}} format
    pattern = r"{{text:([^}]+)}}"
    # Find and process each match
    for match in re.finditer(pattern, processed_text):
        key = match.group(1)
        keyword = match.group(0)

        # Text replacement
        if key in global_data.get("text", {}):
            replacement = global_data["text"][key]
            processed_text = processed_text.replace(keyword, replacement, 1)
    return processed_text


def replace_keywords(text: str, global_data: dict) -> str:
    processed_text = text

    pattern = r"{{keyword:([^}]+)}}"
    keywords = []
    keywords_keys = []
    # Find and process each match
    for match in re.finditer(pattern, processed_text):
        key = match.group(1)
        keyword = match.group(0)

        # Text replacement
        if key in global_data.get("keyword", {}):
            replacement = global_data["keyword"][key]
            keywords.append(replacement)
            keywords_keys.append(key)
            processed_text = processed_text.replace(keyword, replacement, 1)
    return processed_text, keywords, keywords_keys


def find_patterns_in_image(image: Image.Image, patterns: List[str]) -> List[tuple]:
    """
    Find the bounding boxes of given regex patterns in an image using pytesseract.
    Returns a list of (x, y, w, h) tuples for each pattern in order.
    Raises ValueError if any pattern is not found.
    """
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Users\E115606\AppData\Local\Programs\Tesseract-OCR\tesseract"
    )
    boxes = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT,
        lang="eng",
        config="--psm 6",
    )
    results = []
    for idx, pattern in enumerate(patterns):
        found = False
        for j, word in enumerate(boxes["text"]):
            if re.fullmatch(pattern, word):
                x = boxes["left"][j]
                y = boxes["top"][j]
                w = boxes["width"][j]
                h = boxes["height"][j]
                results.append((x, y, w, h))
                found = True
                break
        if not found:
            raise ValueError(
                f"Pattern '{pattern}' not found in image. Found {len(results)} out of {idx + 1}."
            )
    return results
