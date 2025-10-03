from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, base_url: str) -> None:
        self.page.goto(base_url)

    def title(self) -> str:
        return self.page.title()
