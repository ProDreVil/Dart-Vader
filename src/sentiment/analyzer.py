from sentiment.tokenizer import tokenize
from sentiment.lexicon import get_word_score, find_closest_word, get_booster
from sentiment.rules import *
from sentiment.context import analyze_context

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
        context = analyze_context(tokens, index)
        word_score = get_word_score(normalized_token)
        if word_score == 0 and get_booster(token) == 0:
            closest_word, distance = find_closest_word(normalized_token)
            if closest_word is not None:
                word_score = get_word_score(closest_word)
                repeated_booster = get_repeated_letter_booster(token)
                if repeated_booster != 0:
                    word_score = apply_booster(word_score, repeated_booster)
        if word_score == 0:
            emoji_score = get_emoji_score(token)
            if emoji_score != 0:
                total_score += emoji_score
                scored_words += 1
            continue
        if has_negation(tokens, index):
            word_score = apply_negation(word_score)
        booster = get_nearby_booster(tokens, index)
        if index > 0:
            repeated_booster = get_repeated_letter_booster(tokens[index - 1])
            if repeated_booster != 0:
                booster += repeated_booster
        if booster != 0:
            word_score = apply_booster(word_score, booster)
            word_score = apply_capitalization(word_score, token)
        if context["has_aspect"]:
            if word_score > 0:
                word_score += 0.1
            elif word_score < 0:
                word_score -= 0.1
        if has_contrast_before(tokens, index):
            word_score *= 1.5
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