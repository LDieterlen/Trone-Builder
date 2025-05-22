import re
import os
import json
from scripts.card import CardTemplate
from scripts.utils import (
    replace_text,
    replace_keywords,
    replace_icons,
)


FACTIONS = [
    # "dwarf",
    # "dead",
    # "demons",
    # "desert",
    "mages",
    # "mountain",
    # "humans",
]

LANGUAGE = "fr"


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


def build_faction(global_data: dict, faction_details: dict):
    # Load properties of the faction
    faction_name: str = faction_details["name"]
    card_layer_path = faction_details["card_layer_path"]
    image_base_path = faction_details["images_folder"]
    faction_path = faction_details["faction_path"]
    cards = faction_details["cards"]

    # Create the output folder for the faction
    output_folder_path = f"output/{faction_name}"
    os.makedirs(output_folder_path, exist_ok=True)

    # Building cards for each character
    for character_id in cards:
        print(f"Building card for {character_id}...")
        card_template = CardTemplate()
        character_info = cards[character_id]

        character_image = image_base_path + character_info["image"].lower()

        # Handle position with the new format
        character_position = character_info["position"]
        position_icon_name = extract_icon_name(character_position)
        position_icon_path = f"assets/sprites/positions/{position_icon_name}.png"

        card_template.add_image(
            character_image, "character", h_location=character_info.get("h_location")
        )
        card_template.add_image(card_layer_path, "core")
        card_template.add_image(
            faction_path, "faction", centered=True, fit_method="thumbnail"
        )
        card_template.add_image(
            position_icon_path,
            "position",
            centered=True,
            fit_method="thumbnail",
        )

        # Title
        name: str = character_info["name"]
        count: str = character_info["count"]
        points: str = character_info["points"]
        effect_type: str = character_info["type"]
        effect_type = replace_text(effect_type, global_data)

        effect: str = character_info["effect"]
        effect = replace_text(effect, global_data)
        effect, keywords, keyword_keys = replace_keywords(effect, global_data)
        effect, icons_order, icon_count = replace_icons(effect, global_data)

        # Tytle
        card_template.add_text(
            name.upper(),
            "title",
            h_center=True,
            v_center=True,
        )
        # Count
        card_template.add_text(
            count,
            "count",
            h_center=True,
            v_center=True,
        )
        # Points
        card_template.add_text(
            points,
            "points",
            h_center=True,
            v_center=True,
        )

        # Effect type
        card_template.add_text(
            effect_type,
            "effect_type",
            h_center=True,
            v_center=True,
        )

        # Effect
        card_template.add_text(
            effect,
            "effect",
            h_center=True,
            v_center=True,
            auto_indentation=True,
            keywords=keywords,
        )

        # Legend
        for i, key in enumerate(keyword_keys):
            legend_text = global_data["legends"][key]
            legend_text = f"{keywords[i].upper()} : {legend_text}"
            legend_text, legend_icons, icon_count = replace_icons(
                legend_text, global_data, icon_count
            )
            icons_order = {**icons_order, **legend_icons}
            card_template.add_text(
                legend_text,
                "legend",
                h_center=True,
                v_center=True,
            )

        card_template.insert_icons(icons_order)
        card_template.save(output_folder_path + f"/{name}.png")
        print(f"Card for {name} created successfully.")


if __name__ == "__main__":

    global_data = load_global_data(LANGUAGE)
    for faction in FACTIONS:
        faction_data = load_faction(faction, LANGUAGE)

        faction_name = faction_data["name"]
        print(f"Loaded data for faction: {faction_name}")

        build_faction(global_data, faction_data)
