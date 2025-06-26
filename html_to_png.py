import os
import time
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from pathlib import Path


INPUT_DIR = "output"
OUTPUT_DIR = "png_output"

CARDS_NAMES = [
    # none,
]

FACTIONS_NAMES = [
    # name,
]

FACTIONS_EXCLUDED = [
    # "faction_name",
]


def capture_fixed_card(html_path, output_path, width=744, height=1040, wait_time=2):
    options = Options()
    # Utilisation de la nouvelle syntaxe headless pour Chrome récent
    options.add_argument("--headless=new")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--force-device-scale-factor=1")  # augmente qualité
    options.add_argument(
        f"--window-size={width+500},{height + 500}"
    )  # + espace en hauteur si scroll

    driver = webdriver.Chrome(options=options)
    driver.get("file://" + os.path.abspath(html_path))
    time.sleep(wait_time)

    png = driver.get_screenshot_as_png()
    driver.quit()

    X = 239  # work
    # X = 241  # personal
    # Ouvrir image, rogner exactement à 744x1040 pixels
    im = Image.open(io.BytesIO(png))
    cropped = im.crop((X, 0, X + width, height))  # coin haut gauche
    cropped.save(output_path)
    print(f"✅ Capture carte : {output_path} (dim: {width}x{height})")


if __name__ == "__main__":
    input_dir = Path(INPUT_DIR)
    output_dir = Path(OUTPUT_DIR)

    for folder in input_dir.iterdir():
        if not folder.is_dir() or folder.name in FACTIONS_EXCLUDED:
            continue

        if FACTIONS_NAMES != [] and folder.name not in FACTIONS_NAMES:
            continue

        for html_file in folder.rglob("*.html"):
            rel_path = html_file.relative_to(input_dir)
            output_file = output_dir / rel_path.with_suffix(".png")
            if CARDS_NAMES != [] and rel_path.stem not in CARDS_NAMES:
                continue
            output_file.parent.mkdir(parents=True, exist_ok=True)
            capture_fixed_card(str(html_file), str(output_file))
