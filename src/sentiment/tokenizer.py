import re
import unicodedata

def tokenize(text):
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"(?<=\w)['’](?=\w)", "", text)
    return re.findall(r"\w+(?:-\w+)*|[!?.,;:]|[^\w\s]", text)