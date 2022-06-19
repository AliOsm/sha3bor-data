import pandas as pd

from stats import Stats

from aldiwan.constants import RHYME_MAPPING


class AldiwanStats(Stats):
    def __init__(self) -> None:
        super().__init__()

        self.input_file_name = 'aldiwan.csv'

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data.loc[data['النوع'].isna(), 'النوع'] = 'غير محدد'
        data.loc[data['الموضوع'].isna(), 'الموضوع'] = 'غير محدد'

        data.loc[data['القافية'].isna(), 'القافية'] = 'غير محدد'
        data.loc[data['القافية'] == '(#)', 'القافية'] = 'غير محدد'
        data.loc[data['القافية'] == '(1)', 'القافية'] = 'غير محدد'

        for rhyme_mapping in RHYME_MAPPING:
            data.loc[data['القافية'].isin(rhyme_mapping[0]), 'القافية'] = rhyme_mapping[1]

        return data

    def calculate_custom_stats(self, data: pd.DataFrame) -> None:
        print(f"عدد الأنواع: {len(data['النوع'].unique()):,}")
        print(f"عدد الأبيات غير محددة النوع: {len(data[data['النوع'] == 'غير محدد']):,}")
        print(f"عدد القصائد غير محددة النوع: {len(data[data['النوع'] == 'غير محدد'].groupby('القصيدة')):,}")

        print(f"عدد المواضيع: {len(data['الموضوع'].unique()):,}")
        print(f"عدد الأبيات غير محددة الموضوع: {len(data[data['الموضوع'] == 'غير محدد']):,}")
        print(f"عدد القصائد غير محددة الموضوع: {len(data[data['الموضوع'] == 'غير محدد'].groupby('القصيدة')):,}")

        print(f"عدد القوافي: {len(data['القافية'].unique()):,}")
        print(f"عدد الأبيات غير محددة القافية: {len(data[data['القافية'] == 'غير محدد']):,}")
        print(f"عدد القصائد غير محددة القافية: {len(data[data['القافية'] == 'غير محدد'].groupby('القصيدة')):,}")
