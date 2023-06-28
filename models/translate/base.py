from typing import List
from urllib.parse import urlparse
from os import remove

from pydub import AudioSegment
from pydub.utils import make_chunks

from settings import (
    TRANSLATION_FILE_INPUT_FOLDER_PATH,
    TRANSLATION_FILE_OUTPUT_FOLDER_PATH,
)
from models.translate.enums import SourceTypeEnum, TranscribeSourceFileFormatEnum, TranslationSourceFileFormatEnum
from models.article import read_article, separate_sentences, save_translated_sentences
from models.open_ai.base import OpenAI


MAX_AUDIO_FILE_MILLISEC = 1000 * 60 * 10  # 10 mins


def translate(source_path: str, prompt: str) -> None:
    paths = source_path.split('/', 1)[-1].split('.', 1)
    filename, file_format = paths[0], paths[-1]

    if not TranslationSourceFileFormatEnum.has_value(file_format):
        raise Exception('Invalid source file format for translation')

    article = read_article(source_path)
    sentences = separate_sentences(article)
    translated_sentences = OpenAI().translate_sentences(sentences, prompt)
    output_filename = f'{TRANSLATION_FILE_OUTPUT_FOLDER_PATH}{filename}.{file_format}'
    save_translated_sentences(translated_sentences, output_filename)


def _transcribe_youtube(url: str) -> None:
    pass


def _transcribe_file(source_path: str) -> None:
    source_format = source_path.split('.', 1)[-1]

    if not TranscribeSourceFileFormatEnum.has_value(source_format):
        raise Exception(
            f'Invalid source file format, only {','.join(TranscribeSourceFileFormatEnum.get_all_values())} is allowed'
        )

    # separate audio file into chunks
    audio_file_names = _separate_audios(source_path, source_format)

    transcript = ''
    for idx, file_name in enumerate(audio_file_names):
        with open(f'{file_name}', 'rb') as file:
            transcript += OpenAI().transcribe(file)

        print(f'{idx+1}/{len(audio_file_names)} completed')

    transcript_filename = source_path.replace(
        TRANSLATION_FILE_INPUT_FOLDER_PATH, TRANSLATION_FILE_OUTPUT_FOLDER_PATH
    ).replace(source_format, 'txt')
    open(f'{transcript_filename}', 'w').write(transcript)

    remove_files(audio_file_names)

    # 將轉錄文本附加到視頻中（這部分需要使用其他視頻處理庫）
    # 你可以使用OpenCV、MoviePy或FFmpeg等庫來處理視頻並將文本附加到視頻中
    # 下面是一個示例代碼，使用MoviePy庫將文本附加到視頻中
    # from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

    # # 載入視頻文件
    # video = VideoFileClip(video_path)

    # # 創建文本製作片段
    # text_clip = TextClip(transcript, fontsize=24, color='white', bg_color='black').set_duration(video.duration)

    # # 合成視頻和文本
    # final_clip = CompositeVideoClip([video, text_clip])

    # # 輸出合成後的視頻文件
    # output_path = 'output_video.mp4'
    # final_clip.write_videofile(output_path, codec='libx264')


SOURCE_TYPE_F_MAP = {
    SourceTypeEnum.URL: _transcribe_youtube,
    SourceTypeEnum.FILE_PATH: _transcribe_file,
}


def transcribe(source_path: str) -> None:
    if not source_path:
        return

    source_type = _get_source_type(source_path)

    f = SOURCE_TYPE_F_MAP[source_type]
    f(source_path)


def _separate_audios(
    source_path: str, source_format: TranscribeSourceFileFormatEnum
) -> List[str]:
    video = AudioSegment.from_file(source_path, format=source_format)

    file_name = source_path.split('.', 1)[-2]
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio.export(f'{file_name}.wav', format='wav')

    audios = make_chunks(audio, MAX_AUDIO_FILE_MILLISEC)  # 分割音頻文件，每段音頻文件長度為 1 分鐘
    list_chunks = []
    for idx, chunk in enumerate(audios):
        chunk_name = f'{file_name}_{idx}.wav'
        list_chunks.append(chunk_name)
        chunk.export(chunk_name, format='wav')

    return list_chunks


def _get_source_type(source_path: str) -> SourceTypeEnum:
    parsed_result = urlparse(source_path)
    if all([parsed_result.scheme, parsed_result.netloc]):
        return SourceTypeEnum.URL

    return SourceTypeEnum.FILE_PATH


def remove_files(paths: List[str]):
    if not paths:
        return

    for path in paths:
        remove(path)
