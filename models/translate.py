from models.article import read_article, separate_sentences, save_translated_sentences
from models.open_ai import translate_sentences


def translate_article(article_filename: str, output_filename: str) -> None:
    article = read_article(article_filename)
    sentences = separate_sentences(article)
    translated_sentences = translate_sentences(sentences)
    save_translated_sentences(translated_sentences, output_filename)
