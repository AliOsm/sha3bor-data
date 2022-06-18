from typing import List, Union

from playwright.sync_api import ElementHandle, Page

from poet import Poet

from aldiwan.constants import ALDIWAN_ROOT
from aldiwan.aldiwan_poem import AldiwanPoem


class AldiwanPoet(Poet):
    def __init__(self, name: str, url: str, **kwargs: Union[bool, int]) -> None:
        super().__init__(name, url, **kwargs)

    def extract_poet_info(self, page: Page) -> None:
        list(map(self.__process_poem_element, self.__get_poems_elements(page)))

    def __get_poems_elements(self, page: Page) -> List[ElementHandle]:
        poems_elements = (
            page.query_selector_all('.s-menu1')[-1].query_selector_all('.content')[0].query_selector_all('.record')
        )

        if len(poems_elements) == 0:
            print(f'تم العثور على شاعر لا يمتلك أي قصائد: {self.name}.')

        return poems_elements

    def __process_poem_element(self, poem_element: ElementHandle) -> None:
        poem_url = poem_element.query_selector_all('a')[0].get_attribute('href')

        self.poems.append(
            AldiwanPoem(
                f'{ALDIWAN_ROOT}/{poem_url}',
                headless=self.headless,
                max_retries=self.max_retries,
                sleep_time=self.sleep_time,
            ),
        )
