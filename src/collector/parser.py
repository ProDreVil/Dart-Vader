import re

def parse_reviews_from_text(text):
    reviews = []
    date_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}")
    lines = [line.strip() for line in text.splitlines()]
    for index, line in enumerate(lines):
        match = date_pattern.match(line)
        if not match:
            continue
        date = match.group(1)
        username = lines[index - 1] if index > 0 else ""
        review_lines = []
        for current in lines[index + 1:]:
            if current.lower() == "seller's response:":
                break
            if date_pattern.match(current):
                break
            if re.fullmatch(r"\d+:\d{2}", current):
                continue
            review_lines.append(current)
        review_text = " ".join(review_lines).strip()
        if review_text:
            reviews.append({
                "review_id": "",
                "product_name": "",
                "review_text": review_text,
                "date": date,
                "review_url": "",
            })
    return reviews