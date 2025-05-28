import re
import os
import json

from scripts.card import Card
from scripts.utils import (
    replace_keywords_with_bold,
    replace_keywords_with_icons,
)

from scripts.constants import (
    TITLE_STYLE,
    COUNT_STYLE,
    POINTS_STYLE,
    EFFECT_TYPE_STYLE,
    EFFECT_STYLE,
    LEGEND_STYLE,
    LEGEND_NAME_STYLE,
)


ICONS = {
    "dead_fac": "assets/sprites/factions/dead.png",
    "humans_fac": "assets/sprites/factions/humans.png",
    "mages_fac": "assets/sprites/factions/mages.png",
    "dwarf_fac": "assets/sprites/factions/dwarf.png",
    "demons_fac": "assets/sprites/factions/demons.png",
    "desert_fac": "assets/sprites/factions/desert.png",
    "mountain_fac": "assets/sprites/factions/mountain.png",
    "front_icon": "assets/sprites/positions/front_i.png",
    "back_icon": "assets/sprites/positions/back_i.png",
}

BOLD_TEXT = {
    "JOUÉ": "font face='Cinzel-ExtraBold' size='10'",
    "PERMANENT": "font face='Cinzel-ExtraBold' size='10'",
    "X": "font face='Cinzel-ExtraBold' size='10'",
}


FACTIONS = [
    "dwarf",
    "humans",
    "desert",
    "mages",
    "mountain",
    "demons",
    "dead",
    "robots",
]

LANGUAGE = "fr"

BOXES = {
    "card_overlay": (0, 0),
    "background": (0, 0.05),
    "faction": (0.070, 0.051),
    "position": (0.930, 0.051),
}


def deep_merge(dict1: dict, dict2: dict) -> dict:
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            deep_merge(dict1[key], value)
        else:
            dict1[key] = value
    return dict1


def load_data(file_name: str, language: str = "fr") -> dict:
    base_folder = "cards/base"
    localization_folder = f"cards/localization/{language}"

    # Load base data
    base_path = f"{base_folder}/{file_name}.json"
    with open(base_path, "r", encoding="utf-8") as f:
        base_data = json.load(f)

    # Load translation data
    translation_path = f"{localization_folder}/{file_name}.json"
    with open(translation_path, "r", encoding="utf-8") as f:
        translation_data = json.load(f)

    # Merge and return
    return deep_merge(base_data, translation_data)


def load_global_data(language: str = "fr") -> dict:
    return load_data("common", language)


def load_faction(faction_name: str, language: str = "fr") -> dict:
    return load_data(faction_name, language)


def extract_icon_name(text: str):
    """Extract the icon identifier from a position string in format {{icon:name}}"""
    match = re.search(r"{{icon:([^}]+)}}", text)
    if match:
        return match.group(1)
    return text


def build_faction(faction: str, faction_details: dict, language: str = "fr"):
    # Load properties of the faction

    card_layer_path = faction_details["card_layer_path"]
    image_base_path = faction_details["images_folder"]
    faction_path = faction_details["faction_path"]
    cards = faction_details["cards"]

    # Create the output folder for the faction
    output_folder_path = f"output/{language}/{faction}/"
    os.makedirs(output_folder_path, exist_ok=True)

    # Building cards for each character
    for character_id in cards:
        print(f"Building card for {character_id}...")
        card_template = Card()
        character_info = cards[character_id]

        character_image = image_base_path + character_info["image"].lower()

        # Handle position with the new format
        character_position = character_info["position"]
        position_icon_name = extract_icon_name(character_position)
        position_icon_path = f"assets/sprites/positions/{position_icon_name}.png"

        card_template.add_image(
            character_image,
            BOXES["background"],
            h_location=character_info.get("h_location"),
        )
        card_template.add_image(
            card_layer_path, BOXES["card_overlay"], fit_method="fill"
        )
        card_template.add_image(
            faction_path, BOXES["faction"], centered=True, fit_method="thumbnail"
        )
        card_template.add_image(
            position_icon_path,
            BOXES["position"],
            centered=True,
            fit_method="thumbnail",
        )

        card_template.pdf_from_card()

        # Title
        name: str = character_info["name"]
        count: str = character_info["count"]
        points: str = character_info["points"]
        effect_type: str = character_info["type"]

        effect: str = character_info["effect"]
        effect = replace_keywords_with_icons(effect, ICONS)
        effect = replace_keywords_with_bold(effect, BOLD_TEXT)

        # Title
        card_template.add_text(
            name,
            x_offset_ratio=0.5,
            y_offset_ratio=0.045,
            style=TITLE_STYLE,
        )
        # Count
        card_template.add_text(
            count,
            x_offset_ratio=0.83,
            y_offset_ratio=0.03,
            style=COUNT_STYLE,
        )
        # Points
        card_template.add_text(
            points,
            x_offset_ratio=0.5,
            y_offset_ratio=0.58,
            style=POINTS_STYLE,
        )

        # Effect type
        card_template.add_text(
            effect_type,
            x_offset_ratio=0.5,
            y_offset_ratio=0.77,
            style=EFFECT_TYPE_STYLE,
        )

        # Effect
        card_template.add_text(
            effect,
            x_offset_ratio=0.5,
            y_offset_ratio=0.88,
            style=EFFECT_STYLE,
        )

        saved_name = f"{count}-{name}.png"
        card_template.card_from_pdf()
        card_template.save(output_folder_path + saved_name)
        print("Done")


if __name__ == "__main__":

    for faction in FACTIONS:
        faction_data = load_faction(faction, LANGUAGE)

        faction_name = faction_data["name"]
        print(f"Loaded data for faction: {faction_name}")

        build_faction(faction, faction_data)
        # eogr
