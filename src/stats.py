import os
import pandas as pd

from abc import ABC, abstractmethod

from src.processor import Processor
from src.utils.process_utils import diacritization_stats


class Stats(ABC):
    def __init__(self) -> None:
        self.data: pd.DataFrame = None

        self.input_file_name = ''
        self.processor: Processor = None

    @abstractmethod
    def calculate(self) -> None:
        self.data = self.read_data()

        self.data = self.processor.process(self.data)

        print(
            f"عدد الأشطر: {len(self.data[self.data['الصدر'].notna()]) + len(self.data[self.data['العجز'].notna()]):,}"
        )
        print(f"عدد الأبيات: {len(self.data):,}")
        print(f"عدد القصائد: {len(self.data.groupby('القصيدة')):,}")
        print(f"عدد الشعراء: {len(self.data['الشاعر'].unique()):,}")
        print(f"عدد العصور: {len(self.data['العصر'].unique()):,}")
        print(f"عدد البحور: {len(self.data['البحر'].unique()):,}")
        print(f"عدد الأبيات غير محددة البحر: {len(self.data[self.data['البحر'] == 'غير محدد']):,}")
        print(f"عدد القصائد غير محددة البحر: {len(self.data[self.data['البحر'] == 'غير محدد'].groupby('القصيدة')):,}")
        print(f"عدد الأبيات المشطورة: {len(self.data[self.data['العجز'] == '']):,}")
        print(f"عدد القصائد المشطورة: {len(self.data[self.data['العجز'] == ''].groupby('القصيدة')):,}")

        characters_count = 0
        diacritized_characters_count = 0
        diacritization_percentage_25 = 0
        diacritization_percentage_50 = 0
        diacritization_percentage_75 = 0

        for text in self.data['الصدر'] + ' ' + self.data['العجز']:
            (
                text_characters_count,
                text_diacritized_characters_count,
                text_diacritization_percentage,
            ) = diacritization_stats(text)

            characters_count += text_characters_count
            diacritized_characters_count += text_diacritized_characters_count
            diacritization_percentage_25 += text_diacritization_percentage >= 0.25
            diacritization_percentage_50 += text_diacritization_percentage >= 0.5
            diacritization_percentage_75 += text_diacritization_percentage >= 0.75

        print(f'نسبة الحروف المشكلة: {diacritized_characters_count / characters_count * 100:.2f}%')
        print(f'عدد الأبيات المشكلة بنسبة أكثر من 24%: {diacritization_percentage_25:,}')
        print(f'عدد الأبيات المشكلة بنسبة أكثر من 49%: {diacritization_percentage_50:,}')
        print(f'عدد الأبيات المشكلة بنسبة أكثر من 74%: {diacritization_percentage_75:,}')

    def read_data(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join('data', self.input_file_name), sep='\t')
