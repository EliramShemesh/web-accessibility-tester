from playwright.sync_api import sync_playwright
from loguru import logger
import re

def parse_rgb(color):
    """Extracts RGB values from a CSS rgb/rgba string"""
    match = re.match(r"rgba?\((\d+), (\d+), (\d+).*\)", color)
    return tuple(map(int, match.groups())) if match else (0, 0, 0)

def relative_luminance(rgb):
    """Calculates relative luminance according to WCAG formula"""
    def adjust(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = map(adjust, rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(bg_rgb, text_rgb):
    """Computes the contrast ratio between two colors"""
    lum1 = relative_luminance(bg_rgb)
    lum2 = relative_luminance(text_rgb)
    L1, L2 = max(lum1, lum2), min(lum1, lum2)
    return (L1 + 0.05) / (L2 + 0.05)

class AccessibilityTester:
    def __init__(self, url):
        self.url = url
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        logger.info(f"Initialized AccessibilityTester for {self.url}")

    def open_page(self):
        try:
            self.page.goto(self.url)
            logger.info(f"Successfully opened {self.url}")
        except Exception as e:
            logger.error(f"Failed to open {self.url}: {e}")

    def check_missing_aria_labels(self):
        missing_labels = self.page.query_selector_all("*:not([aria-label]):not([aria-labelledby])")
        issues = [elem.evaluate("node => node.outerHTML") for elem in missing_labels]
        if issues:
            logger.warning(f"Found {len(issues)} elements missing ARIA labels.")
        else:
            logger.info("No missing ARIA labels found.")
        return issues
    
    def check_contrast_issues(self):
        contrast_issues = []
        elements = self.page.query_selector_all("*")
        for elem in elements:
            bg_color = elem.evaluate("node => getComputedStyle(node).backgroundColor")
            text_color = elem.evaluate("node => getComputedStyle(node).color")
            if bg_color and text_color:
                bg_rgb = parse_rgb(bg_color)
                text_rgb = parse_rgb(text_color)
                ratio = contrast_ratio(bg_rgb, text_rgb)
                if ratio < 4.5:
                    contrast_issues.append(elem.evaluate("node => node.outerHTML"))
        
        if contrast_issues:
            logger.warning(f"Found {len(contrast_issues)} elements with low contrast (ratio < 4.5).")
        else:
            logger.info("No contrast issues found.")
        return contrast_issues
    
    def generate_report(self):
        logger.info("Generating accessibility report...")
        report = {
            "missing_aria_labels": self.check_missing_aria_labels(),
            "contrast_issues": self.check_contrast_issues()
        }
        logger.info("Report generated successfully.")
        return report
    
    def close(self):
        self.browser.close()
        self.playwright.stop()
        logger.info("Closed AccessibilityTester session.")

if __name__ == "__main__":
    tester = AccessibilityTester("https://elirams.wixsite.com/eliram-shemesh")
    tester.open_page()
    report = tester.generate_report()
    print(report)
    tester.close()
