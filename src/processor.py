from abc import ABC, abstractmethod

import pandas as pd


class Processor(ABC):
    @abstractmethod
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        data.loc[data['الصدر'].isna(), 'الصدر'] = ''
        data.loc[data['العجز'].isna(), 'العجز'] = ''
        data.loc[data['البحر'].isna(), 'البحر'] = 'غير محدد'

        return data
