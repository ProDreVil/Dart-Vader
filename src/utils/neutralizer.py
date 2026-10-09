
import csv
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import ANALYZED_DATA_FILE

OUTPUT_FILE = "data/cleanup/neutral_reviews.csv"

def extract_neutral_reviews():
    if not os.path.exists(ANALYZED_DATA_FILE):
        print(f"File not found: {ANALYZED_DATA_FILE}")
        return
    with open(ANALYZED_DATA_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        if not fieldnames or "sentiment" not in fieldnames:
            print("Error: CSV does not contain a 'sentiment' column.")
            return
        neutral_reviews = [
            row for row in reader
            if (row.get("sentiment") or "").strip().lower() == "neutral"
        ]
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(neutral_reviews)
    print("-" * 40)
    print("Neutral review extraction complete.")
    print(f"Neutral reviews found: {len(neutral_reviews)}")
    print(f"Output: {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_neutral_reviews()