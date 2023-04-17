from typing import List

from nltk.tokenize import sent_tokenize


def read_article(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def separate_sentences(article: str) -> List[str]:
    return sent_tokenize(article)


def save_translated_sentences(sentences: List[str], filename: str) -> None:
    with open(filename, 'w') as f:
        for sentence in sentences:
            f.write(sentence + '\n')
