import csv
import string
import sys
from difflib import SequenceMatcher
from urllib.parse import urlparse, parse_qsl, urlencode


def clean_url(url):
    parts = urlparse(url.strip())

    site = parts.netloc.lower()
    if site.startswith("www."):
        site = site[4:]

    path = parts.path.rstrip("/")

    # drop tracking params like utm_source
    params = [(k, v) for k, v in parse_qsl(parts.query) if not k.startswith("utm_")]

    cleaned = site + path
    if params:
        cleaned += "?" + urlencode(params)
    return cleaned


def clean_title(title):
    title = title.lower()
    for mark in string.punctuation:
        title = title.replace(mark, "")
    return " ".join(title.split())


def is_similar(a, b, threshold=0.9):
    return SequenceMatcher(None, a, b).ratio() >= threshold


def find_similar(title_key, unique):
    for i, story in enumerate(unique):
        if is_similar(title_key, clean_title(story["title"])):
            return i
    return None


def dedupe(alerts):
    unique = []
    seen = {}  # cleaned url or title -> index in unique

    for alert in alerts:
        url_key = clean_url(alert["url"])
        title_key = clean_title(alert["title"])
        topic = alert["topic"].strip()

        index = seen.get(url_key, seen.get(title_key))

        if index is None:
            index = find_similar(title_key, unique)

        if index is None:
            unique.append({
                "title": alert["title"].strip(),
                "url": alert["url"].strip(),
                "topics": [topic],
            })
            index = len(unique) - 1
        elif topic not in unique[index]["topics"]:
            unique[index]["topics"].append(topic)

        seen[url_key] = index
        seen[title_key] = index

    return unique


def main():
    if len(sys.argv) != 3:
        print("Usage: python dedup.py <input.csv> <output.csv>")
        sys.exit(1)

    with open(sys.argv[1], newline="", encoding="utf-8") as f:
        alerts = list(csv.DictReader(f))

    stories = dedupe(alerts)

    with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "url", "topics"])
        for s in stories:
            writer.writerow([s["title"], s["url"], "; ".join(s["topics"])])

    print(f"Read {len(alerts)} alerts")
    print(f"Found {len(stories)} unique stories")
    print(f"Removed {len(alerts) - len(stories)} duplicates")


if __name__ == "__main__":
    main()