LEXICON = {
    # english positive
    "good": 1.9,
    "great": 3.1,
    "excellent": 3.4,
    "amazing": 3.2,
    "love": 3.2,
    "nice": 1.8,
    "best": 3.2,
    "perfect": 3.3,
    "worth": 2.0,
    "recommend": 2.2,
    "recommended": 2.2,
    "fast": 1.6,
    "happy": 2.7,
    "satisfied": 2.3,
    "legit": 2.0,
    "okay": 0.9,
    "ok": 0.9,

    # tagalog positive
    "maganda": 2.6,
    "ganda": 2.4,
    "sulit": 2.8,
    "astig": 2.5,
    "mabilis": 1.8,
    "maayos": 2.0,
    "salamat": 1.9,
    "gusto": 1.8,
    "swak": 2.0,
    "matibay": 2.2,
    "mura": 1.4,
    "solid": 2.4,
    "ayos": 1.8,

    # english negative
    "bad": -2.5,
    "worst": -3.4,
    "terrible": -3.2,
    "poor": -2.3,
    "fake": -3.0,
    "broken": -2.8,
    "damaged": -2.8,
    "late": -1.6,
    "slow": -1.6,
    "disappointed": -2.7,
    "waste": -2.5,
    "scam": -3.5,
    "defective": -2.9,
    "wrong": -2.0,
    "missing": -1.8,
    "useless": -2.8,

    #tagalog negative

    "pangit": -2.8,
    "panget": -2.8,
    "sira": -2.7,
    "basag": -2.6,
    "peke": -3.0,
    "tagal": -1.8,
    "mabagal": -1.8,
    "dismaya": -2.5,
    "sayang": -2.0,
    "bulok": -3.0,
    "palpak": -2.8,
    "kulang": -1.8,
}

NEGATIONS = ["not", "no", "never", "hindi", "di", "wala", "ayaw"]

BOOSTERS = {
    "very": 0.3,
    "super": 0.3,
    "sobra": 0.3,
    "sobrang": 0.3,
    "talaga": 0.3,
    "grabe": 0.3,
    "medyo": -0.3,
}

def get_word_score(word):
    return LEXICON.get(word.lower(), 0)

def is_negation(word):
    return word.lower() in NEGATIONS

def get_booster(word):
    return BOOSTERS.get(word.lower(), 0)