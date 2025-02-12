import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser_type_pw(pytestconfig):
    return pytestconfig.getoption("--browser")

@pytest.fixture(scope="session")
def browser_context_args_pw(pytestconfig):
    return {
        "headless": pytestconfig.getoption("--headless"),
        "ignoreHTTPSErrors": True,
        "viewport": {"width": 1280, "height": 720},
        "video": "retain-on-failure",
        "screenshot": "only-on-failure",
        "trace": "on-first-retry",
    }

@pytest.fixture(scope="session")
def browser_context(browser_type_pw, browser_context_args_pw, worker_info):
    if worker_info is None:  # single-threaded
        browser_context_args_pw["storageState"] = "state.json"
    else:  # multi-threaded
        browser_context_args_pw["storageState"] = f"state-{worker_info.worker_id}.json"
    with sync_playwright() as p:
        browser = p.__dict__[browser_type_pw].launch()
        context = browser.new_context(**browser_context_args_pw)
        yield context
        context.close()
        browser.close()

@pytest.fixture
def page(browser_context):
    page = browser_context.new_page()
    page.goto('https://blazedemo.com')
    yield page
    page.close()

def pytest_addoption(parser):
    parser.addoption('--browser', default='chromium')

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "browser(name): mark test to run only on named browser"
    )

def pytest_collection_modifyitems(config, items):
    keywordexpr = config.option.keyword
    markexpr = config.option.markexpr
    if keywordexpr or markexpr:
        return  # let pytest handle this

    # if neither keyword nor mark are selected, skip tests that don't match the browser
    browser = config.getoption("--browser")
    skip_browser = pytest.mark.skip(reason="not running on this browser")

    for item in items:
        if "browser" in item.keywords:
            browsers = [mark.args[0] for mark in item.iter_markers(name="browser")]
            if browser not in browsers:
                item.add_marker(skip_browser)
