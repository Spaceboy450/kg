import os
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.lib.units import cm


def make_pdf_grid(records, rows=5, cols=5, orientation="portrait"):
    errors = []

    if not records:
        return None, ["Список изображений пуст"]

    try:
        tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        page_size = portrait(A4) if orientation == "portrait" else landscape(A4)
        page_w, page_h = page_size
        c = canvas.Canvas(tmp_pdf.name, pagesize=page_size)

        margin = 2 * cm
        col_w = (page_w - 2 * margin) / cols
        row_h = (page_h - 2 * margin) / rows

        max_img_w = col_w * 0.9
        max_img_h = row_h * 0.65

        num_per_page = rows * cols
        idx = 0

        while idx < len(records):
            page_records = records[idx: idx + num_per_page]

            for i, (path, caption) in enumerate(page_records):
                row = i // cols
                col = i % cols
                x0 = margin + col * col_w
                y0 = page_h - margin - (row + 1) * row_h

                if path and os.path.exists(path):
                    try:
                        img = ImageReader(path)
                        iw, ih = img.getSize()
                        if iw <= 0 or ih <= 0:
                            raise ValueError("Некорректный размер изображения")

                        scale = min(max_img_w / iw, max_img_h / ih, 1.0)
                        draw_w, draw_h = iw * scale, ih * scale
                        ix = x0 + (col_w - draw_w) / 2.0
                        iy = y0 + (row_h * 0.35) + (row_h * 0.65 - draw_h) / 2.0

                        c.drawImage(img, ix, iy, draw_w, draw_h, preserveAspectRatio=True, anchor="c", mask="auto")
                    except Exception as e:
                        errors.append(f"Ошибка вставки {path}: {e}")

                if caption:
                    try:
                        c.setFont("Helvetica", 8)
                        tx = x0 + col_w / 2.0
                        ty = y0 + row_h * 0.15
                        c.drawCentredString(tx, ty, caption)
                    except Exception as e:
                        errors.append(f"Ошибка подписи {path}: {e}")

            idx += num_per_page
            if idx < len(records):
                c.showPage()

        c.save()
        return tmp_pdf.name, errors
    except Exception as e:
        return None, [f"Ошибка генерации PDF: {e}"]