import os
import json

from scripts.card import Card
from scripts.utils import bold_keywords, replace_keywords_with_icons, underline_keywords
import yaml
from scripts.constants import (
    TITLE_STYLE,
    COUNT_STYLE,
    POINTS_STYLE,
    EFFECT_TYPE_STYLE,
    EFFECT_STYLE,
    CARD_BOXES,
    ICONS_IN_TEXT,
    BOLDED_TEXT,
    UNDERLINED_KEYWORDS,
    LANGUAGE,
)


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


def build_faction(faction: str, faction_details: dict, language: str = "fr"):
    # Load properties of the faction
    card_layer_path: str = faction_details["card_layer_path"]
    image_base_path: str = faction_details["images_folder"]
    faction_path: str = faction_details["faction_path"]
    cards: dict = faction_details["cards"]

    # Create the output folder for the faction
    output_folder_path = f"output/{language}/{faction}/"
    os.makedirs(output_folder_path, exist_ok=True)

    # Building cards for each character
    for card_info in cards.values():
        name: str = card_info["name"]
        print(f"Building card for {name}...")
        card_template = Card()

        # Card background image
        card_background = image_base_path + card_info["image"].lower()
        card_template.add_image(
            card_background,
            CARD_BOXES["background"],
            h_location=card_info.get("h_location"),
        )

        # Card overlay
        card_template.add_image(
            card_layer_path, CARD_BOXES["card_overlay"], fit_method="fill"
        )

        # Card faction
        card_template.add_image(
            faction_path, CARD_BOXES["faction"], centered=True, fit_method="thumbnail"
        )

        # Card position icon
        position_icon_name = card_info["position"]
        position_icon_path = f"assets/sprites/positions/{position_icon_name}.png"
        card_template.add_image(
            position_icon_path,
            CARD_BOXES["position"],
            centered=True,
            fit_method="thumbnail",
        )

        # Convert the card to PDF to add html format text
        card_template.pdf_from_card()

        # Title
        card_template.add_text(
            name,
            x_offset_ratio=0.5,
            y_offset_ratio=0.045,
            style=TITLE_STYLE,
        )

        # Count
        count: str = card_info["count"]
        card_template.add_text(
            count,
            x_offset_ratio=0.83,
            y_offset_ratio=0.03,
            style=COUNT_STYLE,
        )

        # Points
        points: str = card_info["points"]
        card_template.add_text(
            points,
            x_offset_ratio=0.5,
            y_offset_ratio=0.58,
            style=POINTS_STYLE,
        )

        # Effect type
        effect_type: str = card_info["type"]
        card_template.add_text(
            effect_type,
            x_offset_ratio=0.5,
            y_offset_ratio=0.77,
            style=EFFECT_TYPE_STYLE,
        )

        # Effect
        effect: str = card_info["effect"]
        effect = replace_keywords_with_icons(effect, ICONS_IN_TEXT)
        effect = bold_keywords(effect, BOLDED_TEXT)
        effect = underline_keywords(effect, UNDERLINED_KEYWORDS)
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
        # Dump faction data to cards/data with appropriate name
        output_data_folder = "cards/data"
        os.makedirs(output_data_folder, exist_ok=True)
        faction_data_path = os.path.join(output_data_folder, f"{faction}.json")
        with open(
            faction_data_path.replace(".json", ".yaml"), "w", encoding="utf-8"
        ) as f:
            yaml.dump(faction_data, f, allow_unicode=True, sort_keys=False)
        print(faction_data)

        continue

        faction_name = faction_data["name"]
        print("-" * 40)
        print(f"Loaded data for faction: {faction_name}")
        print("-" * 40)

        build_faction(faction, faction_data)
