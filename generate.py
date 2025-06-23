import yaml
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def relace_icons(
    text,
    replacements,
):

    def replacer(match: re.Match):
        word = match.group(0)
        img_path = replacements[word]
        return f"<img src='{img_path}' class='inline-logo'/>"

    pattern = r"\b(" + "|".join(map(re.escape, replacements.keys())) + r")\b"
    return re.sub(pattern, replacer, text)


def underline_keywords(text, replacements: list):
    for keyword in replacements:
        escaped_keyword = re.escape(keyword)
        pattern = re.compile(rf"\b{escaped_keyword}\b", re.IGNORECASE)
        text = pattern.sub(lambda m: f"<u>{m.group(0)}</u>", text)
    return text


def bold_keywords(text, replacements):
    for keyword in replacements:
        pattern = re.compile(re.escape(keyword))
        text = pattern.sub(f"<span class='effect-cinzel'>{keyword}</span>", text)
    return text


def format_effect(effect: str) -> str:
    effect = relace_icons(effect, ICONS)
    effect = underline_keywords(effect, KEYWORDS)
    effect = bold_keywords(effect, BOLDED)
    return effect


if __name__ == "__main__":

    # Reading common data file
    commun_data = yaml.safe_load(Path("cards/common.yaml").read_text(encoding="utf-8"))

    FACTION_DIR = Path(commun_data["faction_dir"])
    CARD_LAYER_DIR = Path(commun_data["cards_layers_dir"])
    IMAGES_DIR = Path(commun_data["images_dir"])

    POSITIONS = Path(commun_data["positions_dir"])
    ICONS: dict = commun_data["icons"]

    KEYWORDS: list = commun_data["keywords"]
    DEFAULT_IMAGE_PATH = commun_data["default_image_path"]
    DEFAULT_CARD_LAYER_PATH = commun_data["default_layer_path"]
    DEFAULT_FACTION_PATH = commun_data["default_faction_path"]

    extended_keywords = set(KEYWORDS)
    for kw in KEYWORDS:
        extended_keywords.add(kw + "e")
        extended_keywords.add(kw + "es")
        extended_keywords.add(kw + "s")
    KEYWORDS = list(extended_keywords)

    BOLDED: list = commun_data["bolded"]
    OUTPUT_DIR = Path("output")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Setting up Jinja2 environment
    yaml_dir = Path("cards/factions")
    template_path = Path("templates")
    output_base_dir = Path("output/")
    output_base_dir.mkdir(parents=True, exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(template_path)))
    template = env.get_template("card.html")

    # Loop on factions
    for yaml_path in yaml_dir.glob("*.yaml"):
        file_name = yaml_path.stem
        print(f"Processing {file_name}...")
        data: dict = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        faction_legend = data.get("legend", "")

        faction_name = data.get("faction_name", file_name)
        faction_path = FACTION_DIR / f"{faction_name}.png"
        if not faction_path.exists():
            faction_path = DEFAULT_FACTION_PATH
            # raise FileNotFoundError(f"Faction image not found: {faction_path}")

        card_layer_name = data.get("card_layer_name", file_name)
        card_layer_path = CARD_LAYER_DIR / f"{card_layer_name}.png"
        if not card_layer_path.exists():
            pass
            # raise FileNotFoundError(f"Card layer image not found: {card_layer_path}")

        faction_output_dir = output_base_dir / faction_name
        faction_output_dir.mkdir(parents=True, exist_ok=True)
        for card_key, card in data["cards"].items():
            print(f"\tProcessing card {card_key}...")
            # Character image
            character_image = card.get("image", card_key)
            character_image_path = IMAGES_DIR / faction_name / f"{character_image}.png"
            if not character_image_path.exists():
                character_image_path = DEFAULT_IMAGE_PATH
                # raise FileNotFoundError(
                #     f"Character image not found: {character_image_path}"
                # )

            # Card layer
            card_layer_name = card.get("card_layer_name", faction_name)
            card_layer_path = CARD_LAYER_DIR / f"{card_layer_name}.png"
            if not card_layer_path.exists():
                card_layer_path = DEFAULT_CARD_LAYER_PATH
                # raise FileNotFoundError(
                #     f"Card layer image not found: {card_layer_path}"
                # )

            # Position
            position = card["position"]
            position_path = POSITIONS / f"{position}.png"
            if not position_path.exists():
                raise FileNotFoundError(f"Position image not found: {position_path}")

            effect_type = card.get("type", "")
            if effect_type == "":
                effect = ""
                effect_typeA = card["typeA"]
                effectA = card["effectA"]
                effectA = format_effect(effectA)

                effect_typeB = card["typeB"]
                effectB = card["effectB"]
                effectB = format_effect(effectB)
            else:
                effect_typeA = ""
                effect_typeB = ""

                effectA = ""
                effectB = ""

                effect = card["effect"]
                effect = format_effect(effect)

            legend = ""
            write_legend = card.get("legend", False)
            if write_legend:
                legend = faction_legend

            legend = format_effect(legend)
            context = {
                "name": card["name"],
                "count": card["count"],
                "character_img": "../../" + str(character_image_path),
                "card_layer": "../../" + str(card_layer_path),
                "logo_faction": "../../" + str(faction_path),
                "position": "../../" + str(position_path),
                "type": effect_type.upper(),
                "point": card["points"],
                "effect": effect,
                "legend": legend,
                "typeA": effect_typeA.upper(),
                "effectA": effectA,
                "typeB": effect_typeB.upper(),
                "effectB": effectB,
            }

            output_file = faction_output_dir / f"{card_key}.html"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(template.render(**context))
