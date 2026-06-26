#!/usr/bin/env python3
import os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8080"
OUT = "screenshots"

os.makedirs(OUT, exist_ok=True)


def force_counters(page):
    # Generic counter finalizer: supports .stat-value[data-target] and .counter[data-target]
    page.evaluate("""
      document.querySelectorAll('.stat-value[data-target], .counter[data-target]').forEach(el => {
        const t = parseInt(el.dataset.target);
        let text;
        if (t >= 1000000) text = '1M';
        else if (t >= 100000) text = '100K';
        else if (t >= 10000) text = '10K';
        else if (t >= 1000) text = '1K';
        else if (t >= 100) text = '100';
        else text = String(t);
        el.textContent = text;
      });
    """)


def capture(page, name, viewport):
    page.set_viewport_size(viewport)
    page.goto(f"{BASE}/{name}.html", wait_until="networkidle")
    # Force reveal animations to final state
    page.add_style_tag(content=".reveal { opacity: 1 !important; transform: none !important; transition: none !important; }")
    # Wait for fonts, Mermaid, etc.
    page.wait_for_timeout(2000)
    # Scroll to counters to trigger animation on index/impact pages
    page.evaluate("document.getElementById('vision')?.scrollIntoView({behavior:'instant'})" if name == "index" else "void(0)")
    page.wait_for_timeout(2500)
    # Ensure counters are at final values
    force_counters(page)
    # Scroll to bottom and back to top for full layout
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    width = viewport["width"]
    suffix = "desktop" if width >= 1000 else "mobile"
    path = os.path.join(OUT, f"{name}-{suffix}.png")
    page.screenshot(path=path, full_page=True)
    print(f"Saved {path}")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for name in ["index", "heroes", "developers"]:
        capture(page, name, {"width": 1440, "height": 900})
        capture(page, name, {"width": 390, "height": 844})

    browser.close()
