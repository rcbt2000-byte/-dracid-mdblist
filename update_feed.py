import urllib.request

# MDBList RSS feed
FEED_URL = "https://mdblist.com/lists/rcbt2000/new-releases?rss=ydn1zcgqw7c1tjhxukhabpike"

# Output file used by the addon
OUTPUT_FILE = "feed.json"


def get_feed():
    request = urllib.request.Request(
        FEED_URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8")


def main():
    print("Downloading MDBList RSS feed...")

    data = get_feed()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(data)

    print(f"Feed updated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
