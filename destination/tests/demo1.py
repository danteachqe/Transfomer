# test_flightReservation.py

from playwright.sync_api import sync_playwright
import pytest
import json

from Pages.HomePage import HomePage
from Pages.FlightsPage import FlightsPage
from Pages.PurchasePage import PurchasePage
from Pages.ConfirmationPage import ConfirmationPage

# Import test data
with open("../data/flightData1.json") as f:
    flightData = json.load(f)
with open("../data/passengerInfo1.json") as f:
    passengerInfo = json.load(f)
with open("../data/paymentInfo1.json") as f:
    paymentInfo = json.load(f)

def test_search_and_reserve_a_flight_on_blazedemo(page):
    departureCity = flightData["departureCity"]
    destinationCity = flightData["destinationCity"]

    homePage = HomePage(page)
    flightsPage = FlightsPage(page)
    purchasePage = PurchasePage(page)
    confirmationPage = ConfirmationPage(page)

    homePage.goto()
    homePage.verify_home_page_loaded()
    homePage.select_departure_city(departureCity)
    homePage.select_destination_city(destinationCity)
    homePage.find_flights()

    flightsPage.verify_flights_page(departureCity, destinationCity)
    flightsPage.verify_flights_displayed()
    flightsPage.select_first_flight()
    
    purchasePage.verify_purchase_page_loaded()
    purchasePage.fill_passenger_info(passengerInfo)
    purchasePage.fill_payment_info(paymentInfo)
    purchasePage.purchase_flight()

    confirmationPage.verify_confirmation_page()
    confirmationPage.verify_confirmation_details()


# Pytest configuration for playwright
@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="session", autouse=True)
def teardown(playwright: sync_playwright):
    yield
    playwright.stop()