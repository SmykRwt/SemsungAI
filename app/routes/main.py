# main.py

import os
from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import secure_filename

from app.services.parser import extract_text_from_ppt, extract_text_from_pdf
from app.services.simplifier import simplify_text, get_video_search_prompt
from app.services.tts import generate_voice
from app.services.video_fetcher import download_relevant_video
from app.services.video_maker import combine_audio_with_video

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

            # Step 1: Simplify text for narration
            simplified_text = simplify_text(extracted_text)

            # Step 2: Generate voice narration
            audio_path = generate_voice(simplified_text)  # e.g. static/audio_output/output.mp3

            # Step 3: Extract keyword for stock video search
            search_keyword = get_video_search_prompt(simplified_text)

            # Step 4: Download background video from Pexels
            video_path = download_relevant_video(search_keyword)  # e.g. assets/background.mp4

            # Step 5: Combine audio and video
            final_video_path = None
            if audio_path and video_path:
                final_video_path = combine_audio_with_video(
                    audio_path, video_path, output_path="static/final_output/final_video.mp4"
                )

            # Prepare URLs for frontend
            audio_url = url_for("static", filename=os.path.relpath(audio_path, "static").replace("\\", "/")) if audio_path else None
            video_url = url_for("static", filename=os.path.relpath(final_video_path, "static").replace("\\", "/")) if final_video_path else None


            return render_template(
                "index.html",
                simplified_text=simplified_text,
                audio_url=audio_url,
                video_url=video_url,
                subtitle_text=simplified_text
            )

    return render_template("index.html", simplified_text=None, audio_url=None, video_url=None)
