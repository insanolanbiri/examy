import lxml.html

from examy.models.fetcher import SeleniumCompatibleFetcher


class OptimizedNewTypeFetcher(SeleniumCompatibleFetcher):
    result_page_layout = "new"
    fetcher_codename = "optimized"

    @SeleniumCompatibleFetcher.requires_driver
    @SeleniumCompatibleFetcher.check_fetch_arguments
    def fetch(self, student, exam_descriptor, login_kwargs: dict | None = None, *args, **kwargs):
        if login_kwargs is None:
            login_kwargs = {}

        from examy.fetchers.new_web_layout.utils.webpage_actions import (
            login,
            get_result_page_address,
            logout,
        )
        from examy.fetchers.new_web_layout.utils.process_html import process_result_html
        import requests

        login(self.driver, student, exam_descriptor, **login_kwargs)

        try:
            address = get_result_page_address(self.driver, exam_descriptor)
        finally:
            logout(self.driver, exam_descriptor)

        response = requests.get(address, allow_redirects=False, headers={"User-Agent": "Mozilla/5.0"})

        root = lxml.html.fromstring(response.content)

        result = process_result_html(root, student, exam_descriptor)

        return result
