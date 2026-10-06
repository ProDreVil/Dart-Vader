import csv
import os

def save_reviews(reviews, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fieldnames = [
        "review_id",
        "product_name",
        "review_text",
        "date",
    ]
    existing_reviews = []
    if os.path.exists(filepath):
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            existing_reviews = list(csv.DictReader(file))
    existing_keys = {
        review["review_text"]
        for review in existing_reviews
    }
    new_reviews = []
    for review in reviews:
        key = review["review_text"]
        if key not in existing_keys:
            new_reviews.append(review)
            existing_keys.add(key)
    start_id = len(existing_reviews) + 1
    for index, review in enumerate(new_reviews, start=start_id):
        review["review_id"] = f"review-{index}"
    with open(filepath, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not existing_reviews:
            writer.writeheader()
        writer.writerows(new_reviews)
    saved_count = len(new_reviews)
    duplicate_count = len(reviews) - saved_count
    return saved_count, duplicate_count