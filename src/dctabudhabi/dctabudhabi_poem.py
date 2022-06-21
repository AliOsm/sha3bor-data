from typing import List, Union

from playwright.sync_api import ElementHandle, Page

from src.poem import Poem
from src.utils.process_utils import process_part


class DctAbuDhabiPoem(Poem):
    def __init__(self, url: str, **kwargs: Union[bool, int]) -> None:
        super().__init__(url, **kwargs)

        self.description = ''
        self.diwan = ''
        self.rhyme = ''

    def extract_poem_info(self, page: Page) -> None:
        page.wait_for_selector('.poem-verses', timeout=1500)

        self.__extract_description(page)
        self.__process_search_keys(page)
        self.__extract_verses(page)

    def __extract_description(self, page: Page) -> None:
        try:
            page.click('"اقرأ المزيد ..."', timeout=1500)
            self.description = (
                page.query_selector('text=عن القصيدة')
                .query_selector('xpath=..')
                .query_selector('.text-body')
                .text_content()
                .strip()
            )
            page.click('button.mat-focus-indicator.mat-button.mat-button-base', timeout=1500)
        except Exception:
            pass

    def __process_search_keys(self, page: Page) -> None:
        search_elements = page.query_selector(
            'div.margin-y-base-s.d-flex.align-items-center.flex-wrap'
        ).query_selector_all('.search-keys__col a')

        for search_element in search_elements:
            if 'diwan' in search_element.get_attribute('href'):
                self.diwan = search_element.text_content().strip()
            elif 'bahr' in search_element.get_attribute('href') or 'subBahr' in search_element.get_attribute('href'):
                self.meter = search_element.text_content().strip()

    def __extract_verses(self, page: Page) -> None:
        parts_elements = page.query_selector_all('.poem-verses__part')

        if page.query_selector('.poem-verses__part--single'):
            parts_strings = self.__extract_mashtoora_poem_parts(parts_elements)
            self.mashtoora = 'نعم'
        else:
            parts_strings = self.__extract_normal_poem_parts(parts_elements)

        self.__build_verses(parts_strings)

    def __extract_normal_poem_parts(self, parts_elements: List[ElementHandle]) -> List[str]:
        parts_strings = list(map(lambda x: x.text_content(), parts_elements))

        if len(parts_strings) % 2 == 1:
            parts_strings.append('')

        return parts_strings

    def __extract_mashtoora_poem_parts(self, parts_elements: List[ElementHandle]) -> List[str]:
        parts_strings = list()

        for part_string in list(map(lambda x: x.text_content(), parts_elements)):
            parts_strings.append(part_string)
            parts_strings.append('')

        return parts_strings

    def __build_verses(self, parts_strings: List[str]) -> None:
        parts_strings = list(map(process_part, parts_strings))

        is_mashtoora = True
        for i in range(1, len(parts_strings), 2):
            if parts_strings[i] != '':
                is_mashtoora = False

        if is_mashtoora:
            self.mashtoora = 'نعم'

        parts_strings_iter = iter(parts_strings)

        for first_part, second_part in zip(parts_strings_iter, parts_strings_iter):
            if '\n' in first_part or '\n' in second_part:
                self.verses = list()
                break

            self.verses.append((first_part, second_part))

        if len(self.verses) == 0:
            print(f'تم العثور على قصيدة لا تحتوي على أي أبيات: {self.url}.')
