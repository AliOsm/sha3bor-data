import re

from pyarabic.araby import TASHKEEL, strip_tatweel

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
