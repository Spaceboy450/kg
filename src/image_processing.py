import os
from src.zip_utils import save_zip, UPLOAD_FOLDER
from src.pdf_utils import make_pdf_grid, make_pdf_preview
from src.color_filter import filter_images_by_hue
from src.color_distance import split_images_by_distance
from src.utils import hex_to_hue

EMPTY_RESULT = ([], [], [], None, "", [])


def make_caption(folder, record):
    fname, hue, dist = record
    base = os.path.basename(fname)
    return (os.path.join(folder, fname), f"{base}, Δ={dist:.1f}°")


def filter_and_sort_zip(zip_file, color, tolerance, rows, cols, orientation):
    try:
        saved_files = save_zip(zip_file)
        if not saved_files:
            return EMPTY_RESULT

        target_hue = hex_to_hue(color)
        filtered_files, filter_errors = filter_images_by_hue(UPLOAD_FOLDER, target_hue, tolerance)
        if not filtered_files:
            return EMPTY_RESULT

        all_imgs, left_col, right_col, split_errors = split_images_by_distance(
            UPLOAD_FOLDER, filtered_files, target_hue
        )

        all_paths = [make_caption(UPLOAD_FOLDER, r) for r in all_imgs]
        left_paths = [make_caption(UPLOAD_FOLDER, r) for r in left_col]
        right_paths = [make_caption(UPLOAD_FOLDER, r) for r in right_col]

        pdf_path, pdf_errors = make_pdf_grid(all_paths, rows, cols, orientation)
        pdf_preview_html = make_pdf_preview(pdf_path)

        errors = filter_errors + split_errors + pdf_errors

        return all_paths, left_paths, right_paths, pdf_path, pdf_preview_html, errors
    except Exception as e:
        return EMPTY_RESULT