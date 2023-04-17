import re
from typing import List


def read_article(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def separate_sentences(article: str) -> List[str]:
    return [re.sub(r'^[^a-zA-Z]+', '', sentence)+'.' for sentence in re.split(r'[.\n?!]', article) if sentence]


def save_translated_sentences(sentences: List[str], filename: str) -> None:
    with open(filename, 'w') as f:
        for sentence in sentences:
            f.write(sentence + '\n')
