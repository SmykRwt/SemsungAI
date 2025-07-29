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
