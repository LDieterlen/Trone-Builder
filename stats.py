import numpy as np
import matplotlib.pyplot as plt
import yaml
from pathlib import Path


def read_yaml_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


if __name__ == "__main__":
    yaml_dir = Path("cards/factions")

    # Compteurs globaux pour toutes les factions
    global_effects_types = {
        "IMMÉDIAT": 0,
        "PERMANENT": 0,
    }
    global_effects_types_unique = global_effects_types.copy()

    global_points_count = {
        "X": 0,
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
    }
    global_points_unique_count = global_points_count.copy()

    global_position_count = {
        "front": 0,
        "back": 0,
        "any": 0,
    }
    global_position_unique_count = global_position_count.copy()

    for yaml_path in yaml_dir.glob("*.yaml"):
        data = read_yaml_file(yaml_path)
        name: str = data["name"]
        cards: dict = data["cards"]

        effects_types = {"IMMÉDIAT": 0, "PERMANENT": 0}
        effects_types_unique = effects_types.copy()
        points_count = {k: 0 for k in global_points_count}
        points_unique_count = points_count.copy()
        position_count = {k: 0 for k in global_position_count}
        position_unique_count = position_count.copy()

        for card in cards.values():
            if (
                "count" not in card
                or "type" not in card
                or "points" not in card
                or "position" not in card
            ):
                continue
            card_count = int(card["count"])
            effects_types[card["type"]] += card_count
            effects_types_unique[card["type"]] += 1
            points_count[card["points"]] += card_count
            points_unique_count[card["points"]] += 1
            position_count[card["position"]] += card_count
            position_unique_count[card["position"]] += 1

        # Ajout aux compteurs globaux
        for k in global_effects_types:
            global_effects_types[k] += effects_types[k]
            global_effects_types_unique[k] += effects_types_unique[k]
        for k in global_points_count:
            global_points_count[k] += points_count[k]
            global_points_unique_count[k] += points_unique_count[k]
        for k in global_position_count:
            global_position_count[k] += position_count[k]
            global_position_unique_count[k] += position_unique_count[k]

        # Affichage des graphiques par faction
        plt.figure(figsize=(14, 10))

        # 1. Types d'effets (Total et Unique)
        plt.subplot(3, 1, 1)
        width = 0.35
        x = np.arange(len(effects_types))
        plt.bar(x - width / 2, list(effects_types.values()), width, label="Total")
        plt.bar(
            x + width / 2,
            list(effects_types_unique.values()),
            width,
            label="Unique",
            color="skyblue",
        )
        plt.title(f"Types d'effets - {name}")
        plt.ylabel("Nombre de cartes")
        plt.xticks(x, effects_types.keys(), rotation=0)
        plt.legend()

        # 2. Points (Total et Unique)
        plt.subplot(3, 1, 2)
        width = 0.35
        x = np.arange(len(points_count))
        plt.bar(
            x - width / 2,
            list(points_count.values()),
            width,
            label="Total",
            color="orange",
            alpha=0.7,
        )
        plt.bar(
            x + width / 2,
            list(points_unique_count.values()),
            width,
            label="Unique",
            color="gold",
            alpha=0.7,
        )
        plt.title(f"Points - {name}")
        plt.ylabel("Nombre de cartes")
        plt.xticks(x, points_count.keys(), rotation=0)
        plt.legend()

        # 3. Position (Total et Unique)
        plt.subplot(3, 1, 3)
        width = 0.35
        x = np.arange(len(position_count))
        plt.bar(
            x - width / 2,
            list(position_count.values()),
            width,
            label="Total",
            color="green",
            alpha=0.7,
        )
        plt.bar(
            x + width / 2,
            list(position_unique_count.values()),
            width,
            label="Unique",
            color="limegreen",
            alpha=0.7,
        )
        plt.title(f"Position - {name}")
        plt.ylabel("Nombre de cartes")
        plt.xlabel("Position")
        plt.xticks(x, position_count.keys(), rotation=0)
        plt.legend()

        plt.tight_layout()
        plt.show()

    # Affichage des graphiques globaux (overview)
    plt.figure(figsize=(14, 10))

    # 1. Types d'effets (Total and Unique)
    plt.subplot(3, 1, 1)
    width = 0.35
    x = np.arange(len(global_effects_types))
    plt.bar(x - width / 2, list(global_effects_types.values()), width, label="Total")
    plt.bar(
        x + width / 2,
        list(global_effects_types_unique.values()),
        width,
        label="Unique",
        color="skyblue",
    )
    plt.title("Types d'effets (toutes factions)")
    plt.ylabel("Nombre de cartes")
    plt.xticks(x, global_effects_types.keys(), rotation=0)
    plt.legend()

    # 2. Points (Total and Unique)
    plt.subplot(3, 1, 2)
    width = 0.35
    x = np.arange(len(global_points_count))
    plt.bar(
        x - width / 2,
        list(global_points_count.values()),
        width,
        label="Total",
        color="orange",
        alpha=0.7,
    )
    plt.bar(
        x + width / 2,
        list(global_points_unique_count.values()),
        width,
        label="Unique",
        color="gold",
        alpha=0.7,
    )
    plt.title("Points (toutes factions)")
    plt.ylabel("Nombre de cartes")
    plt.xticks(x, global_points_count.keys(), rotation=0)
    plt.legend()

    # 3. Position (Total and Unique)
    plt.subplot(3, 1, 3)
    width = 0.35
    x = np.arange(len(global_position_count))
    plt.bar(
        x - width / 2,
        list(global_position_count.values()),
        width,
        label="Total",
        color="green",
        alpha=0.7,
    )
    plt.bar(
        x + width / 2,
        list(global_position_unique_count.values()),
        width,
        label="Unique",
        color="limegreen",
        alpha=0.7,
    )
    plt.title("Position (toutes factions)")
    plt.ylabel("Nombre de cartes")
    plt.xlabel("Position")
    plt.xticks(x, global_position_count.keys(), rotation=0)
    plt.legend()

    plt.tight_layout()
    plt.show()
