# home_page.py
from playwright.sync_api import Page, Locator, Error


class HomePage:
    def __init__(self, page: Page):
        self.page = page

        # Define selectors with both XPath and CSS
        self.selectors = {
            "departureDropdown": {
                "xpath": '//select[@name="fromPort"]',
                "css": 'select[name="fromPort"]'
            },
            "destinationDropdown": {
                "xpath": '//select[@name="toPort"]',
                "css": 'select[name="toPort"]'
            },
            "findFlightsButton": {
                "xpath": '//input[@type="submit" and @value="Find Flights"]',
                "css": 'input[type="submit"][value="Find Flights"]'
            },
            "pageHeader": {
                "xpath": '//h1',
                "css": 'h1'
            },
            # Add more elements as needed
        }

    def get_locator(self, selectors: dict) -> Locator:
        # Attempt using XPath first
        locator = self.page.locator(f'{selectors["xpath"]}')
        if len(locator) > 0:
            return locator

        # If not found, attempt using CSS selector
        locator = self.page.locator(f'{selectors["css"]}')
        if len(locator) > 0:
            return locator

        # If still not found, throw an error
        raise Error(f'Element not found using XPath: {selectors["xpath"]} or CSS: {selectors["css"]}')

    def goto(self):
        self.page.goto('/') 

    def verify_home_page_loaded(self):
        assert self.page.url() in self.page.url()
        header_locator = self.get_locator(self.selectors["pageHeader"])
        assert header_locator.text_content() == 'Welcome to the Simple Travel Agency!'

    def select_departure_city(self, city: str):
        departure_locator = self.get_locator(self.selectors["departureDropdown"])
        departure_locator.select_option(label=city)

    def select_destination_city(self, city: str):
        destination_locator = self.get_locator(self.selectors["destinationDropdown"])
        destination_locator.select_option(label=city)

    def find_flights(self):
        find_flights_locator = self.get_locator(self.selectors["findFlightsButton"])
        find_flights_locator.click()