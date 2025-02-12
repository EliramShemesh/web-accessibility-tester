# Web Accessibility Tester

## Overview
Accessibility Tester is an automated tool built using **Python**, **Playwright**, and **Loguru**. It helps identify web accessibility issues, including:
- Missing ARIA labels
- Low-contrast text elements (based on WCAG contrast ratio)

## Features
✅ **Automated ARIA Label Check**: Finds elements missing `aria-label` or `aria-labelledby` attributes.  
✅ **Contrast Ratio Analysis**: Calculates contrast ratio between text and background colors using WCAG guidelines.  
✅ **Logging with Loguru**: Provides detailed logging for debugging and reporting.  
✅ **Fully Automated Testing**: Uses Playwright to navigate and interact with web pages.

## Installation
Make sure you have Python installed (>=3.7), then install the dependencies:
```bash
pip install playwright loguru
playwright install
```

## Usage
Run the script by providing a website URL:
```bash
python accessibility_tester.py
```
This will:
1. Open the webpage
2. Check for missing ARIA labels
3. Check for low-contrast text elements
4. Generate an accessibility report

## Example Output
```json
{
  "missing_aria_labels": ["<button>Click me</button>"],
  "contrast_issues": ["<p style='color: #aaa; background: #fff'>Some text</p>"]
}
```

## Future Improvements
- Add support for checking keyboard accessibility
- Generate detailed HTML reports
- Support batch testing for multiple URLs

## License
This project is licensed under the MIT License.

