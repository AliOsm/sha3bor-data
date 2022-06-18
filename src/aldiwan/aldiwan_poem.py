import re

from typing import List, Union

from bs4 import BeautifulSoup
from playwright.sync_api import ElementHandle, Page

from poem import Poem
from utils.process_utils import process_part


class AldiwanPoem(Poem):
    def __init__(self, url: str, **kwargs: Union[bool, int]) -> None:
        super().__init__(url, **kwargs)

        self.type = ''
        self.category = ''
        self.rhyme = ''

    def extract_poem_info(self, page: Page) -> None:
        self.__process_tips(page)
        self.__extract_verses(page)

    def __process_tips(self, page: Page) -> None:
        tips_elements = page.query_selector_all('.tips')[0].query_selector_all('a')

        for tip_element in tips_elements:
            text = tip_element.text_content().strip()
            value = ' '.join(text.split()[1:])

            if text.startswith('قصائد'):
                self.category = value
            elif text.startswith('بحر'):
                self.meter = value
            elif text.startswith('قافية'):
                self.rhyme = value
            else:
                self.type = text

    def __extract_verses(self, page: Page) -> None:
        parts_elements = page.query_selector('#poem_content').query_selector_all('h3')

        if len(parts_elements) == 0:
            parts_elements = page.query_selector('#poem_content').query_selector_all('h4')

        if len(parts_elements) > 0:
            parts_strings = self.__extract_normal_poem_parts(parts_elements)
        else:
            parts_strings = self.__extract_mashtoora_poem_parts(parts_elements)
            self.mashtoora = 'نعم'

        self.__build_verses(parts_strings)

    def __extract_normal_poem_parts(self, parts_elements: List[ElementHandle]) -> List[str]:
        parts_strings = list(map(lambda x: x.text_content(), parts_elements))
        parts_strings = list(map(process_part, parts_strings))

        if len(parts_strings) % 2 == 1:
            parts_strings.append('')

        return parts_strings

    def __extract_mashtoora_poem_parts(self, parts_elements: List[ElementHandle]) -> List[str]:
        parts_element = parts_elements[0]

        soup = BeautifulSoup(parts_element.inner_html().replace('<br>', '\n'), features='lxml')

        parts_strings = list()

        for part_string in re.sub('\n+', '\n', soup.text.strip()).split('\n'):
            parts_strings.append(part_string)
            parts_strings.append('')

        parts_strings = list(map(process_part, parts_strings))

        return parts_strings

    def __build_verses(self, parts_strings: List[str]) -> None:
        parts_strings_iter = iter(parts_strings)

        for first_part, second_part in zip(parts_strings_iter, parts_strings_iter):
            if '\n' in first_part or '\n' in second_part:
                self.verses = list()
                break

            self.verses.append((first_part, second_part))

        if len(self.verses) == 0:
            print(f'تم العثور على قصيدة لا تحتوي على أي أبيات: {self.url}.')
