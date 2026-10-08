import csv
import os

from sentiment.analyzer import analyze_sentiment

def load_reviews(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))

def analyze_reviews(reviews, existing_reviews=None):
    evaluated = []
    existing_reviews = existing_reviews or {}
    for review in reviews:
        review_id = review["review_id"]
        if review_id in existing_reviews:
            evaluated.append(existing_reviews[review_id])
            continue
        result = analyze_sentiment(review["review_text"])
        evaluated_review = review.copy()
        evaluated_review["sentiment_score"] = result["score"]
        evaluated_review["sentiment"] = result["sentiment"]
        evaluated.append(evaluated_review)
    return evaluated

def analyze_and_save(input_file, output_file):
    reviews = load_reviews(input_file)
    existing = load_reviews(output_file)
    existing_reviews = {
        review["review_id"]: review
        for review in existing
    }
    evaluated = analyze_reviews(reviews, existing_reviews)
    save_analysis(evaluated, output_file)
    return evaluated

def summarize(reviews):
    total = len(reviews)
    summary = {
        "total": total,
        "positive": 0,
        "negative": 0,
        "neutral": 0,
        "average_score": 0.0,
    }
    if total == 0:
        return summary
    total_score = 0.0
    for review in reviews:
        sentiment = review["sentiment"]
        if sentiment == "positive":
            summary["positive"] += 1
        elif sentiment == "negative":
            summary["negative"] += 1
        else:
            summary["neutral"] += 1
        total_score += float(review["sentiment_score"])
    summary["average_score"] = round(total_score / total, 4)
    return summary

def save_analysis(reviews, filepath):
    if not reviews:
        return
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)
    fieldnames = [
        "review_id",
        "product_name",
        "review_text",
        "date",
        "sentiment_score",
        "sentiment",
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(reviews)