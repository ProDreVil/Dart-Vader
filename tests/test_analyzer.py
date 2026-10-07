import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sentiment.analyzer import analyze_sentiment

TEST_REVIEWS = [
    "good",
    "bad",
    "not good",
    "very good",
    "sobrang ganda",
    "hindi maganda",
    "GOOD!!!",
    "soooo good",
    "pangit 😡",
]

def main():
    print("=" * 60)
    print("DART VADER - SENTIMENT ANALYZER TEST")
    print("=" * 60)
    for review in TEST_REVIEWS:
        result = analyze_sentiment(review)
        print(f"\nReview: {review}")
        print(f"Score: {result['score']}")
        print(f"Sentiment: {result['sentiment']}")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()