import yaml
import math
import pandas as pd
import sys
import os
import json
from src.card import Card, TextProperties


def build_cards(properties, data: pd.DataFrame, output_path):
    title_properties = TextProperties(properties["title"])
    count_properties = TextProperties(properties["count"])
    score_properties = TextProperties(properties["score"])
    effect_type_properties = TextProperties(properties["effect_type"])
    effect_properties = TextProperties(properties["effect"])
    legend_properties = TextProperties(properties["legend"])

    for index, row in data.iterrows():
        name = row["Name"]
        faction = row["Faction"]
        print(f"Building card {name} for {faction}")

        card = Card(properties)
        width = card.width
        height = card.height
        sprite_core = "sprites"
        faction_index = index % 8 + 1

        image_path = f"{sprite_core}/Images/{faction}/{faction_index}.png"
        if not os.path.exists(image_path):
            image_path = f"{sprite_core}/Images/default.png"
        card.add_image(image_path, (0, math.floor(height * 0.1)), True)

        card_model = f"{sprite_core}/Models/{faction}.png"
        card.add_image(card_model, (0, 0), True)

        faction_sprite = f"{sprite_core}/Factions/Large/{faction}.png"
        card.add_image(
            faction_sprite,
            (math.ceil(width * 0.071), math.ceil(height * 0.05)),
            True,
            centered=True,
        )

        locations = row["Location"].split(" ")
        for location in locations:
            position_sprite = f"{sprite_core}/Position/{location} LARGE.png"
            card.add_image(
                position_sprite,
                (math.floor(width * 0.929), math.ceil(height * 0.05)),
                True,
                centered=True,
            )

        card.write(name, title_properties)

        count = row["Count"]
        card.write(str(count), count_properties)

        score = row["Score"]
        card.write(str(score), score_properties)

        effect_type = row["Type"]
        card.write(effect_type, effect_type_properties)

        effect = row["Effect"]
        card.write(effect, effect_properties, add_new_lines=True)

        print(f"Building card {name} for {faction}")
        os.makedirs(f"{output_path}/{faction}", exist_ok=True)
        card.save(f"{output_path}/{faction}/{name}.png")


if __name__ == "__main__":

    properties = yaml.safe_load(open("properties.yaml"))

    os.makedirs("output", exist_ok=True)

    source_path = "sources/translation/"
    directories = [
        d
        for d in os.listdir(source_path)
        if os.path.isdir(os.path.join(source_path, d))
    ]
    print("Available translations:", ", ".join(directories))

    directories = ["fr"]

    for directory in directories:
        data = []

        for root, dirs, files in os.walk(f"{source_path}/{directory}"):
            for file in files:
                if file.endswith(".json"):
                    file_data = pd.read_json(f"{root}/{file}")
                    file_data["Faction"] = file.split(".")[0]
                    data.append(file_data)

        data = pd.concat(data)
        build_cards(properties, data, f"output/{directory}")