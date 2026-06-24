#!/usr/bin/env python3
import os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8080"
OUT = "screenshots"

os.makedirs(OUT, exist_ok=True)


def force_counters(page):
    page.evaluate("""
      document.querySelectorAll('.counter').forEach(el => {
        const t = parseInt(el.dataset.target);
        if (t >= 1000000) el.textContent = '1M';
        else if (t >= 100000) el.textContent = '100K';
        else if (t >= 10000) el.textContent = '10K';
        else if (t >= 1000) el.textContent = '1K';
        else if (t >= 100) el.textContent = '100';
        else el.textContent = String(t);
      });
    """)


def capture(page, name, viewport):
    page.set_viewport_size(viewport)
    page.goto(f"{BASE}/{name}.html", wait_until="networkidle")
    # Force reveal animations to final state
    page.add_style_tag(content=".reveal { opacity: 1 !important; transform: none !important; transition: none !important; }")
    # Wait for Mermaid diagrams
    page.wait_for_timeout(2000)
    # Scroll to counters to trigger animation
    page.evaluate("document.getElementById('impact')?.scrollIntoView({behavior:'instant'})" if name == "index" else "void(0)")
    page.wait_for_timeout(2500)
    # Ensure counters are at final values
    force_counters(page)
    # Scroll to bottom and back to top for full layout
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    prefix = "index" if name == "index" else "developers"
    width = viewport["width"]
    suffix = "desktop" if width >= 1000 else "mobile"
    path = os.path.join(OUT, f"{prefix}-{suffix}.png")
    page.screenshot(path=path, full_page=True)
    print(f"Saved {path}")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    capture(page, "index", {"width": 1440, "height": 900})
    capture(page, "index", {"width": 390, "height": 844})
    capture(page, "developers", {"width": 1440, "height": 900})
    capture(page, "developers", {"width": 390, "height": 844})

    browser.close()
