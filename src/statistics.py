import argparse

from typing import Type

from src.stats import Stats

from src.adabworld.adabworld_stats import AdabWorldStats
from src.aldiwan.aldiwan_stats import AldiwanStats


def get_website_stats_class(website: str) -> Type[Stats]:
    if website == 'adabworld':
        return AdabWorldStats
    elif website == 'aldiwan':
        return AldiwanStats
    # elif website == 'dctabudhabi':
    #     return DctAbuDhabiCrawler
    else:
        raise ValueError(f'الموقع "{website}" غير مدعوم.')


def main(args: argparse.Namespace) -> None:
    crawler_class = get_website_stats_class(args.website)
    crawler_class().calculate()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--website',
        required=True,
        choices=['adabworld', 'aldiwan', 'dctabudhabi'],
        help='الموقع الذي يجب جمع البيانات منه.',
    )
    args = parser.parse_args()

    main(args)
