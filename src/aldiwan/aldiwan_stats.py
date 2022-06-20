from src.stats import Stats

from src.aldiwan.aldiwan_processor import AldiwanProcessor


class AldiwanStats(Stats):
    def __init__(self) -> None:
        super().__init__()

        self.input_file_name = 'aldiwan.csv'
        self.processor = AldiwanProcessor()

    def calculate(self) -> None:
        super().calculate()

        print(f"عدد الأنواع: {len(self.data['النوع'].unique()):,}")
        print(f"عدد الأبيات غير محددة النوع: {len(self.data[self.data['النوع'] == 'غير محدد']):,}")
        print(f"عدد القصائد غير محددة النوع: {len(self.data[self.data['النوع'] == 'غير محدد'].groupby('القصيدة')):,}")

        print(f"عدد المواضيع: {len(self.data['الموضوع'].unique()):,}")
        print(f"عدد الأبيات غير محددة الموضوع: {len(self.data[self.data['الموضوع'] == 'غير محدد']):,}")
        print(
            f"عدد القصائد غير محددة الموضوع: {len(self.data[self.data['الموضوع'] == 'غير محدد'].groupby('القصيدة')):,}"
        )

        print(f"عدد القوافي: {len(self.data['القافية'].unique()):,}")
        print(f"عدد الأبيات غير محددة القافية: {len(self.data[self.data['القافية'] == 'غير محدد']):,}")
        print(
            f"عدد القصائد غير محددة القافية: {len(self.data[self.data['القافية'] == 'غير محدد'].groupby('القصيدة')):,}"
        )
