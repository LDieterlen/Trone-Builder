import re
import os
import json
import scripts.utils
from scripts.card import CardTemplate

FACTIONS = [
    "humans",
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
    match = re.search(r'{{icon:([^}]+)}}', text)
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
        card_template = CardTemplate()
        character_info = cards[character_id]

        character_image = image_base_path + character_info["image"]
        
        # Handle position with the new format
        character_position = character_info["position"]
        position_icon_name = extract_icon_name(character_position)
        position_icon_path = f"assets/sprites/positions/{position_icon_name}.png"

        card_template.add_image(character_image, "character")
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
        effect: str = character_info["effect"]

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
        
        # Process effect_type with keywords
        card_template.add_text(
            effect_type, 
            "effect_type",
            h_center=True,
            v_center=True,
            global_data=global_data,
        )
        
        # Process effect with keywords
        # First process keywords, then do auto-indentation
        processed_effect, icons_info = scripts.utils.process_keywords(effect, global_data)
        card_template.add_text_with_icons(
            processed_effect,
            "effect",
            h_center=True,
            v_center=True,
            auto_indentation=True,
            icons_info=icons_info,
            global_data=global_data,
        )
        
        # Legend
        card_template.add_text(
            "HOW TO DO THIS ?",
            "legend",
            h_center=True,
            v_center=True,
        )

        card_template.save(output_folder_path + f"/{name}.png")
        print(f"Card for {name} created successfully.")


if __name__ == "__main__":

    global_data = load_global_data(LANGUAGE)
    for faction in FACTIONS:
        faction_data = load_faction(faction, LANGUAGE)

        faction_name = faction_data["name"]
        print(f"Loaded data for faction: {faction_name}")

        build_faction(global_data, faction_data)
