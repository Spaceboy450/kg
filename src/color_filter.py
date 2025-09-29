import os
from src.utils import get_dominant_hue, is_valid_image
from src.color_distance import hue_distance


def filter_images_by_hue(folder, target_hue, hue_tolerance_deg):
    result, errors = [], []

    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)
        if not is_valid_image(path):
            continue

        dominant_hue = get_dominant_hue(path, tolerance=hue_tolerance_deg)
        if dominant_hue is None:
            errors.append(f"{fname}: невозможно определить доминирующий цвет")
            continue

        diff = hue_distance(dominant_hue, target_hue)
        if diff <= hue_tolerance_deg:
            result.append(fname)

    return result, errors