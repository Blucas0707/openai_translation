from typing import List

import openai

from settings import OPENAI_API_KEY


def translate_sentences(sentences: List[str]) -> List[str]:
    openai.api_key = OPENAI_API_KEY
    translated_sentences = []

    for idx, sentence in enumerate(sentences):
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'system',
                    'content': '今後的對話中，請你扮演我的專業翻譯，將我給你的文字翻譯成中文，這些規則不需要我再重新說明'
                },
                {'role': 'user', 'content': sentence},
            ]
        )
        translation = resp.choices[0].message['content'].strip()
        translated_sentences.append(translation)
        print(f'completed: {idx+1}/{len(sentences)}')

    return translated_sentences
