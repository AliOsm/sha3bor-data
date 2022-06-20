import pandas as pd

from src.processor import Processor

from src.aldiwan.constants import RHYME_MAPPING


class AldiwanProcessor(Processor):
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        data = super().process(data)

        data.loc[data['النوع'].isna(), 'النوع'] = 'غير محدد'
        data.loc[data['الموضوع'].isna(), 'الموضوع'] = 'غير محدد'

        data.loc[data['القافية'].isna(), 'القافية'] = 'غير محدد'
        data.loc[data['القافية'] == '(#)', 'القافية'] = 'غير محدد'
        data.loc[data['القافية'] == '(1)', 'القافية'] = 'غير محدد'

        for rhyme_mapping in RHYME_MAPPING:
            data.loc[data['القافية'].isin(rhyme_mapping[0]), 'القافية'] = rhyme_mapping[1]

        return data
