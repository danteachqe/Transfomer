Below is your code after adapting it to Python with Playwright:

```python
from playwright.sync_api import sync_playwright
from zerostep.playwright import ai

def test_blaze_demo_booking():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto('http://blazedemo.com')
        page.wait_for_timeout(5000)

        ai('Select "Boston" from the departure city dropdown', page)
        page.wait_for_timeout(5000)

        ai('Select "New York" from the destination city dropdown', page)
        page.wait_for_timeout(5000)

        ai('Click the Find Flights button', page)
        page.wait_for_timeout(5000)

        ai('Select the first flight from the results table', page)
        page.wait_for_timeout(5000)

        ai('Enter passenger details with realistic values, for state just say NY', page)
        page.wait_for_timeout(5000)

        ai('Click the Purchase button', page)
        page.wait_for_timeout(5000)

        confirmation_message = page.get_by_text('Thank you for your purchase today!').content()
        assert confirmation_message is not None

        browser.close()
```

This code does not include an exact replica of `expect(confirmationMessage).toBeDefined();` from your original JavaScript code. The closest to it in Python is arguably the `assert` statement used to verify that `confirmation_message` is not None. If the content extracted with `get_by_text` is None, the `assert` will raise an `AssertionError`, failing the test.

Note that I've added `from zerostep.playwright import ai` to replace `import { ai } from '@zerostep/playwright';`. Replace `zerostep.playwright` with the equivalent package name in Python if it differs. Furthermore, in Python, Playwright has to be used in a context manager, that's why it is necessary to use the `with` keyword.