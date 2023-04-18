from settings import TRANSLATION_FILE_FOLDER_PATH
from models.article import read_article, separate_sentences, save_translated_sentences
from models.open_ai import translate_sentences


def translate_article(input_filename: str) -> None:
    article = read_article(input_filename)
    sentences = separate_sentences(article)
    translated_sentences = translate_sentences(sentences)
    output_filename = f'{TRANSLATION_FILE_FOLDER_PATH}{input_filename.replace(".input", ".outpout")}'
    save_translated_sentences(translated_sentences, output_filename)
