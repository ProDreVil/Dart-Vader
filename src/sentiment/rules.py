import re

from sentiment.lexicon import is_negation, get_booster

def apply_negation(score):
    return -score

def apply_booster(score, booster):
    if score > 0:
        return score * (1 + booster)
    if score < 0:
        return score * (1 + booster)
    return score

def has_negation(tokens, index, window=3):
    start = max(0, index - window)
    for position in range(start, index):
        if is_negation(tokens[position]):
            return True
    return False

def get_nearby_booster(tokens, index):
    if index == 0:
        return 0
    return get_booster(tokens[index - 1])

def apply_capitalization(score, word):
    if len(word) > 1 and word.isupper() and word.isalpha():
        if score > 0:
            return score + 0.3
        if score < 0:
            return score - 0.3
    return score

def apply_punctuation(score, text):
    exclamation_count = text.count("!")
    if exclamation_count == 0:
        return score
    emphasis = min(exclamation_count * 0.1, 0.3)
    if score > 0:
        return score + emphasis
    if score < 0:
        return score - emphasis
    return score

def normalize_repeated_letters(word):
    return re.sub(r"(.)\1{2,}", r"\1\1", word)

def get_repeated_letter_booster(word):
    matches = re.findall(r"(.)\1{2,}", word.lower())
    if not matches:
        return 0.0
    repetition_count = sum(
        len(match.group(0)) - 1
        for match in re.finditer(r"(.)\1+", word.lower())
    )
    return min(repetition_count * 0.1, 0.5)

EMOJI_SCORES = {
    # POSITIVE
    "❤️": 2.5,
    "❤": 2.5,
    "😍": 3.0,
    "🥰": 2.8,
    "😊": 2.0,
    "😁": 2.2,
    "😄": 2.2,
    "👍": 2.0,
    "👏": 1.8,
    "✨": 1.5,
    "💖": 2.8,
    "💕": 2.5,
    #NEGATIVE
    "😡": -2.8,
    "😠": -2.5,
    "😞": -2.2,
    "😔": -2.0,
    "😢": -2.0,
    "😭": -2.3,
    "👎": -2.0,
    "💔": -2.8,
    "🤮": -3.0,
    "😤": -2.4,
}

def get_emoji_score(emoji):
    return EMOJI_SCORES.get(emoji, 0.0)