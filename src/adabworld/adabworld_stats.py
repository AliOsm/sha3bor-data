import pandas as pd

from src.stats import Stats


class AdabWorldStats(Stats):
    def __init__(self) -> None:
        super().__init__()

        self.input_file_name = 'adabworld.csv'

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data.loc[data['البحر'] == '؟', 'البحر'] = 'غير محدد'

        return data

    def calculate_custom_stats(self, _) -> None:
        pass
