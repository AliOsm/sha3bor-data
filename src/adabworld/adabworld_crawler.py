from typing import Union

from crawler import Crawler

from adabworld.constants import ERAS
from adabworld.adabworld_era import AdabWorldEra


class AdabworldCrawler(Crawler):
    def __init__(self, **kwargs: Union[bool, int]) -> None:
        super().__init__(**kwargs)

        self.eras = [
            AdabWorldEra(
                name,
                url,
                headless=self.headless,
                max_retries=self.max_retries,
                sleep_time=self.sleep_time,
            )
            for name, url in ERAS
        ]
        self.output_file_name = 'adabworld.csv'
        self.poem_attributes_header = ['مشطورة', 'البحر']
        self.poem_attributes = ['mashtoora', 'meter']
