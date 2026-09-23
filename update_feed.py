import urllib.request
import xml.etree.ElementTree as ET
import json
import re
import os

FEED_URL = "https://mdblist.com/lists/rcbt2000/new-releases?rss=ydn1zcgqw7c1tjhxukhabpike"

OUTPUT_FILE = "addon/catalog/movie/new-releases.json"


def download_feed():
    request = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request) as response:
        return response.read()


def get_text(element, tag):
    child = element.find(tag)
    return child.text.strip() if child is not None and child.text else ""


def extract_imdb(description):
    match = re.search(
        r"(?:imdb\.com/title/)(tt\d+)",
        description,
        re.IGNORECASE
    )
    return match.group(1) if match else ""


def extract_poster(description):
    match = re.search(
        r'<img[^>]+src=["\']([^"\']+)["\']',
        description,
        re.IGNORECASE
    )
    return match.group(1) if match else ""


def extract_year(title):
    match = re.search(r"\((\d{4})\)\s*$", title)
    return match.group(1) if match else ""


def clean_title(title):
    return re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()


def main():
    print("Downloading MDBList RSS feed...")

    data = download_feed()
    root = ET.fromstring(data)

    metas = []

    for item in root.findall("./channel/item"):
        guid = get_text(item, "guid")

        # Only include movies
        if guid and not guid.lower().startswith("movie:"):
            continue

        title = get_text(item, "title")
        description = get_text(item, "description")

        imdb_id = extract_imdb(description)

        if not imdb_id:
            continue

        meta = {
            "type": "movie",
            "id": imdb_id,
            "name": clean_title(title)
        }

        poster = extract_poster(description)
        if poster:
            meta["poster"] = poster

        year = extract_year(title)
        if year:
            meta["releaseInfo"] = year

        metas.append(meta)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump({"metas": metas}, file, ensure_ascii=False, separators=(",", ":"))

    print(f"Created {OUTPUT_FILE}")
    print(f"Movies found: {len(metas)}")


if __name__ == "__main__":
    main()
