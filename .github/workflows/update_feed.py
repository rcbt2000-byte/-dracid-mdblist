import json
import os
import urllib.request

# URL of the MDBList feed
FEED_URL = "https://mdblist.com/lists/dracid77/latest"

# Output file used by the addon
OUTPUT_FILE = "feed.json"


def get_feed():
    request = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8")


def main():
    print("Downloading MDBList feed...")

    data = get_feed()

    # Save the downloaded feed
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(data)

    print(f"Feed updated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
