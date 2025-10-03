import os
import io
import math
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright


FIGMA_BASELINE_PATH = os.getenv("FIGMA_BASELINE_PATH", ".playwright/figma_baseline.png")
BASE_URL = os.getenv("BASE_URL", "")
VISUAL_TOLERANCE = float(os.getenv("VISUAL_TOLERANCE", "0.01"))  # 1% default


def images_similar(img1: Image.Image, img2: Image.Image, tolerance: float) -> bool:
    if img1.size != img2.size:
        return False
    diff = ImageChops.difference(img1, img2).convert("L")
    # Calculate normalized mean absolute error
    hist = diff.histogram()
    total_pixels = img1.size[0] * img1.size[1]
    total = 0
    for i, count in enumerate(hist):
        total += i * count
    nmae = total / (255.0 * total_pixels)
    return nmae <= tolerance


def test_visual_against_figma_baseline():
    if not BASE_URL or not os.path.exists(FIGMA_BASELINE_PATH):
        import pytest
        pytest.skip("BASE_URL or baseline missing, skipping visual test")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(BASE_URL)
        buf = page.screenshot(full_page=False)
        current = Image.open(io.BytesIO(buf)).convert("RGBA").resize((1280, 800))
        baseline = Image.open(FIGMA_BASELINE_PATH).convert("RGBA").resize((1280, 800))
        assert images_similar(current, baseline, VISUAL_TOLERANCE)
        browser.close()
