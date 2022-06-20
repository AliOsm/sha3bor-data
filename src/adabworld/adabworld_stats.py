from src.stats import Stats

from src.adabworld.adabworld_processor import AdabWorldProcessor


class AdabWorldStats(Stats):
    def __init__(self) -> None:
        super().__init__()

        self.input_file_name = 'adabworld.csv'
        self.processor = AdabWorldProcessor()

    def calculate(self) -> None:
        super().calculate()
