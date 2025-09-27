import os
import base64
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.lib.units import cm


def make_pdf_grid(records, rows=5, cols=5, orientation="portrait"):
    errors = []

    if not records:
        return None, errors

    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    page_size = portrait(A4) if orientation == "portrait" else landscape(A4)
    page_w, page_h = page_size

    c = canvas.Canvas(tmp_pdf.name, pagesize=page_size)

    col_w = (page_w - 2 * cm) / cols
    row_h = (page_h - 2 * cm) / rows

    max_img_w = col_w * 0.9
    max_img_h = row_h * 0.65

    num_per_page = rows * cols
    idx = 0

    while idx < len(records):
        page_records = records[idx: idx + num_per_page]

        for i, (path, caption) in enumerate(page_records):
            row = i // cols
            col = i % cols
            x0 = col * col_w + cm
            y0 = page_h - (row + 1) * row_h - cm

            if path and os.path.exists(path):
                try:
                    img = ImageReader(path)
                    iw, ih = img.getSize()
                    scale = min(max_img_w / iw, max_img_h / ih)
                    iw *= scale
                    ih *= scale
                    ix = x0 + (col_w - iw) / 2
                    iy = y0 + (row_h * 0.35) + (row_h * 0.65 - ih) / 2
                    c.drawImage(img, ix, iy, iw, ih, preserveAspectRatio=True, anchor="c")
                except Exception as e:
                    errors.append(f"Ошибка вставки {path}: {e}")

            if caption:
                c.setFont("Helvetica", 8)
                tx = x0 + col_w / 2
                ty = y0 + row_h * 0.2
                c.drawCentredString(tx, ty, caption)

        idx += num_per_page
        if idx < len(records):
            c.showPage()

    try:
        c.save()
    except Exception as e:
        errors.append(f"Ошибка сохранения PDF: {e}")

    return tmp_pdf.name, errors


def make_pdf_preview(pdf_path):
    if not pdf_path or not os.path.exists(pdf_path):
        return ""

    try:
        with open(pdf_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")

        #HTML шаблон был доработан с использованием Chat GPT
        return f"""
        <iframe width="100%" height="100%" style="min-height:90vh;"
            srcdoc="
            <html>
            <body style='margin:0; height:100vh;'>
            <script>
            (function() {{
                try {{
                    var b64 = '{b64}';
                    var byteCharacters = atob(b64);
                    var byteNumbers = new Array(byteCharacters.length);
                    for (var i = 0; i < byteCharacters.length; i++) {{
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }}
                    var byteArray = new Uint8Array(byteNumbers);
                    var blob = new Blob([byteArray], {{type: 'application/pdf'}});
                    var url = URL.createObjectURL(blob);
                    document.body.innerHTML =
                        '<iframe src=\\'' + url + '\\' width=100% height=100% style=\\'border:none;\\'></iframe>';
                }} catch(e) {{
                    document.body.innerText = 'Ошибка предпросмотра PDF';
                    console.error(e);
                }}
            }})();
            </script>
            </body>
            </html>
            ">
        </iframe>
        """
    except Exception as e:
        return f"<div style='color:red'>Ошибка генерации предпросмотра PDF: {e}</div>"