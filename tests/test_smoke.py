import os
import pytest
from playwright.sync_api import sync_playwright
from tests.pages.home_page import HomePage


BASE_URL = os.getenv("BASE_URL", "")
EXPECTED_TITLE = os.getenv("EXPECTED_TITLE", "")


@pytest.mark.skipif(not BASE_URL, reason="BASE_URL not set")
def test_home_title():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        home = HomePage(page)
        home.goto(BASE_URL)
        title = home.title()
        if EXPECTED_TITLE:
            assert EXPECTED_TITLE in title
        else:
            assert len(title) > 0
        browser.close()
