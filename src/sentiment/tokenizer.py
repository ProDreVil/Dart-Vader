import re

def tokenize(text):
    text = re.sub(r"(?<=\w)['’](?=\w)", "", text)
    return re.findall(r"\w+(?:-\w+)*|[!?.,;:]|[^\w\s]", text)