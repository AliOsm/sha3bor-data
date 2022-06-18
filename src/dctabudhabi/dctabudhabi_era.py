from typing import List, Union

from pyarabic.araby import strip_tashkeel
from playwright.sync_api import ElementHandle, Page

from era import Era

from dctabudhabi.constants import DCTABUDHABI_ROOT
from dctabudhabi.dctabudhabi_poet import DctAbuDhabiPoet


class DctAbuDhabiEra(Era):
    def __init__(self, name: str, url: str, **kwargs: Union[bool, int]) -> None:
        super().__init__(name, url, **kwargs)

    def extract_era_info(self, page: Page) -> None:
        page.wait_for_selector('.author-poems')
        list(map(self.__process_poet_element, self.__get_poets_elements(page)))

    def __get_poets_elements(self, page: Page) -> List[ElementHandle]:
        poets_elements = page.query_selector_all('.author-poems__name')

        if len(poets_elements) == 0:
            print(f'تم العثور على عصر لا يحتوي على أي شعراء: {self.name}.')

        return poets_elements

    def __process_poet_element(self, poet_element: ElementHandle) -> None:
        poet_name = strip_tashkeel(poet_element.query_selector('a').text_content().strip())
        poet_url = f"{DCTABUDHABI_ROOT}/{poet_element.query_selector('a').get_attribute('href')}"

        self.poets.append(
            DctAbuDhabiPoet(
                poet_name,
                poet_url,
                headless=self.headless,
                max_retries=self.max_retries,
                sleep_time=self.sleep_time,
            ),
        )
