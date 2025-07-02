import pandas as pd
import yaml

from pathlib import Path


def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_cards_data():
    cards_dir = Path("cards/factions")
    cards_data = {}

    for yaml_file in cards_dir.glob("*.yaml"):
        faction_name = yaml_file.stem
        data = load_yaml(yaml_file)
        cards_data[faction_name] = data

    return cards_data


def cards_to_dataframe(cards_data):
    all_cards = []

    for faction, data in cards_data.items():
        for _, card_info in data.get("cards", {}).items():
            card_info = card_info.copy()  # Avoid mutating original
            card_info["faction"] = faction
            all_cards.append(card_info)

    df = pd.DataFrame(all_cards)
    # Desired column order
    columns = [
        "faction",
        "count",
        "name",
        "position",
        "points",
        "type",
        "effect",
        "typeA",
        "effectA",
        "typeB",
        "effectB",
    ]
    # Only keep columns that exist in the DataFrame
    columns = [col for col in columns if col in df.columns]
    df = df[columns]
    df = df.sort_values(by=["faction", "count", "name"], ascending=[True, False, True])
    return df


def main():
    cards_data = load_cards_data()
    cards_df = cards_to_dataframe(cards_data)

    # Save to CSV
    output_file = Path("cards/cards_data.csv")
    cards_df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Cards data saved to {output_file}")


if __name__ == "__main__":
    main()
