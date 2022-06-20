from typing import List, Tuple, Union

from playwright.sync_api import ElementHandle, Page

from src.poet import Poet

from src.dctabudhabi.constants import DCTABUDHABI_ROOT
from src.dctabudhabi.dctabudhabi_poem import DctAbuDhabiPoem


class DctAbuDhabiPoet(Poet):
    def __init__(self, name: str, url: str, **kwargs: Union[bool, int]) -> None:
        super().__init__(name, url, **kwargs)

    def extract_poet_info(self, page: Page) -> None:
        page.wait_for_selector('.search-key')
        list(map(lambda rhyme_info: self.__process_rhyme_element(page, rhyme_info), self.__extract_rhymes_info(page)))

    def __extract_rhymes_info(self, page: Page) -> List[Tuple[str, str]]:
        h2_elements = page.query_selector_all('h2')

        search_keys = None
        for h2_element in h2_elements:
            if h2_element.text_content().strip() == 'القوافي':
                search_keys = h2_element.query_selector('xpath=../../../..').query_selector_all('.search-key')

        if not search_keys:
            print(f'تم العثور على شاعر لا يمتلك أي قوافي: {self.name}')
            return list()

        rhymes = list()

        for search_key in search_keys:
            rhyme_url = f"{DCTABUDHABI_ROOT}/{search_key.get_attribute('href')}"
            rhyme_url = rhyme_url.replace('pageSize=30', 'pageSize=5000')
            rhymes.append((search_key.text_content().strip(), rhyme_url))

        return rhymes

    def __process_rhyme_element(self, page: Page, rhyme_info: Tuple[str, str]) -> None:
        rhyme, rhyme_url = rhyme_info

        page.goto(rhyme_url)

        try:
            page.click('"استمر بالتصفّح"', timeout=500)
        except Exception:
            pass

        page.wait_for_selector('.base-card__title')

        list(
            map(
                lambda poem_element: self.__process_poem_element(poem_element, rhyme),
                self.__get_poems_elements(page, rhyme),
            ),
        )

        page.wait_for_timeout(self.sleep_time)

    def __get_poems_elements(self, page: Page, rhyme: str) -> List[ElementHandle]:
        poems_elements = page.query_selector_all('.base-card__title')

        if len(poems_elements) == 0:
            print(f'تم العثور على قافية لا تمتلك أي قصائد للشاعر {self.name}: {rhyme}.')

        return poems_elements

    def __process_poem_element(self, poem_element: ElementHandle, rhyme: str) -> None:
        poem_url = f"{DCTABUDHABI_ROOT}/{poem_element.query_selector('a').get_attribute('href')}"

        poem = DctAbuDhabiPoem(
            poem_url,
            headless=self.headless,
            max_retries=self.max_retries,
            sleep_time=self.sleep_time,
        )

        poem.rhyme = rhyme

        self.poems.append(poem)
