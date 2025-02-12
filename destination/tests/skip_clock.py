from playwright.async_api import async_playwright

from Pages.HomePage import HomePage
from Pages.FlightsPage import FlightsPage
from Pages.PurchasePage import PurchasePage
from Pages.ConfirmationPage import ConfirmationPage

import json

# Import test data
with open('../data/flightData1.json') as file:
    flight_data = json.load(file)
departure_city = flight_data['departureCity']
destination_city = flight_data['destinationCity']

with open('../data/passengerInfo1.json') as file:
    passenger_info = json.load(file)

with open('../data/paymentInfo1.json') as file:
    payment_info = json.load(file)

async with async_playwright() as playwright:
    browser = await playwright.chromium.launch()
    page = await browser.new_page()
    
    home_page = HomePage(page)
    flights_page = FlightsPage(page)
    purchase_page = PurchasePage(page)
    confirmation_page = ConfirmationPage(page)

    await home_page.goto()
    await home_page.verify_home_page_loaded()
    await home_page.select_departure_city(departure_city)
    await home_page.select_destination_city(destination_city)
    await home_page.find_flights()

    await flights_page.verify_flights_page(departure_city, destination_city)
    await flights_page.verify_flights_displayed()
    await flights_page.select_first_flight()

    await purchase_page.verify_purchase_page_loaded()
    await purchase_page.fill_passenger_info(passenger_info)
    await purchase_page.fill_payment_info(payment_info)

    time_before_fast_forward = await page.evaluate('() => Date.now()')
    print(f"Time before fast-forward: {time_before_fast_forward}")

    await page.evaluate('() => Date.now() + 3 * 60 * 1000')
    print("Fast-forwarding time by 3 minutes...")

    time_after_fast_forward = await page.evaluate('() => Date.now()')
    print(f"Time after fast-forward: {time_after_fast_forward}")

    fast_forwarded_time = time_after_fast_forward - time_before_fast_forward
    print(f"Fast-forwarded time difference: {fast_forwarded_time / 1000} seconds")

    await purchase_page.purchase_flight()

    await confirmation_page.verify_confirmation_page()
    await confirmation_page.verify_confirmation_details()

    await browser.close()