from playwright.async_api import async_playwright, expect

async def test_booking_flight_from_boston_to_new_york():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Step 1: Navigate to the homepage
        await page.goto('http://blazedemo.com/')

        # Step 2: Locate the "Departure City" dropdown menu and select "Boston"
        await page.select_option('select[name="fromPort"]', 'Boston')

        # Step 3: Locate the "Destination City" dropdown menu and select "New York"
        await page.select_option('select[name="toPort"]', 'New York')

        # Step 4: Click on the "Find Flights" button
        await page.click('input[type="submit"]')

        # Step 5: Verify that the user is redirected to the flights listing page
        # URLs in Python require exact matching
        expect(page).to_have_url('*/reserve')

        # Step 6: Verify the list of available flights is displayed
        flight_list = page.locator('table tbody tr')

        # Option 1: Using manual count verification
        flight_count = await flight_list.count()
        expect(flight_count, "Flight count expected to be greater than 0").tobe_greater_than(0)

        # Proceed with the first flight selection
        await flight_list.nth(0).locator('input[type="submit"]').click()

        # Step 8: Verify that the user is on the purchase page
        expect(page).to_have_url('*/purchase')

        # Step 9: Fill in the purchase form with dummy passenger details
        await page.fill('input[name="inputName"]', 'John Doe')
        await page.fill('input[name="address"]', '123 Elm Street')
        await page.fill('input[name="city"]', 'Boston')
        await page.fill('input[name="state"]', 'MA')
        await page.fill('input[name="zipCode"]', '02115')
        await page.fill('input[name="creditCardNumber"]', '4111111111111111')
        await page.fill('input[name="nameOnCard"]', 'John Doe')

        # Step 10: Click on the "Purchase Flight" button
        await page.click('input[type="submit"]')

        # Step 11: Verify that the user is on the confirmation page
        expect(page).to_have_url('*/confirmation')

        # Step 12: Verify the confirmation details are displayed
        expect(page.locator('h1')).to_have_text('Thank you for your purchase today!')

        confirmation_id = await page.locator('tr:nth-child(1) td:nth-child(2)').text_content()
        expect(confirmation_id).not_to_be_none()

        print('Purchase confirmation ID:', confirmation_id)

        await browser.close()
