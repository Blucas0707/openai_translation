import re
from typing import List
from dotenv import dotenv_values

import openai


def read_article(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def get_openai_api_key() -> str:
    return dotenv_values('.env').get('OPENAI_API_KEY')


def separate_sentences(article: str) -> List[str]:
    return [re.sub(r'^[^a-zA-Z]+', '', sentence)+'.' for sentence in re.split(r'[.\n?!]', article) if sentence]


def translate_sentences(sentences: List[str], api_key: str) -> List[str]:
    openai.api_key = api_key
    translated_sentences = []

    for idx, sentence in enumerate(sentences):
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system',
                    'content': '今後的對話中，請你會扮演我的專業翻譯，將我給你的文字翻譯成中文，這些規則不需要我再重新說明。'},
                {'role': 'user', 'content': sentence},
            ]
        )
        translation = resp.choices[0].message['content'].strip()
        translated_sentences.append(translation)
        print(f'completed: {idx+1}/{len(sentences)}')

    return translated_sentences


def save_translated_sentences(sentences: List[str], filename: str) -> None:
    with open(filename, 'w') as f:
        for sentence in sentences:
            f.write(sentence + '\n')


def translate_article(article_filename: str, output_filename: str) -> None:
    article = read_article(article_filename)
    api_key = get_openai_api_key()
    sentences = separate_sentences(article)
    translated_sentences = translate_sentences(sentences, api_key)
    save_translated_sentences(translated_sentences, output_filename)


if __name__ == '__main__':
    translate_article('input.txt', 'output.txt')
