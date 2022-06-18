from typing import List
from abc import ABC, abstractmethod

from playwright.sync_api import Page

from poem import Poem
from utils.pw_utils import process_page_with_retry


class Poet(ABC):
    def __init__(self, name: str, url: str, headless: bool, max_retries: int, sleep_time: int) -> None:
        self.name = name
        self.url = url
        self.poems: List[Poem] = list()

        self.headless = headless
        self.max_retries = max_retries
        self.sleep_time = sleep_time

    @abstractmethod
    def extract_poet_info(self, page: Page) -> None:
        pass

    def process_poet_page(self) -> None:
        print(f'يتم حاليا معالجة الشاعر: {self.name}.')

        successful_processing = process_page_with_retry(
            self.url,
            self.extract_poet_info,
            self.headless,
            self.max_retries,
            self.sleep_time,
        )

        if not successful_processing:
            print(f'لا يمكن معالجة الشاعر: {self.name}.')

    def __str__(self) -> str:
        return f'الشاعر {self.name}: {self.url}.'
