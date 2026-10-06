import csv
import os

def save_reviews(reviews, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    existing_reviews = []
    if os.path.exists(filepath):
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            existing_reviews = list(csv.DictReader(file))
    fieldnames = [
        "review_id",
        "product_name",
        "review_text",
        "date",
        "review_url",
    ]
    existing_keys = {
        (review["date"], review["review_text"])
        for review in existing_reviews
    }
    new_reviews = []
    for review in reviews:
        key = (review["date"], review["review_text"])
        if key not in existing_keys:
            new_reviews.append(review)
            existing_keys.add(key)
    file_exists = os.path.exists(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        start_id = len(existing_reviews) + 1
        for index, review in enumerate(new_reviews, start=start_id):
            review["review_id"] = f"review-{index}"
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_reviews)
    return len(new_reviews), len(reviews) - len(new_reviews)