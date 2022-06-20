import argparse

from typing import Type

from src.crawler import Crawler

from src.adabworld.adabworld_crawler import AdabworldCrawler
from src.aldiwan.aldiwan_crawler import AldiwanCrawler
from src.dctabudhabi.dctabudhabi_crawler import DctAbuDhabiCrawler


def get_website_crawler_class(website: str) -> Type[Crawler]:
    if website == 'adabworld':
        return AdabworldCrawler
    elif website == 'aldiwan':
        return AldiwanCrawler
    elif website == 'dctabudhabi':
        return DctAbuDhabiCrawler
    else:
        raise ValueError(f'الموقع "{website}" غير مدعوم.')


def main(args: argparse.Namespace) -> None:
    crawler_class = get_website_crawler_class(args.website)
    del args.website
    crawler_class(**vars(args)).crawl()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--website',
        required=True,
        choices=['adabworld', 'aldiwan', 'dctabudhabi'],
        help='الموقع الذي يجب جمع البيانات منه.',
    )
    parser.add_argument(
        '--no_headless',
        action='store_true',
        help='بتمرير هذا الخيار، سيتم إظهار صفحات المتصفح على الشاشة. يُنصح باستخدامه خلال عملية التطوير فقط.',
    )
    parser.add_argument('--max_retries', default=3, type=int, help='العدد الأقصى من المحاولات لمعالجة صفحة معينة.')
    parser.add_argument(
        '--sleep_time',
        default=500,
        type=int,
        help='المدة الزمنية التي يجب انتظارها قبل معالجة الصفحة التالية. يتم التعبير عن الرقم بوحدة الميلي ثانية.',
    )
    args = parser.parse_args()

    args.headless = not args.no_headless
    del args.no_headless

    main(args)
