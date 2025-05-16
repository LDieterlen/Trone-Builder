from PIL.ImageFont import FreeTypeFont
from PIL import Image
import math
import re


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


def process_keywords(text: str, global_data: dict):
    """
    Process keywords in the format {{type:key}} in text.
    Returns:
    - processed_text: Text with keywords replaced by actual text values or spaces for icons
    - icons_info: List of tuples (icon_path, position_in_text) for icons that need to be inserted
    """
    icons_info = []
    processed_text = text
    
    # Find all instances of {{type:key}}
    pattern = r'{{(text|icon):([^}]+)}}'
    matches = re.findall(pattern, text)
    
    offset = 0
    for match_type, key in matches:
        keyword = f"{{{{{match_type}:{key}}}}}"
        start_pos = text.find(keyword)
        
        if match_type == "text":
            # Replace text keyword with its value
            if key in global_data["text"]:
                replacement = global_data["text"][key]
                processed_text = processed_text.replace(keyword, replacement)
            else:
                # If the key is not found, leave it as is
                pass
        elif match_type == "icon":
            # Replace icon keyword with 5 spaces to leave room for the icon
            if key in global_data["icon"]:
                icon_path = global_data["icon"][key]
                # Calculate position - the position needs to be adjusted based on text processing
                position = start_pos + offset
                icons_info.append((icon_path, position))
                processed_text = processed_text.replace(keyword, "     ", 1)
                offset += 5 - len(keyword)
            else:
                # If the icon is not found, leave it as is
                pass
    
    return processed_text, icons_info
