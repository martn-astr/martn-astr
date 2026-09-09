import os
import requests
import re

def update_apod():
    # Fetch API key from GitHub Secrets
    api_key = os.environ.get("NASA_API_KEY", "DEMO_KEY")
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    
    # Get data from NASA
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch APOD")
        return
        
    data = response.json()
    title = data.get("title", "Astronomy Picture of the Day")
    img_url = data.get("url", "")
    date = data.get("date", "")
    
    # Format the image for your README
    apod_html = f"""
<div align="center">
  <a href="https://apod.nasa.gov/apod/astropix.html">
    <img src="{img_url}" width="80%" alt="{title}">
  </a>
  <p><strong>{title}</strong> ({date})</p>
</div>
"""
    
    # Read your current README.md
    with open("README.md", "r", encoding="utf-8") as file:
        readme = file.read()
        
    # Replace the placeholder text between your HTML comments
    readme = re.sub(
        r'<!-- APOD-START -->.*<!-- APOD-END -->',
        f'<!-- APOD-START -->\n{apod_html}\n<!-- APOD-END -->',
        readme,
        flags=re.DOTALL
    )
    
    # Save the updated README.md
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme)

if __name__ == "__main__":
    update_apod()
