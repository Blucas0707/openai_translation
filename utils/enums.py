from enum import Enum


class TextEnum(Enum):
    def __str__(self):
        return self.value

    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_all_values(cls):
        return [e.value for e in cls]

    @classmethod
    def get_all_keys(cls):
        return [e.name for e in cls]
