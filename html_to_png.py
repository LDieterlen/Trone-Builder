import os
import time
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import glob


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

    X = 239
    # Ouvrir image, rogner exactement à 744x1040 pixels
    im = Image.open(io.BytesIO(png))
    cropped = im.crop((X, 0, X + width, height))  # coin haut gauche
    cropped.save(output_path)
    print(f"✅ Capture carte : {output_path} (dim: {width}x{height})")


input_dir = "output"
output_dir = "png_output"

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".html"):
            html_file = os.path.join(root, file)
            # Conserver la structure du dossier
            rel_path = os.path.relpath(html_file, input_dir)
            output_file = os.path.join(
                output_dir, os.path.splitext(rel_path)[0] + "_fixed.png"
            )
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            capture_fixed_card(html_file, output_file)
