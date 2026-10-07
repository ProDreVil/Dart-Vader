# MSG TO LEE:
# Lee tignan mo kung ok to, nandyan na yung mga mahahalaga binabasa niya yung na sqve na reviews nirate nadin han kung good, bad, o neutral, tapos may summary na yung bilang, average score, tapos yung pinaka positive at negative.
# Nagse save din siya ng bagong CSV na may sentiment, baka pwede yan baguhin monalang lee kung mali.

import csv
import os

from evaluator import ReviewEvaluator


def load_reviews(filepath):
if not os.path.exists(filepath):
return []
with open(filepath, "r", newline="", encoding="utf-8") as file:
return list(csv.DictReader(file))


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
"review_url",
"sentiment_score",
"sentiment",
 ]
with open(filepath, "w", newline="", encoding="utf-8") as file:
writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
writer.writeheader()
writer.writerows(reviews)


def analyze_reviews(reviews):
evaluator = ReviewEvaluator()
evaluated = evaluator.evaluate_reviews(reviews)
summary = evaluator.summarize(evaluated)

if evaluated:
total_score = sum(r["sentiment_score"] for r in evaluated)
summary["average_score"] = round(total_score / len(evaluated), 4)
else:
summary["average_score"] = 0.0

return evaluated, summary


def print_summary(evaluated, summary):
total = summary["total"]
print("========== REVIEW ANALYSIS ==========")
print(f"Total reviews : {total}")
if total == 0:
print("No reviews to analyze.")
return

for name in ("good", "bad", "neutral"):
percent = summary[name] / total * 100
print(f"{name.capitalize():<8}: {summary[name]} ({percent:.1f}%)")
print(f"Average score : {summary['average_score']}")

# most positive and most negative reviews
ranked = sorted(evaluated, key=lambda r: r["sentiment_score"])

print("\nMost negative reviews:")
for review in ranked[:3]:
print(f" {review['sentiment_score']:+.2f} {review['review_text'][:70]}")

print("\nMost positive reviews:")
for review in reversed(ranked[-3:]):
print(f" {review['sentiment_score']:+.2f} {review['review_text'][:70]}")


def analyze_file(input_path, output_path=None):
reviews = load_reviews(input_path)
evaluated, summary = analyze_reviews(reviews)
print_summary(evaluated, summary)
if output_path:
save_analysis(evaluated, output_path)
print(f"\nSaved analysis to {output_path}")
return summary


if name == "main":
from config import DATA_FILE

output = os.path.join(os.path.dirname(DATA_FILE), "analyzed_reviews.csv")
analyze_file(DATA_FILE, output)