from typing import List
from PIL.ImageFont import FreeTypeFont, Image
import math
import re
import scripts.constant as C
import pytesseract


def add_new_lines(width: int, text: str, font: FreeTypeFont):
    text_lenght = font.getlength(text)
    line_count = 1 + (text_lenght // width)
    size_per_line = math.ceil(text_lenght / line_count)
    text_with_new_lines = ""
    current_text = ""
    for word in text.split(" "):
        lenght = font.getlength(current_text + word)
        if lenght <= size_per_line:
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
            replacement = f"  {current_pattern}  "
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
