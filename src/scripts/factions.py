from dataclasses import dataclass
from typing import List
from PIL.Image import Image
from scripts import utils
from pathlib import Path
from enum import Enum, auto


class EffectType(Enum):
    PLAY = auto()
    PERMANENT = auto()

    def translate(self, language: str = "fr", upper=True) -> str:
        translations = {
            "fr": {"PLAY": "Joué", "PERMANENT": "Permanent"},
            "en": {"PLAY": "Play", "PERMANENT": "Permanent"},
        }
        tranlation = translations.get(language, {}).get(self.name, "Unknown")
        if upper:
            tranlation = tranlation.upper()
        return tranlation


class CharacterPosition(Enum):
    FRONT = auto()
    BACK = auto()
    ANY = auto()

    def to_image(self, base_path: str) -> Image:
        position_images = {
            "FRONT": "front.png",
            "BACK": "back.png",
            "ANY": "any.png",
        }
        image_path = Path(base_path) / position_images[self.name]
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        return image_path


@dataclass
class Character:
    name: str
    faction: str
    points: str
    effect: str
    effect_type: EffectType
    position: CharacterPosition
    count: int
    image_path: Path
    image: Image
    h_location: float = None

    def __post_init__(self):
        self.count = int(self.count)
        self.effect_type = EffectType[self.effect_type]
        self.image = utils.load_image(self.image_path)
        self.position = CharacterPosition[self.position.upper()]


class Faction:
    def __init__(
        self,
        name: str,
        icon: Image,
        card_layer: Image,
        characters: List[Character] = [],
    ):
        self.name: str = name
        self.icon: Image = icon
        self.card_layer: Image = card_layer
        self.characters: List[Character] = characters

    def add_character(self, character: Character):
        self.characters.append(character)

    def is_ready(self):
        name_ok = self.name is not None
        icon_ok = isinstance(self.icon, Image)
        card_layer_ok = isinstance(self.card_layer, Image)
        characters_ok = isinstance(self.characters, list) and len(self.characters) > 0
        character_count_ok = sum(character.count for character in self.characters) == 16
        ok = (
            name_ok
            and icon_ok
            and card_layer_ok
            and characters_ok
            and character_count_ok
        )

        details = {
            "Name": name_ok,
            "Icon": icon_ok,
            "Card Layer": card_layer_ok,
            "Characters": characters_ok,
            "Character Count": character_count_ok,
        }

        return (ok, details)

    def __repr__(self):
        return f"Faction(name={self.name}, characters={len(self.characters)})"


def load_faction(path: Path, language: str = "fr"):
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    root_path: Path = path

    data_path: Path = root_path / "data"
    base_data_file = data_path / "data.yaml"
    if not base_data_file.exists():
        raise FileNotFoundError(f"Base data file not found: {base_data_file}")

    base_data = utils.load_yaml_file(base_data_file)

    translation_file = data_path / f"{language}" / "data.yaml"
    if not translation_file.exists():
        raise FileNotFoundError(f"Translation file not found: {translation_file}")

    transalation_data = utils.load_yaml_file(translation_file)
    faction_data = utils.deep_merge(base_data, transalation_data)
    faction_name = faction_data["name"]

    sprites_path = root_path / "sprites"
    faction_icon_file = sprites_path / "faction_icon.png"
    if not faction_icon_file.exists():
        raise FileNotFoundError(f"Faction icon file not found: {faction_icon_file}")
    faction_icon = utils.load_image(faction_icon_file)
    card_layer_file = sprites_path / "card_layer.png"
    if not card_layer_file.exists():
        raise FileNotFoundError(f"Card layer file not found: {card_layer_file}")
    card_layer = utils.load_image(card_layer_file)
    images_path = root_path / "images"
    faction = Faction(faction_name, faction_icon, card_layer)
    for character_data in faction_data["cards"].values():
        image_path: Path = images_path / character_data["image"]
        if not image_path.exists():
            raise FileNotFoundError(f"Character image file not found: {image_path}")

        character = Character(
            name=character_data["name"],
            faction=faction_name,
            points=character_data["points"],
            effect=character_data["effect"],
            effect_type=character_data["type"],
            position=character_data["position"],
            count=character_data["count"],
            image_path=image_path,
        )
        faction.add_character(character)
    if not faction.is_ready():
        raise ValueError(
            f"Faction {faction_name} is not ready. Missing characters or assets."
        )
    return faction
