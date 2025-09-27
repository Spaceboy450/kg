import os
import shutil
import zipfile
import tempfile

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_zip(file_obj):
    shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = None
    if isinstance(file_obj, str) and os.path.isfile(file_obj):
        file_path = file_obj
    elif hasattr(file_obj, "name") and os.path.isfile(file_obj.name):
        file_path = file_obj.name
    elif isinstance(file_obj, dict) and "tmp_path" in file_obj and os.path.isfile(file_obj["tmp_path"]):
        file_path = file_obj["tmp_path"]
    else:
        try:
            data = getattr(file_obj, "read", lambda: None)()
            if data:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
                tmp.write(data)
                tmp.close()
                file_path = tmp.name
        except Exception:
            pass

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(UPLOAD_FOLDER)

    files = []
    for root, _, filenames in os.walk(UPLOAD_FOLDER):
        for fname in filenames:
            rel = os.path.relpath(os.path.join(root, fname), UPLOAD_FOLDER)
            files.append(rel)
    return files