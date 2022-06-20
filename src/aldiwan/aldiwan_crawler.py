from typing import Union

from src.crawler import Crawler

from src.aldiwan.constants import ERAS
from src.aldiwan.aldiwan_era import AldiwanEra


class AldiwanCrawler(Crawler):
    def __init__(self, **kwargs: Union[bool, int]) -> None:
        super().__init__(**kwargs)

        self.eras = [
            AldiwanEra(
                name,
                url,
                headless=self.headless,
                max_retries=self.max_retries,
                sleep_time=self.sleep_time,
            )
            for name, url in ERAS
        ]
        self.output_file_name = 'aldiwan.csv'
        self.poem_attributes_header = ['النوع', 'مشطورة', 'الموضوع', 'البحر', 'القافية']
        self.poem_attributes = ['type', 'mashtoora', 'category', 'meter', 'rhyme']
