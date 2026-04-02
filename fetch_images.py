import os
import requests
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
IMAGES_DIR = "images"


def fetch_lily_images(count=3):
    """Fetch `count` different lily images from Unsplash and save to images/."""
    os.makedirs(IMAGES_DIR, exist_ok=True)

    response = requests.get(
        "https://api.unsplash.com/search/photos",
        params={"query": "lily flower", "per_page": count, "orientation": "landscape"},
        headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
    )
    response.raise_for_status()

    results = response.json().get("results", [])
    if len(results) < count:
        raise ValueError(f"Only {len(results)} images returned, expected {count}")

    saved_paths = []
    for i, photo in enumerate(results[:count]):
        image_url = photo["urls"]["regular"]
        image_response = requests.get(image_url)
        image_response.raise_for_status()

        path = os.path.join(IMAGES_DIR, f"lily_{i + 1}.jpg")
        with open(path, "wb") as f:
            f.write(image_response.content)
        print(f"Downloaded: {path}")
        saved_paths.append(path)

    return saved_paths


if __name__ == "__main__":
    paths = fetch_lily_images()
    print("All images downloaded:", paths)
