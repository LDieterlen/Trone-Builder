from typing import List, Union
from PIL import Image
import math
import re
import yaml
from pathlib import Path


def load_image(file_path: Union[str, Path]) -> Image.Image:
    try:
        return Image.open(file_path).convert("RGBA")
    except Exception as e:
        raise ValueError(f"Could not load image from {file_path}: {e}")


def load_yaml_file(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def deep_merge(dict1: dict, dict2: dict) -> dict:
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            deep_merge(dict1[key], value)
        else:
            dict1[key] = value
    return dict1


def remove_html_tags(text):
    text = re.sub(r"<img[^>]*>", "XX", text)
    return re.sub(r"<[^>]*>", "", text)


def balance_list_weight(list_1: List[float], list_2: List[float]) -> bool:
    if not list_1 or not list_2:
        return False

    sum1 = sum(list_1)
    sum2 = sum(list_2)
    updated = False

    while len(list_1) > 1 and (sum1 - list_1[-1]) > sum2:
        moved = list_1.pop(-1)
        list_2.append(moved)
        sum1 -= moved
        sum2 += moved
        updated = True

    return updated


def balance_list(lists: List[List[float]]):
    if not lists or len(lists) < 2:
        return

    need_update = True
    while need_update:
        need_update = False
        for i in range(len(lists) - 1):
            updated = balance_list_weight(lists[i], lists[i + 1])
            need_update = need_update or updated


def smart_box_size(
    total_length,
    words_lenght,
    box_max_length,
):
    if total_length < box_max_length:
        return box_max_length

    nb_lines = 1
    balanced_lists = []
    current_line = []
    for word in words_lenght:
        if sum(current_line) + word > box_max_length:
            balanced_lists.append(current_line)
            current_line = [word]
            nb_lines += 1
        else:
            current_line.append(word)
    balanced_lists.append(current_line)

    balance_list(balanced_lists)
    max_word_length = math.ceil(max(sum(lst) for lst in balanced_lists))
    return max_word_length


def replace_keywords_with_icons(
    text,
    replacements,
    img_width=12,
    img_height=12,
):

    def replacer(match: re.Match):
        word = match.group(0)
        img_path = replacements[word]
        return f"<img src='{img_path}' width='{img_width}' height='{img_height}' valign='bottom'/>"

    pattern = r"\b(" + "|".join(map(re.escape, replacements.keys())) + r")\b"
    return re.sub(pattern, replacer, text)


def underline_keywords(text, replacements: list, end="(e?s?)"):
    for keyword in replacements:
        escaped_keyword = re.escape(keyword)
        pattern = re.compile(rf"\b{escaped_keyword}{end}\b", re.IGNORECASE)
        text = pattern.sub(lambda m: f"<u>{m.group(0)}</u>", text)
    return text


def bold_keywords(text, replacements, end="(e?s?)"):
    for keyword, style in replacements.items():
        pattern = re.compile(rf"\b{re.escape(keyword)}{end}\b")
        text = pattern.sub(f"<{style}>{keyword}</{style}>", text)
    return text


def resize_image(
    image: Image.Image,
    width: int,
    height: int,
    fit_method="crop",
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
