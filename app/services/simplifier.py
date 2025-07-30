# app/services/llm_simplifier.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.5-pro")

def simplify_text(input_text):
    # prompt = (
    #     "Simplify this text as if you’re reading it out loud for a YouTube video or an educational podcast. "
    #     "Keep it short, clear, and easy to follow. Use natural spoken English with short sentences. "
    #     "Avoid technical jargon unless you explain it. Make sure it sounds friendly, like a teacher talking to beginners.\n\n"
    #     "Split the output into natural speech-friendly blocks, each 1–3 sentences long.\n\n"
    #     f"Slide content:\n\"\"\"\n{input_text.strip()}\n\"\"\""
    # )
    prompt = (
        "Write two lines, dont exceed 20 words"
        f"Slide content:\n\"\"\"\n{input_text.strip()}\n\"\"\""
    )


    response = model.generate_content(prompt)
    return response.text.strip()

def get_video_search_prompt(simplified_text):
    prompt = f"Given the following simplified educational narration:\n\n{simplified_text}\n\nExtract a short and simple keyword or phrase (max 5 words) that represents the topic of the narration. This keyword should be used to search for a stock video background."
    
    gemini_response = model.generate_content(prompt)  # Replace `model` with your Gemini setup
    return gemini_response.text.strip()

