import os
from PIL import Image
import colorsys
from collections import Counter

VALID_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}


def is_valid_image(path):
    ext = os.path.splitext(path)[1].lower()
    return os.path.isfile(path) and ext in VALID_EXT


def get_dominant_hue(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")

            hues = []
            for r, g, b in img.getdata():
                h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                if s > 0.2 and v > 0.2:
                    hues.append(int(h * 360))

            if not hues:
                return None

            counter = Counter(hues)
            dominant_hue, _ = counter.most_common(1)[0]
            return dominant_hue

    except Exception:
        return None


def hex_to_hue(color_hex):
    """Переводит HEX (#rrggbb) в hue (0–360)."""
    try:
        color_hex = (color_hex or "#000000").lstrip("#")
        r, g, b = (
            int(color_hex[0:2], 16),
            int(color_hex[2:4], 16),
            int(color_hex[4:6], 16),
        )
        h, _, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        return h * 360
    except Exception:
        return 0.0