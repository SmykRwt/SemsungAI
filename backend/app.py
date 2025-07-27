from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_slide():
    file = request.files['slide']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        # TODO: Add slide parsing + summarization
        return f"Uploaded: {file.filename}"
    return "No file uploaded"

if __name__ == '__main__':
    app.run(debug=True)
