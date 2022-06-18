from typing import List, Union

from playwright.sync_api import ElementHandle, Page

from era import Era

from aldiwan.constants import ALDIWAN_ROOT
from aldiwan.aldiwan_poet import AldiwanPoet


class AldiwanEra(Era):
    def __init__(self, name: str, url: str, **kwargs: Union[bool, int]) -> None:
        super().__init__(name, url, **kwargs)

    def extract_era_info(self, page: Page) -> None:
        list(map(self.__process_poet_element, self.__get_poets_elements(page)))

    def __get_poets_elements(self, page: Page) -> List[ElementHandle]:
        poets_elements = page.query_selector_all('.button-menu-follow')
        poets_elements = [poet_element.query_selector('xpath=..') for poet_element in poets_elements]

        if len(poets_elements) == 0:
            print(f'تم العثور على عصر لا يحتوي على أي شعراء: {self.name}.')

        return poets_elements

    def __process_poet_element(self, poet_element: ElementHandle) -> None:
        poet_name = poet_element.query_selector_all('a')[0].text_content().strip()
        poet_url = f"{ALDIWAN_ROOT}/{poet_element.query_selector_all('a')[0].get_attribute('href')}"

        self.poets.append(
            AldiwanPoet(
                poet_name,
                poet_url,
                headless=self.headless,
                max_retries=self.max_retries,
                sleep_time=self.sleep_time,
            ),
        )
