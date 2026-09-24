import urllib.request
import json
import xml.etree.ElementTree as ET
from email.utils import formatdate
import os

SOURCE_URL = "https://raw.githubusercontent.com/Dracid77/lists/main/addon/catalog/movie/released-movies.json"
OUTPUT_FILE = "feed.xml"


def download_source():
    request = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    print("Downloading Dracid77 movie list...")

    data = download_source()
    movies = data.get("metas", [])

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "Dracid77 Released Movies"
    ET.SubElement(channel, "link").text = "https://github.com/Dracid77/lists"
    ET.SubElement(channel, "description").text = "Automatically updated movie list from Dracid77"

    now = formatdate(usegmt=True)

    for movie in movies:
        imdb_id = movie.get("id", "").strip()

        if not imdb_id.startswith("tt"):
            continue

        title = movie.get("name", "").strip()
        year = str(movie.get("releaseInfo", "")).strip()

        if year:
            display_title = f"{title} ({year})"
        else:
            display_title = title

        imdb_url = f"https://www.imdb.com/title/{imdb_id}/"

        item = ET.SubElement(channel, "item")

        ET.SubElement(item, "title").text = display_title
        ET.SubElement(item, "link").text = imdb_url
        ET.SubElement(item, "guid", isPermaLink="false").text = imdb_id
        ET.SubElement(item, "pubDate").text = now
        ET.SubElement(item, "description").text = f"IMDb ID: {imdb_id}"

    tree = ET.ElementTree(rss)
    tree.write(
        OUTPUT_FILE,
        encoding="utf-8",
        xml_declaration=True
    )

    print(f"Created {OUTPUT_FILE}")
    print(f"Movies found: {len(movies)}")


if __name__ == "__main__":
    main()
