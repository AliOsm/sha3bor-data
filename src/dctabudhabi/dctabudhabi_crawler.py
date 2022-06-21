from typing import Union

from src.crawler import Crawler

from src.dctabudhabi.constants import ERAS
from src.dctabudhabi.dctabudhabi_era import DctAbuDhabiEra


class DctAbuDhabiCrawler(Crawler):
    def __init__(self, **kwargs: Union[bool, int]) -> None:
        super().__init__(**kwargs)

        self.eras = [
            DctAbuDhabiEra(
                name,
                url,
                headless=self.headless,
                max_retries=self.max_retries,
                sleep_time=self.sleep_time,
            )
            for name, url in ERAS
        ]
        self.output_file_name = 'dctabudhabi.tsv'
        self.poem_attributes_header = ['الديوان', 'مشطورة', 'الوصف', 'البحر', 'القافية']
        self.poem_attributes = ['diwan', 'mashtoora', 'description', 'meter', 'rhyme']
