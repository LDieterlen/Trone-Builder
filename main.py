import re
import os
import json
from scripts.card import CardTemplate

FACTIONS = [
    "humans",
]

LANGUAGE = "fr"


def replace_placeholders(text: str, data_dict: dict) -> str:
    # Traitement des placeholders de texte normaux
    def replace_text_match(match):
        key = match.group(1).strip()
        return str(data_dict.get(key, f"{{{{{key}}}}}"))

    text_pattern = r"\{\{([^}]+)\}\}"
    matches = re.finditer(text_pattern, text)
    match_positions = []

    for match in matches:
        key = match.group(1).strip()
        start_idx = match.start()
        end_idx = match.end()
        match_positions.append((key, start_idx, end_idx))

    print("Match positions:", match_positions)
    import sys

    sys.exit(0)
    text_result = re.sub(text_pattern, replace_text_match, text)

    # # Si on ne s'intéresse pas aux images, on retourne juste le texte
    # if image_dict is None:
    #     return text_result

    # Extraction des références d'images
    # image_matches = []
    # image_pattern = r"\[\[image:([^\]]+)\]\]"

    # def collect_image_match(match):
    #     key = match.group(1).strip()
    #     if key in image_dict:
    #         image_matches.append((match.group(0), image_dict[key]))
    #     return match.group(0)  # On garde le placeholder pour l'instant

    # re.sub(image_pattern, collect_image_match, text_result)

    # return (text_result, image_matches)


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
        character_position = character_info["position"]

        position_icon_path = f"assets/sprites/positions/{character_position}.png"

        card_template.add_image(character_image, "character", True)
        card_template.add_image(card_layer_path, "core", True)
        card_template.add_image(
            faction_path, "faction", True, centered=True, fit_method="thumbnail"
        )
        card_template.add_image(
            position_icon_path,
            "position",
            True,
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

        replace_placeholders()

        build_faction(global_data, faction_data)
