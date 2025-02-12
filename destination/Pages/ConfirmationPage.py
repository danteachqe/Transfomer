from playwright.sync_api import Page, expect  # Import expect from Playwright

class ConfirmationPage:
  def __init__(self, page: Page):
    self.page = page

  def verify_confirmation_page(self):
    print('Verifying confirmation page loaded...')
    expect(self.page).to_have_url(url_pattern= "/.*confirmation/", timeout= 10000)
  #  self.page.screenshot(path= 'step14_confirmation_page.png')

  def verify_confirmation_details(self):
    print('Verifying confirmation details...')
    confirmation_table = self.page.locator('table.table tbody')
    expect(confirmation_table).is_visible()
  #  self.page.screenshot(path= 'step15_confirmation_table.png')

    print('Verifying confirmation ID is visible...')
    confirmation_id = confirmation_table.locator('tr').first().locator('td:nth-child(2)')
    expect(confirmation_id).is_visible()
  #  self.page.screenshot(path= 'step16_confirmation_id.png')

    print('Verifying payment details...')
    payment_details = confirmation_table.locator('tr').nth(3)
    expect(payment_details.locator('td:nth-child(2)')).to_have_text('xxxxxxxxxxxx1111')  # Masked credit card
    self.page.screenshot(path= 'step17_payment_details.png')