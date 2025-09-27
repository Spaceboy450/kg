import os
from src.utils import get_dominant_hue, is_valid_image
from src.color_distance import hue_distance

def filter_images_by_hue(folder, target_hue, hue_tolerance_percent):
    hue_tolerance_deg = 360 * (hue_tolerance_percent / 100)
    result = []
    errors = []

    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)
        if not is_valid_image(path):
            continue

        try:
            dominant_hue = get_dominant_hue(path)
            if dominant_hue is None:
                errors.append(f"{fname}: невозможно определить доминирующий цвет")
                continue
            diff = hue_distance(dominant_hue, target_hue)
            if diff <= hue_tolerance_deg:
                result.append(fname)
        except Exception as e:
            errors.append(f"{fname}: ошибка обработки ({e})")

    return result, errors