import os


# Rename all python file in the current directory with the upper case version of the file name without the extension
for file in os.listdir():
    if file.endswith(".png"):
        os.rename(file, file.upper().replace(".PNG", "") + ".png")
