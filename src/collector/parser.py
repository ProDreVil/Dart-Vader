import re

def extract_product_name(lines):
    for line in lines:
        if line.startswith("Product image "):
            return line[len("Product image "):].strip()
    return ""

FILTER_PATTERNS = [
    r"seller['’]?s?\s+response\s*:.*$",
    r"\bprofile\s+\S+.*$",
    r"\bhelpful\?.*$",
    r"\b[a-zA-Z]\*{3,}[a-zA-Z]\b.*$",
    r"\.\.\.\s*\.\.\..*$",
]

def clean_review_text(review_text):
    cleaned = review_text
    for pattern in FILTER_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def parse_reviews_from_text(text):
    reviews = []
    review_header_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}\s+\|\s+Variation:")
    lines = [line.strip() for line in text.splitlines()]
    try:
        ratings_start = lines.index("Product Ratings")
    except ValueError:
        return []
    product_name = extract_product_name(lines)
    if not product_name:
        product_name = "Unknown Product"
    ratings_end = len(lines)
    for index, line in enumerate(lines):
        if "From The Same Shop" in line:
            ratings_end = index
            break
    lines = lines[:ratings_end]
    for index, line in enumerate(lines):
        match = review_header_pattern.match(line)
        if not match:
            continue
        date = match.group(1)
        review_lines = []
        for current in lines[index + 1:]:
            if "From The Same Shop" in current:
                break
            if re.search(r"seller'?s response:", current, re.IGNORECASE):
                current = re.split(r"seller'?s response:", current, maxsplit=1, flags=re.IGNORECASE)[0].strip()
                if current:
                    review_lines.append(current)
                break
            if re.search(r"\bprofile\s+\S+", current, re.IGNORECASE):
                current = re.split(r"\bprofile\b", current, maxsplit=1, flags=re.IGNORECASE)[0].strip()
                if current:
                    review_lines.append(current)
                break
            if review_header_pattern.match(current):
                break
            if re.fullmatch(r"\d+:\d{2}", current):
                break
            if re.search(r"helpful\?", current, re.IGNORECASE):
                before_helpful = re.split(r"helpful\?", current, maxsplit=1, flags=re.IGNORECASE)[0].strip()
                if before_helpful:
                    review_lines.append(before_helpful)
                break
            if re.fullmatch(r"[a-zA-Z]\*{3,}[a-zA-Z]", current):
                break
            if re.fullmatch(r"\d+", current):
                continue
            review_lines.append(current)
        review_text = " ".join(review_lines).strip()
        review_text = clean_review_text(review_text)
        if review_text:
            reviews.append({
                "review_id": "",
                "product_name": product_name,
                "review_text": review_text,
                "date": date,
            })
    return reviews