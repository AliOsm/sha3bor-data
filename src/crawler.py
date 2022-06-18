import os
import csv

from typing import List, Union
from abc import ABC, abstractmethod

from era import Era


class Crawler(ABC):
    @abstractmethod
    def __init__(self, headless: bool, max_retries: int, sleep_time: int) -> None:
        self.data: List[List[Union[str, int]]] = list()

        self.eras: List[Era] = list()
        self.output_file_name = ''
        self.poem_attributes_header: List[str] = list()
        self.poem_attributes: List[str] = list()

        self.headless = headless
        self.max_retries = max_retries
        self.sleep_time = sleep_time

    def crawl(self) -> None:
        self.__process_pages()
        self.__prepare_data()
        self.__write_data()

    def __process_pages(self) -> None:
        for era in self.eras:
            era.process_era_page()
            era.process_poets_pages()
            era.process_poems_pages()

    def __prepare_data(self) -> None:
        self.data.append(
            [
                'القصيدة',
                'العصر',
                'الشاعر',
            ]
            + self.poem_attributes_header
            + [
                'الصدر',
                'العجز',
            ]
        )

        poem_id = 1
        for era in self.eras:
            for poet in era.poets:
                for poem in poet.poems:
                    if len(poem.verses) > 0:
                        for verse in poem.verses:
                            self.data.append(
                                [
                                    str(poem_id),
                                    era.name,
                                    poet.name,
                                ]
                                + [getattr(poem, attribute) for attribute in self.poem_attributes]
                                + list(verse)
                            )
                        poem_id += 1

    def __write_data(self) -> None:
        with open(os.path.join('data', self.output_file_name), 'w') as fp:
            csv.writer(fp, delimiter='\t').writerows(self.data)
