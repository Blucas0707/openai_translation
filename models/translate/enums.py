from enum import auto

from utils.enums import TextEnum


class SourceTypeEnum(TextEnum):
    URL = auto()
    FILE_PATH = auto()


class TranscribeSourceFileFormatEnum(TextEnum):
    MP4 = auto()


class TranslationSourceFileFormatEnum(TextEnum):
    TXT = auto()
