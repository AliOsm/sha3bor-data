import pandas as pd

from src.processor import Processor


class AdabWorldProcessor(Processor):
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        data = super().process(data)

        data.loc[data['البحر'] == '؟', 'البحر'] = 'غير محدد'

        return data
