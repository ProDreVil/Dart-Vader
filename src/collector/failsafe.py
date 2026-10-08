import csv
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import DATA_FILE
from collector.parser import clean_review_text

def filter_reviews(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return
    with open(input_file, "r", newline="", encoding="utf-8-sig") as file:
        reviews = list(csv.DictReader(file))
    changed_count = 0
    for review in reviews:
        original = review["review_text"]
        cleaned = clean_review_text(original)
        if cleaned != original:
            changed_count += 1
        review["review_text"] = cleaned
    fieldnames = reviews[0].keys() if reviews else []
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reviews)
    print("----------------------------------------")
    print("Review filter complete.")
    print(f"Reviews checked: {len(reviews)}")
    print(f"Reviews changed: {changed_count}")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    output_file = "data/reviews_cleaned.csv"
    filter_reviews(DATA_FILE, output_file)