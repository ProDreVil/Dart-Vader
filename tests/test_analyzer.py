import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sentiment.analyzer import analyze_sentiment

TEST_REVIEWS = [
    "good",
    "bad",
    "baaad",
    "baaaaaad",
    "not good",
    "very good",
    "sobrang ganda",
    "hindi maganda",
    "GOOD!!!",
    "sooo good",
    "soooo good",
    "soooooo good",
    "maganda",
    "magandaaa",
    "magandaaaaaa",
    "pangit 😡",
    "good quality",
    "super bad product",
    "Call me high but this product is super bad",
    "sobrang ganda ng product",
    "sobrang ganda ng product pero baaad",
    "maganda pero pangit",
    "pangit pero maganda",
    "good but bad",
    "bad but good",
    "okay pero hindi maganda",
]

def main():
    print("=" * 60)
    print("SENTIMENT ANALYZER TEST")
    print("=" * 60)
    for review in TEST_REVIEWS:
        result = analyze_sentiment(review)
        print(f"\nReview: {review}")
        print(f"Score: {result['score']}")
        print(f"Sentiment: {result['sentiment']}")
        print("\n" + "=" * 60)
    print("MANUAL TEST")
    print("=" * 60)
    while True:
        review = input("\nEnter test review: ")
        if review.lower() == "exit":
            break
        result = analyze_sentiment(review)
        print(f"Score: {result['score']}")
        print(f"Sentiment: {result['sentiment']}")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()