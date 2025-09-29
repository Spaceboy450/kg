import os
from src.utils import get_dominant_hue, is_valid_image


def hue_distance(h1, h2):
    diff = abs(h1 - h2)
    return min(diff, 360 - diff)


def split_images_by_distance(folder, filenames, target_hue, tolerance=10):
    all_images, left_column, right_column, errors = [], [], [], []

    for fname in filenames:
        path = os.path.join(folder, fname)
        if not is_valid_image(path):
            continue

        hue = get_dominant_hue(path, tolerance=tolerance)
        if hue is None:
            errors.append(f"{fname}: не удалось определить цвет")
            continue

        dist = hue_distance(hue, target_hue)
        clockwise_diff = (hue - target_hue) % 360
        record = (fname, hue, dist)

        if clockwise_diff <= 180:
            right_column.append(record)
        else:
            left_column.append(record)

        all_images.append(record)

    key = lambda x: x[2]
    all_images.sort(key=key)
    left_column.sort(key=key)
    right_column.sort(key=key)

    return all_images, left_column, right_column, errors