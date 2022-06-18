from typing import List, Tuple
from abc import ABC, abstractmethod

from playwright.sync_api import Page

from utils.pw_utils import process_page_with_retry


class Poem(ABC):
    def __init__(self, url: str, headless: bool, max_retries: int, sleep_time: int) -> None:
        self.url = url
        self.mashtoora = 'لا'
        self.meter = ''
        self.verses: List[Tuple[str, str]] = list()

        self.headless = headless
        self.max_retries = max_retries
        self.sleep_time = sleep_time

    @abstractmethod
    def extract_poem_info(self, page: Page) -> None:
        pass

    def process_poem_page(self) -> None:
        successful_processing = process_page_with_retry(
            self.url,
            self.extract_poem_info,
            self.headless,
            self.max_retries,
            self.sleep_time,
        )

        if not successful_processing:
            print(f'لا يمكن معالجة القصيدة: {self.url}.')

    def __str__(self) -> str:
        return f'رابط القصيدة: {self.url}.'
