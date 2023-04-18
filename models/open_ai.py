from typing import List

import openai

from settings import OPENAI_API_KEY


def translate_sentences(sentences: List[str]) -> List[str]:
    """Translates a list of sentences from English to Traditional Chinese using OpenAI's GPT-3 language model.
    Args:
        sentences (List[str]): A list of sentences to be translated.

    Returns:
        List[str]: A list of translated sentences in Traditional Chinese.

    Raises:
        Exception: If OpenAI API key is missing or invalid.
    """
    prompt = '''
        You have been hired to translate an article about a style of dance from English to Traditional Chinese for a dance magazine in Taiwan.
        The article includes technical terms related to dance, so it is important to have a strong understanding of both English and Traditional Chinese.
        The client requires the final product to be of high quality and culturally sensitive to the target audience in Taiwan.
        Please translate:
    '''
    # Check if the OpenAI API key is valid
    if not OPENAI_API_KEY:
        raise Exception('OpenAI API key is missing or invalid.')

    openai.api_key = OPENAI_API_KEY
    translated_sentences = []
    # Translate each sentence using GPT-3 language model
    for idx, sentence in enumerate(sentences):
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'system',
                    'content': prompt,
                },
                {'role': 'user', 'content': sentence},
            ],
        )
        # Extract the translated sentence from the response
        translation = resp.choices[0].message['content'].strip()
        translated_sentences.append(translation)
        print(f'> completed: {idx+1}/{len(sentences)}')

    return translated_sentences
