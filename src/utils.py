from PIL.ImageFont import FreeTypeFont
import math


def add_new_lines(width: int, text: str, font: FreeTypeFont):
    text_lenght = font.getlength(text)
    line_count = 1 + (text_lenght // width)
    size_per_line = math.ceil(text_lenght / line_count)
    text_with_new_lines = ""
    current_text = ""
    for word in text.split(" "):
        lenght = font.getlength(current_text + word)
        if lenght <= size_per_line:
            current_text += word + " "
        else:
            if lenght < width:
                current_text += word
                text_with_new_lines += current_text + "\n"
                current_text = ""
            else:
                text_with_new_lines += current_text + "\n"
                current_text = word + " "
    text_with_new_lines += current_text
    return text_with_new_lines

