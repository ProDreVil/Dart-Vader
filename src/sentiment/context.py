
ASPECT_WORDS = {
    # English
    "product",
    "item",
    "quality",
    "texture",
    "flavor",
    "taste",
    "size",
    "appearance",
    "delivery",
    "packaging",
    "seller",
    "service",
    "price",
    "material",
    "color",
    "colour",
    "shipping",
    "order",
    "parcel",
    "package",
    # Tagalog
    "produkto",
    "gamit",
    "kalidad",
    "lasa",
    "sukat",
    "itsura",
    "hitsura",
    "pagkakabalot",
    "balot",
    "tinda",
    "tindero",
    "tindera",
    "nagbebenta",
    "serbisyo",
    "presyo",
    "kulay",
    "materyales",
    "pagpapadala",
}

def find_context(tokens, index):
    context = []
    start = max(0, index - 2)
    end = min(len(tokens), index + 3)
    for position in range(start, end):
        if position != index:
            context.append(tokens[position].lower())
    return context

def get_context_words(tokens, index):
    return find_context(tokens, index)

def has_relevant_context(tokens, index):
    return bool(get_context_words(tokens, index))

def has_aspect_context(tokens, index):
    start = max(0, index - 2)
    end = min(len(tokens), index + 3)
    for position in range(start, end):
        if position == index:
            continue
        if tokens[position].lower() in ASPECT_WORDS:
            return True
    return False

def analyze_context(tokens, index):
    return {
        "nearby_words": get_context_words(tokens, index),
        "has_aspect": has_aspect_context(tokens, index),
    }

NEGATIVE_MODIFIERS = {"masyado", "masyadong"}

def get_modifier_sentiment(tokens, index):
    if tokens[index].lower() not in NEGATIVE_MODIFIERS:
        return 0.0
    if index + 1 >= len(tokens):
        return 0.0
    attribute = tokens[index + 1].lower()
    if attribute in {
        "malaki", "mahal", "mabigat", "mataas", "makapal",
        "mabilis", "manipis", "maliit", "matigas", "maluwag",
    }:
        return -2.0
    return 0.0