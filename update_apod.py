import os
import requests
import re

def update_apod():
    api_key = os.environ.get("NASA_API_KEY", "DEMO_KEY")
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch APOD")
        return
        
    data = response.json()
    title = data.get("title", "Astronomy Picture of the Day")
    img_url = data.get("url", "")
    date = data.get("date", "")
    
    # Check if it's a video (like YouTube) instead of an image
    media_type = data.get("media_type", "image")
    if media_type != "image":
        img_url = data.get("hdurl", "https://apod.nasa.gov/apod/image/2403/M51_HubbleSchmidt_960.jpg") # Fallback image if APOD is a video

    # Clean Markdown/HTML block for README
    apod_html = f"""<div align="center">
  <a href="https://apod.nasa.gov/apod/astropix.html" target="_blank">
    <img src="{img_url}" width="100%" alt="{title}">
  </a>
  <p><b>{title}</b> ({date})</p>
</div>"""
    
    with open("README.md", "r", encoding="utf-8") as file:
        readme = file.read()
        
    if "<!-- APOD-START -->" not in readme or "<!-- APOD-END -->" not in readme:
        print("Error: APOD markers missing from README.md")
        return

    readme = re.sub(
        r'<!-- APOD-START -->[\s\S]*?<!-- APOD-END -->',
        f'<!-- APOD-START -->\n{apod_html}\n<!-- APOD-END -->',
        readme
    )
    
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme)

if __name__ == "__main__":
    update_apod()
