# main.py

import os
from flask import Blueprint, render_template, request, url_for
from app.services.parser import extract_text_from_ppt
from app.services.parser import extract_text_from_pdf
from app.services.simplifier import simplify_text
from app.services.tts import generate_voice
from werkzeug.utils import secure_filename

main = Blueprint("main", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pptx", "pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)

            ext = filename.rsplit(".", 1)[1].lower()
            if ext == "pptx":
                extracted_text = extract_text_from_ppt(save_path)
            elif ext == "pdf":
                extracted_text = extract_text_from_pdf(save_path)
            else:
                extracted_text = ""

            simplified_text = simplify_text(extracted_text)

            # Generate audio file from simplified text
            audio_path = generate_voice(simplified_text)  # Full static/audio_output path

            if audio_path:
                relative_path = os.path.relpath(audio_path, "static").replace("\\", "/")
                audio_url = url_for("static", filename=relative_path)
            else:
                audio_url = None

            return render_template(
                "index.html",
                simplified_text=simplified_text,
                audio_url=audio_url
            )

    return render_template("index.html", simplified_text=None, audio_url=None)