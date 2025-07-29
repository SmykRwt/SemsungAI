# app/services/voice_gen.py

import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
HEADERS = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

AUDIO_FOLDER = os.path.join("static", "audio_output")
os.makedirs(AUDIO_FOLDER, exist_ok=True)

def generate_voice(text):
    if not text or not text.strip():
        print("[VoiceGen] Empty text input, skipping audio generation.")
        return None

    filename = f"output_{uuid.uuid4().hex[:8]}.mp3"
    output_path = os.path.join(AUDIO_FOLDER, filename)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            return output_path
        else:
            print(f"[VoiceGen] Failed with status {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[VoiceGen] Request failed: {e}")
        return None
