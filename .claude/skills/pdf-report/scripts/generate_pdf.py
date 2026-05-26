#!/usr/bin/env python3
"""
Generate PDF from HTML using Playwright (Chromium headless).
Auto-installs dependencies on first run.
Usage: python3 generate_pdf.py <input.html> <output.pdf>
"""

import sys, os, subprocess, shutil

def ensure_playwright():
    """Install playwright + chromium if not present."""
    try:
        from playwright.sync_api import sync_playwright
        return
    except ImportError:
        print("[pdf-report] Installing playwright...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Check if chromium is installed
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
        return
    except Exception:
        print("[pdf-report] Installing Chromium (~150MB, one-time)...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def html_to_pdf(input_path, output_path):
    """Convert HTML file to PDF using headless Chromium."""
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    abs_input = os.path.abspath(input_path)
    abs_output = os.path.abspath(output_path)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 1600})
        page.goto(f"file://{abs_input}", wait_until="networkidle")
        # Wait for any rendered content
        page.wait_for_timeout(500)

        page.pdf(
            path=abs_output,
            format="A4",
            print_background=True,
            display_header_footer=False,
            prefer_css_page_size=True,  # respect @page CSS rules
        )
        browser.close()

    size_kb = os.path.getsize(abs_output) / 1024
    print(f"[pdf-report] PDF generated: {abs_output} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 generate_pdf.py <input.html> <output.pdf>")
        sys.exit(1)
    html_to_pdf(sys.argv[1], sys.argv[2])
