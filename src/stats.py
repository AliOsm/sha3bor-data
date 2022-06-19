import os
import pandas as pd

from abc import ABC, abstractmethod

from utils.process_utils import diacritization_stats


class Stats(ABC):
    def __init__(self) -> None:
        self.input_file_name = ''

    @abstractmethod
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def calculate_custom_stats(self, data: pd.DataFrame) -> None:
        pass

    def calculate(self) -> None:
        data = self.read_data()

        data = self.preprocess_data(data)

        data.loc[data['البحر'].isna(), 'البحر'] = 'غير محدد'
        data.loc[data['الصدر'].isna(), 'الصدر'] = ''
        data.loc[data['العجز'].isna(), 'العجز'] = ''

        print(f"عدد الأشطر: {len(data[data['الصدر'].notna()]) + len(data[data['العجز'].notna()]):,}")
        print(f"عدد الأبيات: {len(data):,}")
        print(f"عدد القصائد: {len(data.groupby('القصيدة')):,}")
        print(f"عدد الشعراء: {len(data['الشاعر'].unique()):,}")
        print(f"عدد العصور: {len(data['العصر'].unique()):,}")
        print(f"عدد البحور: {len(data['البحر'].unique()):,}")
        print(f"عدد الأبيات غير محددة البحر: {len(data[data['البحر'] == 'غير محدد']):,}")
        print(f"عدد القصائد غير محددة البحر: {len(data[data['البحر'] == 'غير محدد'].groupby('القصيدة')):,}")
        print(f"عدد الأبيات المشطورة: {len(data[data['العجز'] == '']):,}")
        print(f"عدد القصائد المشطورة: {len(data[data['العجز'] == ''].groupby('القصيدة')):,}")

        self.calculate_custom_stats(data)

        characters_count = 0
        diacritized_characters_count = 0
        diacritization_percentage_25 = 0
        diacritization_percentage_50 = 0
        diacritization_percentage_75 = 0

        for text in data['الصدر'] + ' ' + data['العجز']:
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
