import os
import tempfile
import uuid
import base64
from io import BytesIO
from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image

from src.utils import hex_to_hue, is_valid_image
from src.color_filter import filter_images_by_hue
from src.color_distance import split_images_by_distance
from src.pdf_utils import make_pdf_grid

app = Flask(__name__)

# Хранилище временных PDF по токенам
PDF_STORAGE = {}


def make_preview(path: str) -> tuple[str, str]:
    """Создает base64 превью и MIME-тип для отображения миниатюры в браузере."""
    try:
        with Image.open(path) as img:
            img.thumbnail((100, 100))

            # Определяем формат
            ext = os.path.splitext(path)[1].lower()
            if ext in (".jpg", ".jpeg"):
                fmt, mime = "JPEG", "image/jpeg"
            else:
                fmt, mime = "PNG", "image/png"

            if img.mode in ("RGBA", "LA", "P"):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
                img = bg

            buf = BytesIO()
            img.save(buf, format=fmt)
            return base64.b64encode(buf.getvalue()).decode("utf-8"), mime
    except Exception as e:
        print(f"[PREVIEW ERROR] {path}: {e}")
        return "", "image/jpeg"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/select", methods=["POST"])
def select():
    """Фильтрация и сортировка изображений, возвращает JSON с двумя колонками."""
    uploaded_files = request.files.getlist("images")
    if not uploaded_files:
        return jsonify({"error": "Файлы не выбраны"}), 400

    try:
        target_color = request.form.get("targetColor", "#ff0000")
        tolerance = float(request.form.get("tolerance", 10))
        target_hue = hex_to_hue(target_color)
    except Exception as e:
        return jsonify({"error": f"Некорректные параметры: {e}"}), 400

    errors = []

    with tempfile.TemporaryDirectory() as tmpdir:
        filenames = []
        for file in uploaded_files:
            fname = os.path.basename(file.filename)
            path = os.path.join(tmpdir, fname)
            file.save(path)
            if is_valid_image(path):
                filenames.append(fname)

        filtered, err1 = filter_images_by_hue(tmpdir, target_hue, tolerance)
        all_images, left_col, right_col, err2 = split_images_by_distance(tmpdir, filtered, target_hue)
        errors.extend(err1 + err2)

        def serialize(records):
            return [
                {
                    "caption": f"{fname} — Δ{dist:.1f}°",
                    "preview": make_preview(os.path.join(tmpdir, fname))[0],
                    "mime": make_preview(os.path.join(tmpdir, fname))[1],
                }
                for fname, _, dist in records
            ]

        return jsonify({"left": serialize(left_col), "right": serialize(right_col), "errors": errors})


@app.route("/process", methods=["POST"])
def process():
    """Формирование PDF с выбранными параметрами."""
    uploaded_files = request.files.getlist("images")
    if not uploaded_files:
        return jsonify({"error": "Файлы не выбраны"}), 400

    try:
        target_color = request.form.get("targetColor", "#ff0000")
        tolerance = float(request.form.get("tolerance", 10))
        rows = max(1, min(5, int(request.form.get("rows", 5))))
        cols = max(1, min(5, int(request.form.get("cols", 5))))
        orientation = request.form.get("orientation", "portrait")
        target_hue = hex_to_hue(target_color)
    except Exception as e:
        return jsonify({"error": f"Некорректные параметры: {e}"}), 400

    errors = []

    with tempfile.TemporaryDirectory() as tmpdir:
        filenames = []
        for file in uploaded_files:
            fname = os.path.basename(file.filename)
            path = os.path.join(tmpdir, fname)
            file.save(path)
            if is_valid_image(path):
                filenames.append(fname)

        filtered, err1 = filter_images_by_hue(tmpdir, target_hue, tolerance)
        all_images, _, _, err2 = split_images_by_distance(tmpdir, filtered, target_hue)
        errors.extend(err1 + err2)

        records = [
            (os.path.join(tmpdir, fname), f"{fname} — Δ{dist:.1f}°")
            for fname, _, dist in all_images
        ]

        pdf_path, pdf_errors = make_pdf_grid(records, rows=rows, cols=cols, orientation=orientation)
        errors.extend(pdf_errors)

        if not pdf_path:
            return jsonify({"error": "Не удалось создать PDF", "errors": errors}), 500

        token = str(uuid.uuid4())
        PDF_STORAGE[token] = pdf_path

        return jsonify({"pdf_url": f"/download/{token}", "errors": errors, "count": len(records)})


@app.route("/download/<token>")
def download(token):
    """Отдача PDF по токену."""
    pdf_path = PDF_STORAGE.get(token)
    if not pdf_path or not os.path.exists(pdf_path):
        return "PDF не найден", 404
    return send_file(pdf_path, as_attachment=False, mimetype="application/pdf")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)