from playwright.sync_api import Page

class FlightsPage:
    def __init__(self, page: Page):
        self.page = page
        self.flightTable = self.page.locator('table.table')
        self.flights = self.flightTable.locator('tbody tr')

    def verifyFlightsPage(self, departureCity, destinationCity):
        print('Verifying flights listing page loaded...')
        assert self.page.url == 'https://blazedemo.com/reserve.php'
        assert self.page.locator('h3').inner_text() == f'Flights from {departureCity} to {destinationCity}:'
        # self.page.screenshot(path='step6_flights_listing_page.png')

    def verifyFlightsDisplayed(self):
        print('Verifying flight entries are displayed...')
        flightCount = len(self.flights)
        print(f'Number of flights found: {flightCount}')
        assert flightCount > 0  # Ensure at least one flight is listed
        # self.page.screenshot(path='step7_flights_displayed.png')

    def selectFirstFlight(self):
        print('Selecting the first available flight...')
        self.flights.nth(0).locator('input[type="submit"]').click()
        self.page.screenshot(path='step8_first_flight_selected.png')