ASPECT_WORDS = {
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