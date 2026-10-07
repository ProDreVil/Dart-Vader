from sentiment.tokenizer import tokenize
from sentiment.lexicon import get_word_score
from sentiment.rules import *

def analyze_sentiment(text):
    tokens = tokenize(text)
    if not tokens:
        return {
            "score": 0.0,
            "sentiment": "neutral",
        }
    total_score = 0.0
    scored_words = 0
    for index, token in enumerate(tokens):
        normalized_token = normalize_repeated_letters(token)
        word_score = get_word_score(normalized_token)
        if word_score == 0:
            emoji_score = get_emoji_score(token)
            if emoji_score != 0:
                total_score += emoji_score
                scored_words += 1
            continue
        if has_negation(tokens, index):
            word_score = apply_negation(word_score)
        booster = get_nearby_booster(tokens, index)
        if booster != 0:
            word_score = apply_booster(word_score, booster)
        word_score = apply_capitalization(word_score, token)
        total_score += word_score
        scored_words += 1
    if scored_words == 0:
        return {
            "score": 0.0,
            "sentiment": "neutral",
        }
    score = total_score / scored_words
    score = apply_punctuation(score, text)
    if score > 0:
        score = score / (score + 1.0)
    elif score < 0:
        score = score / (-score + 1.0)
    if score >= 0.05:
        sentiment = "positive"
    elif score <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return {
        "score": round(score, 4),
        "sentiment": sentiment,
    }