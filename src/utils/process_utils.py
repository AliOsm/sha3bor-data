import re

from typing import Tuple

from pyarabic.araby import LETTERS, TASHKEEL, strip_tatweel

from constants import POSSIBLE_DIACRITIZATION


def process_part(part: str) -> str:
    part = re.sub(r'\s+', ' ', part.strip())
    part = strip_tatweel(part)

    while len(part) > 0 and (part[0] in TASHKEEL or part[0] == '.'):
        part = part[1:]

    return process_diacritics(part)


def process_diacritics(part: str) -> str:
    characters = list()
    diacritics = list()

    i = 0
    while i < len(part):
        if part[i] not in TASHKEEL:
            characters.append(part[i])
            i += 1

            character_diacritics = ''
            while i < len(part) and part[i] in TASHKEEL:
                character_diacritics += part[i]
                i += 1

            if len(character_diacritics) > 2:
                print(f'تم العثور على حرف يمتلك أكثر من حركتين: {character_diacritics}.')
                character_diacritics = character_diacritics[:2]

            if character_diacritics not in POSSIBLE_DIACRITIZATION:
                character_diacritics = character_diacritics[::-1]

            if character_diacritics in POSSIBLE_DIACRITIZATION:
                diacritics.append(character_diacritics)
            else:
                diacritics.append('')
        else:
            i += 1

    return ''.join([c + d for c, d in zip(characters, diacritics)])


def diacritization_stats(text: str) -> Tuple[int, int, float]:
    characters_count = 0
    diacritized_characters_count = 0

    i = 0
    while i < len(text):
        if text[i] not in TASHKEEL and text[i] in LETTERS:
            characters_count += 1
            i += 1

            diacritics_exist = False
            while i < len(text) and text[i] in TASHKEEL:
                diacritics_exist = True
                i += 1

            diacritized_characters_count += diacritics_exist
        else:
            i += 1

    return (characters_count, diacritized_characters_count, diacritized_characters_count / max(characters_count, 1))
