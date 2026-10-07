import csv
import os

from sentiment.analyzer import analyze_sentiment

def load_reviews(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))

def analyze_reviews(reviews):
    evaluated = []
    for review in reviews:
        result = analyze_sentiment(review["review_text"])
        evaluated_review = review.copy()
        evaluated_review["sentiment_score"] = result["score"]
        evaluated_review["sentiment"] = result["sentiment"]
        evaluated.append(evaluated_review)
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