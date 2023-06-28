from typing import List
from io import BufferedReader
from time import sleep

import openai

from settings import OPENAI_API_KEY
from utils.base import retry
from models.open_ai.enums import OpenAIEngineEnum


class OpenAI:
    OPENAI_API_KEY = OPENAI_API_KEY

    def __init__(
        self,
        engine: OpenAIEngineEnum = OpenAIEngineEnum.GPT_3_5_TURBO,
        sleep_second: float = 0.5,
    ) -> None:
        # Check if the OpenAI API key is valid
        if not OPENAI_API_KEY:
            raise Exception('OpenAI API key is missing')

        openai.api_key = self.OPENAI_API_KEY
        self.engine = str(engine)
        self.sleep_second = sleep_second

    def translate_sentences(
        self, sentences: List[str], prompt: str = None
    ) -> List[str]:
        '''Translates a list of sentences from English to Traditional Chinese using OpenAI's GPT-3 language model.
        Args:
            sentences (List[str]): A list of sentences to be translated.

        Returns:
            List[str]: A list of translated sentences in Traditional Chinese.

        Raises:
            Exception: If OpenAI API key is missing or invalid.
        '''
        if not prompt:
            prompt = '''
                You have been hired to translate an article to Traditional Chinese.
                Please translate:
            '''

        translated_sentences = []
        # Translate each sentence using GPT-3 language model
        for idx, sentence in enumerate(sentences):
            translation = retry(
                lambda: _translate(self.engine, prompt, sentence),
                errors=(openai.error.ServiceUnavailableError,),
                sleep_second=10,
            )
            translated_sentences.append(translation)
            print('> translating: ', translation)
            print(f'> completed: {idx+1}/{len(sentences)}')

            sleep(self.sleep_second)

        return translated_sentences

    def transcribe(self, source: BufferedReader) -> str:
        '''Transcribe an audio file to text using OpenAI's API.
        https://platform.openai.com/docs/guides/speech-to-text/quickstart

        The size of the audio file must be less than 25 MB.

        Args: file_path (str): The path to the audio file to be transcribed.
        Returns: str: The transcribed text.
        '''
        if not source:
            raise Exception('Source file is missing')

        transcript = openai.Audio.translate('whisper-1', source)

        return transcript.get('text', '')


def _translate(engine: OpenAIEngineEnum, prompt: str, sentence: str) -> str:
    resp = openai.ChatCompletion.create(
        model=engine,
        messages=[
            {
                'role': 'system',
                'content': prompt,
            },
            {'role': 'user', 'content': sentence},
        ],
    )
    # Extract the translated sentence from the response
    return resp.choices[0].message['content'].strip()
