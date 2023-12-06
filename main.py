
import asyncio
from playwright.async_api import async_playwright, Playwright

PAGE_URI = "https://www.google.com/travel/flights?hl=en-US&curr=USD"
COOKIE_REFUSE_SEL = ".VfPpkd-dgl2Hf-ppHlrf-sM5MNb button"
TRIP_SEL_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div[1]"
ONE_WAY_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div[2]/ul/li[2]"
FROM_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input"
TO_XPATH =   "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input"
DATE_XPATH ="/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input"
SEARCH_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button"
DATE_DONE_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/div[3]/div/button"
FROM = "LHR"
TO = "FRA"
DATE = "12-15-2023"     # mm-dd-yyyy
async def web_page_scraper(playwright: Playwright):
    # Initial Setup
    print("Starting a webscraper...")
    chromium = playwright.chromium
    browser = await chromium.launch()
    page = await browser.new_page()
    await page.goto(PAGE_URI)

    await page.screenshot(path="./screens/1.png", full_page=True)

    # Refuse cookies
    refuse_cookie = await page.wait_for_selector(COOKIE_REFUSE_SEL)
    await refuse_cookie.click()

    await page.screenshot(path="./screens/2.png", full_page=True)
    # BASIC INPUT AND ENTER A NEW PAGE
    # Click "trip type selector"
    await page.locator("xpath="+TRIP_SEL_XPATH).click()
    # Click "one-way"
    await page.locator("xpath="+ONE_WAY_XPATH).click()
    await page.wait_for_timeout(500)
    await page.screenshot(path="./screens/3.png", full_page=True)

    # Click and type "From", "To" and "Date"
    # "From"
    from_field = await page.wait_for_selector("/" + FROM_XPATH)
    await page.wait_for_timeout(100)
    await from_field.click()
    await page.wait_for_timeout(100)
    await from_field.type("a" + FROM, delay=50)
    await page.wait_for_timeout(100)
    await page.keyboard.down("Enter")
    await page.keyboard.up("Enter")

    # "To"
    inputs = await page.query_selector_all(".e5F5td")
    to_field = inputs[1]
    if to_field:

    # test
    # if to_field:
    #     await page.wait_for_timeout(100)
    #     await from_field.click()
    #     await page.wait_for_timeout(100)
    #     await from_field.type("a" + TO, delay=50)
    #     await page.wait_for_timeout(100)
    #     await page.keyboard.down("Enter")
    #     await page.keyboard.up("Enter")

    # await page.locator("xpath="+DATE_DONE_BUTTON).click()

    # await page.wait_for_load_state()
    await page.wait_for_timeout(100)
    await page.screenshot(path="./screens/4.png", full_page=True)


    await page.close()

async def main():
    async with async_playwright() as playwright:
         await web_page_scraper(playwright)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())



