import os

from scripts.factions import load_faction, Faction
from scripts.card import Card
from scripts.utils import bold_keywords, replace_keywords_with_icons, underline_keywords
from config import (
    load_fonts,
    TITLE_STYLE,
    COUNT_STYLE,
    POINTS_STYLE,
    EFFECT_TYPE_STYLE,
    EFFECT_STYLE,
    CARD_BOXES,
    BOLDED_TEXT,
    UNDERLINED_KEYWORDS,
    ASSETS_FOLDER,
    FONT_FOLDER,
    WIDTH_PX,
    HEIGHT_PX,
    DPI,
    POSITION_ICONS_FOLDER,
    OUTPUT_FOLDER,
    ICONS_IN_TEXT,
)
from scripts.box import BoxFactory, AbsoluteCoordinate, RelativeCoordinate
from scripts.box import Layer

LANGUAGE = "fr"
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


if __name__ == "__main__":
    card_box = BoxFactory.from_size(WIDTH_PX, HEIGHT_PX)
    print(f"Card box size: {card_box}")
    print(f"Card box width: {card_box.width}")

    header_box = BoxFactory.from_parent(
        card_box,
        RelativeCoordinate(0.5, 0.15),
        relative_height=0.25,
        relative_width=1.0,
        centered=True,
        color="blue",
    )
    print(f"Header box: {header_box}")
    print(f"Header box height: {header_box.height}")

    iehfg

    load_fonts(FONT_FOLDER)
    for faction_folder in ASSETS_FOLDER.glob("**/factions/*"):
        if faction_folder.is_dir():
            print(f"Found faction folder: {faction_folder.name}")
        faction: Faction = load_faction(faction_folder, LANGUAGE)
        valid, detail = faction.is_ready()
        if not valid:
            raise ValueError(f"Faction {faction.name} is not ready:\n{detail}")
        print(f"Faction {faction.name} is ready to build cards.")

        faction_icon = faction.icon
        faction_card_layer = faction.card_layer

        output_folder_path = f"{OUTPUT_FOLDER}/{LANGUAGE}/{faction}/"
        os.makedirs(output_folder_path, exist_ok=True)
        for characters in faction.characters:
            name: str = characters.name
            print(f"Building card for {name}...")
            card_template = Card(WIDTH_PX, HEIGHT_PX, DPI)

            # Background image
            character_image = characters.image
            card_template.add_image(
                character_image,
                CARD_BOXES["background"],
                h_location=characters.h_location,
            )

            # Card overlay
            card_template.add_image(
                faction_card_layer,
                CARD_BOXES["card_overlay"],
                fit_method="fill",
            )

            # Faction icon
            card_template.add_image(
                faction_icon,
                CARD_BOXES["faction"],
                centered=True,
                fit_method="thumbnail",
            )

            # Card position icon
            card_template.add_image(
                characters.position.to_image(POSITION_ICONS_FOLDER),
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
            count: str = str(characters.count)
            card_template.add_text(
                count,
                x_offset_ratio=0.83,
                y_offset_ratio=0.03,
                style=COUNT_STYLE,
            )

            # Points
            points: str = characters.points
            card_template.add_text(
                points,
                x_offset_ratio=0.5,
                y_offset_ratio=0.58,
                style=POINTS_STYLE,
            )

            # Effect type
            effect_type: str = characters.effect_type.translate(LANGUAGE)
            card_template.add_text(
                effect_type,
                x_offset_ratio=0.5,
                y_offset_ratio=0.77,
                style=EFFECT_TYPE_STYLE,
            )

            # Effect
            effect: str = characters.effect
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

    print("All cards have been built successfully.")
