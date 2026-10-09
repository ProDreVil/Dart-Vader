
import csv
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sentiment.analyzer import analyze_sentiment

ANALYZE_REVIEWS_FILE = "data/manual/analyzed_reviews.csv"
OUTPUT_FILE = "data/cleanup/neutral_reviews.csv"

REVIEW_COLUMNS = [
    "review_text",
    "review",
    "text",
    "content",
    "comment",
]

def extract_neutral_reviews():
    if not os.path.exists(ANALYZE_REVIEWS_FILE):
        print(f"File not found: {ANALYZE_REVIEWS_FILE}")
        return
    with open(ANALYZE_REVIEWS_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        if not fieldnames:
            print("Error: CSV has no column headers.")
            return
        required_columns = {"sentiment", "sentiment_score"}
        if not required_columns.issubset(fieldnames):
            print("CSV headers found:", fieldnames)
            print("Missing columns:", required_columns - set(fieldnames))
            return
        review_column = next((column for column in REVIEW_COLUMNS if column in fieldnames), None)
        if review_column is None:
            print(
                "Error: Could not find the review-text column. "
                f"Available columns: {fieldnames}"
            )
            return
        rows = list(reader)
    neutral_reviews = []
    updated_count = 0
    for row in rows:
        if (row.get("sentiment") or "").strip().lower() != "neutral":
            continue
        review_text = (row.get(review_column) or "").strip()
        if not review_text:
            neutral_reviews.append(row.copy())
            continue
        result = analyze_sentiment(review_text)
        row["sentiment_score"] = result["score"]
        row["sentiment"] = result["sentiment"]
        neutral_reviews.append(row.copy())
        updated_count += 1
    neutral_ids = {id(row) for row in []}
    with open(ANALYZE_REVIEWS_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        original_rows = list(reader)
    for original_row, updated_row in zip(original_rows, rows):
        pass
    with open(ANALYZE_REVIEWS_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(neutral_reviews)
    print("-" * 40)
    print("Neutral review reanalysis complete.")
    print(f"Neutral reviews reanalyzed: {updated_count}")
    print(f"Updated main CSV: {ANALYZE_REVIEWS_FILE}")
    print(f"Neutral review report: {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_neutral_reviews()