import os
import requests

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")  # Store in your .env
PEXELS_SEARCH_URL = "https://api.pexels.com/videos/search"
DOWNLOAD_DIR = "assets"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_relevant_video(keyword, filename="background.mp4"):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": keyword, "per_page": 1}
    
    response = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params)
    if response.status_code != 200:
        print(f"[Pexels] Error: {response.status_code}")
        return None

    videos = response.json().get("videos", [])
    if not videos:
        print("[Pexels] No videos found.")
        return None

    video_url = videos[0]["video_files"][0]["link"]
    video_path = os.path.join(DOWNLOAD_DIR, filename)
    
    with requests.get(video_url, stream=True) as r:
        with open(video_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    return video_path
