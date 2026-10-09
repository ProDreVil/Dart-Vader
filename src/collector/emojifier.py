import csv
import os
import sys
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import DATA_FILE

def extract_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001FAFF"
        "\U00002700-\U000027BF"
        "\U00002600-\U000026FF"
        "\U00002300-\U000023FF"
        "]+"
    )
    return "".join(emoji_pattern.findall(text))

def filter_emojis(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return
    with open(input_file, "r", newline="", encoding="utf-8-sig") as file:
        reviews = list(csv.DictReader(file))
    emoji_reviews = []
    for review in reviews:
        emojis = extract_emojis(review["review_text"])
        if emojis:
            emoji_reviews.append({
                "review_id": review["review_id"],
                "emojis": emojis,
            })
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["review_id", "emojis"])
        writer.writeheader()
        writer.writerows(emoji_reviews)
    print("-" * 40)
    print("Emoji filter complete.")
    print(f"Reviews checked: {len(reviews)}")
    print(f"Reviews containing emojis: {len(emoji_reviews)}")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    filter_emojis(DATA_FILE, "data/cleanup/emoji_reviews.csv")