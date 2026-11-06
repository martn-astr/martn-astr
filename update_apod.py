import os
import requests
import re

def get_youtube_thumbnail(video_url):
    video_id_match = re.search(r'(?:v=|\/embed\/|youtu\.be\/)([a-zA-Z0-9_-]{11})', video_url)
    if video_id_match:
        return f"https://img.youtube.com/vi/{video_id_match.group(1)}/hqdefault.jpg"
    return "https://apod.nasa.gov/apod/fap/image/2403/M51_HubbleSchmidt_960.jpg"

def update_apod():
    api_key = os.environ.get("NASA_API_KEY", "DEMO_KEY")
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return
        
    title = data.get("title", "Astronomy Picture of the Day")
    date = data.get("date", "")
    media_type = data.get("media_type", "image")

    if media_type == "image":
        img_url = data.get("hdurl") or data.get("url", "")
    elif media_type == "video":
        video_url = data.get("url", "")
        img_url = get_youtube_thumbnail(video_url)
    else:
        img_url = data.get("url", "")

    apod_html = f"""<div align="center">
  <a href="https://apod.nasa.gov/apod/astropix.html" target="_blank">
    <img src="{img_url}" width="100%" alt="{title}">
  </a>
  <p><b>{title}</b> ({date})</p>
</div>"""
    
    if not os.path.exists("README.md"):
        return

    with open("README.md", "r", encoding="utf-8") as file:
        readme = file.read()
        
    if "<!-- APOD-START -->" not in readme or "<!-- APOD-END -->" not in readme:
        return

    updated_readme = re.sub(
        r'<!-- APOD-START -->[\s\S]*?<!-- APOD-END -->',
        f'<!-- APOD-START -->\n{apod_html}\n<!-- APOD-END -->',
        readme
    )
    
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(updated_readme)

if __name__ == "__main__":
    update_apod()
