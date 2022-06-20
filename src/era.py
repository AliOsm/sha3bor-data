from typing import List
from abc import ABC, abstractmethod

from tqdm import tqdm
from playwright.sync_api import Page

from src.poet import Poet
from src.utils.pw_utils import process_page_with_retry


class Era(ABC):
    def __init__(self, name: str, url: str, headless: bool, max_retries: int, sleep_time: int) -> None:
        self.name = name
        self.url = url
        self.poets: List[Poet] = list()

        self.headless = headless
        self.max_retries = max_retries
        self.sleep_time = sleep_time

    @abstractmethod
    def extract_era_info(self, page: Page) -> None:
        pass

    def process_era_page(self) -> None:
        print(f'يتم حاليا معالجة العصر: {self.name}.')

        successful_processing = process_page_with_retry(
            self.url,
            self.extract_era_info,
            self.headless,
            self.max_retries,
            self.sleep_time,
        )

        if not successful_processing:
            print(f'لا يمكن معالجة العصر: {self.name}.')

    def process_poets_pages(self) -> None:
        print('بدء معالجة الشعراء.')
        for poet in tqdm(self.poets):
            poet.process_poet_page()

    def process_poems_pages(self) -> None:
        print('بدء معالجة القصائد.')
        for poet in tqdm(self.poets):
            for poem in tqdm(poet.poems, leave=False):
                poem.process_poem_page()

    def __str__(self) -> str:
        return f'العصر {self.name}: {self.url}.'
