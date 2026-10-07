from sentiment.lexicon import is_negation, get_booster

def apply_negation(score):
    return -score

def apply_booster(score, booster):
    if score > 0:
        return score + booster
    if score < 0:
        return score - booster
    return score