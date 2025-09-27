import os
from PIL import Image
import colorsys
from statistics import mean

VALID_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}


def is_valid_image(path):
    ext = os.path.splitext(path)[1].lower()
    return os.path.isfile(path) and ext in VALID_EXT


def get_dominant_hue(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        hues = []
        for r, g, b in img.getdata():
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            hues.append(h * 360)
        return mean(hues) if hues else None


#HEX (#rrggbb) в Hue (0-360)
def hex_to_hue(color_hex):
    color_hex = (color_hex or "#000000").lstrip("#")
    r, g, b = (
        int(color_hex[0:2], 16),
        int(color_hex[2:4], 16),
        int(color_hex[4:6], 16),
    )
    h, _, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return h * 360