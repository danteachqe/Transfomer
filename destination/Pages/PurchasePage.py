from playwright.sync_api import Page, expect

class PurchasePage:
    def __init__(self, page: Page):
        self.page = page

    def verify_purchase_page_loaded(self):
        print('Verifying reservation page loaded...')
        expect(self.page).to_have_url('https://blazedemo.com/purchase.php')
        # self.page.screenshot(path='step9_reservation_page.png')

    def fill_passenger_info(self, passenger_info):
        print('Filling in passenger information...')
        self.page.fill('input[name="inputName"]', passenger_info['name'])
        self.page.fill('input[name="address"]', passenger_info['address'])
        self.page.fill('input[name="city"]', passenger_info['city'])
        self.page.fill('input[name="state"]', passenger_info['state'])
        self.page.fill('input[name="zipCode"]', passenger_info['zipCode'])
        self.page.screenshot(path='step11_passenger_info_filled.png')

    def fill_payment_info(self, payment_info):
        print('Filling in payment information...')
        self.page.fill('input[name="creditCardNumber"]', payment_info['creditCardNumber'])
        self.page.fill('input[name="creditCardMonth"]', payment_info['creditCardMonth'])
        self.page.fill('input[name="creditCardYear"]', payment_info['creditCardYear'])
        self.page.fill('input[name="nameOnCard"]', payment_info['nameOnCard'])
        # self.page.screenshot(path='step12_payment_info_filled.png')

    def purchase_flight(self):
        print('Clicking "Purchase Flight" button...')
        self.page.click('input[type="submit"]')
        # self.page.screenshot(path='step13_purchase_flight_clicked.png')