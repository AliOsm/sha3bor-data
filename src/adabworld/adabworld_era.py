from typing import List, Union

from playwright.sync_api import ElementHandle, Page

from src.era import Era

from src.adabworld.constants import ADABWORLD_ROOT
from src.adabworld.adabworld_poet import AdabWorldPoet


class AdabWorldEra(Era):
    def __init__(self, name: str, url: str, **kwargs: Union[bool, int]) -> None:
        super().__init__(name, url, **kwargs)

    def extract_era_info(self, page: Page) -> None:
        list(map(self.__process_poet_element, self.__get_poets_elements(page)))

    def __get_poets_elements(self, page: Page) -> List[ElementHandle]:
        poets_elements = page.query_selector_all('.c-card-author-mini')

        if len(poets_elements) == 0:
            print(f'تم العثور على عصر لا يحتوي على أي شعراء: {self.name}.')

        return poets_elements

    def __process_poet_element(self, poet_element: ElementHandle) -> None:
        poet_name = poet_element.query_selector('.c-card-author-mini__name').text_content().strip()
        poet_url = f"{ADABWORLD_ROOT}{poet_element.get_attribute('href')}"

        self.poets.append(
            AdabWorldPoet(
                poet_name,
                poet_url,
                headless=self.headless,
                max_retries=self.max_retries,
                sleep_time=self.sleep_time,
            ),
        )
