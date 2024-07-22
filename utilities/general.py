import re

def to_single_line(text: str = None) -> str:
    no_surplus = re.compile(r"\s+").sub(" ", text)
    no_trailing = no_surplus.strip()

    return no_trailing