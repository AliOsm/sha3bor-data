from typing import Callable

from fake_useragent import UserAgent
from playwright.sync_api import Page, sync_playwright


ua = UserAgent()


def scroll_to_page_end(page: Page) -> None:
    add_scrolling_interval(page)
    wait_for_scrolling(page)
    remove_scrolling_interval(page)


def add_scrolling_interval(page: Page) -> None:
    page.evaluate(
        """
        var scrollingInterval = setInterval(function () {
            var scrollingElement = (document.scrollingElement || document.body);
            scrollingElement.scrollTop = scrollingElement.scrollHeight;
        }, 100);
        """
    )


def remove_scrolling_interval(page: Page) -> None:
    page.evaluate('clearInterval(scrollingInterval)')


def wait_for_scrolling(page: Page) -> None:
    previous_height = -1
    current_height = get_page_height(page)

    while previous_height != current_height:
        previous_height, current_height = current_height, get_page_height(page)
        page.wait_for_timeout(1500)


def get_page_height(page: Page) -> int:
    return page.evaluate('(window.innerHeight + window.scrollY)')


def process_page_with_retry(url: str, processor: Callable, headless: bool, max_retries: int, sleep_time: int) -> bool:
    retry_count = 0

    while retry_count < max_retries:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=headless)
                context = browser.new_context(user_agent=ua.random)
                page = context.new_page()

                page.goto(url, timeout=0)

                processor(page)

                page.wait_for_timeout(sleep_time)

                browser.close()

                return True
        except Exception:
            retry_count += 1

    return False
