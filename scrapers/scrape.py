import asyncio
from time import sleep
from playwright.async_api import async_playwright

async def scrape_site():
    async with async_playwright() as p:
        # Launch the Firefox browser. Headless mode can be set to False to watch the script's actions
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()

        # Navigate to the initial page
        await page.goto('https://www.trees.menu/102nd/flower')

        # Find all sale items by their unique selectors or attributes indicating a sale
        on_sale_items = await page.query_selector_all('xpath=//div[contains(@class, "flowerboxleft12")][.//div[@id="onsale"][not(.="")]]')

        # Iterate over found items to click and scrape modal content
        for item in on_sale_items:
            # Clicking on the item to open the modal with details
            await item.click()
            # Ensure the modal is open and content is loaded; adjust the selector as necessary
            await page.wait_for_selector('div.modal.fade.in')

            # Scrape the necessary details from the modal
            thc_value = await page.inner_text('xpath=//div[@id="dataModal"]//div[@class="modal-dialog modal-lg"]//div[@class="modal-content"]//form[@id="productmodal"]//div[@id="product_detail"]//div[contains(@class, "col-md-6")][2]//div[contains(., "THC:")]')
            thc_percentage = thc_value.split('\n')[1]
            thc_percentage = thc_percentage.split(":")
            thc_percentage = float(thc_percentage[1].replace("%", "").strip())
            if thc_percentage >= 25:
                # Scrape other necessary details here
                product_name = await page.input_value('input#name')
                print(f"Product Name: {product_name}, THC: {thc_percentage}%")

            # Close the modal if necessary before moving to the next item
            await page.click('xpath=//div[@id="dataModal"]//div[@class="modal-dialog modal-lg"]//div[@class="modal-content"]//form[@id="productmodal"]//div[@id="product_detail"]//div[contains(@class, "col-md-6")][1]//img[@data-dismiss="modal"]')

            # Adding a slight delay to ensure the modal closes smoothly and to mimic human interaction
            await asyncio.sleep(1)

        # Close the browser
        await browser.close()

asyncio.run(scrape_site())

