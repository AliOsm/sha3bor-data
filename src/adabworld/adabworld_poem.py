from typing import List, Union

from playwright.sync_api import ElementHandle, Page

from src.poem import Poem
from src.utils.process_utils import process_part


class AdabWorldPoem(Poem):
    def __init__(self, url: str, **kwargs: Union[bool, int]) -> None:
        super().__init__(url, **kwargs)

    def extract_poem_info(self, page: Page) -> None:
        self.__extract_meter(page)
        self.__extract_verses(page)

    def __extract_meter(self, page: Page) -> None:
        tags_elements = page.query_selector_all('.jeg_post_tags')[0].query_selector_all('a')

        for tag_element in tags_elements:
            text = tag_element.text_content().strip()
            if text.startswith('بحر'):
                self.meter = ' '.join(text.split()[1:])
                break

    def __extract_verses(self, page: Page) -> None:
        parts_elements = page.query_selector_all('.poem')[0].query_selector_all('p')

        if len(parts_elements) == 0:
            parts_elements = page.query_selector_all('.poem')[0].query_selector_all('h3')

        if len(parts_elements) > 1:
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
        parts_strings = list()

        for part_string in parts_elements[0].text_content().strip().split('\n'):
            parts_strings.append(part_string)
            parts_strings.append('')

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
