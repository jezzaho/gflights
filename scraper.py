import asyncio

from playwright.async_api import Playwright, expect, async_playwright
from selectolax.lexbor import LexborHTMLParser
from datetime import  datetime
from utils import *
PAGE_URI = "https://www.google.com/travel/flights?hl=en-US&curr=USD"
COOKIE_REFUSE_SEL = ".VfPpkd-dgl2Hf-ppHlrf-sM5MNb button"
TRIP_SEL_XPATH = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div["
                  "1]/div/div/div/div[1]")
ONE_WAY_XPATH = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div["
                 "1]/div/div/div/div[2]/ul/li[2]")
FROM_XPATH = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div["
              "1]/div/div/div[1]/div/div/input")
TO_XPATH = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div["
            "6]/div[2]/div[2]/div[1]/div/input")
DATE_XPATH = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div["
              "2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input")
SEARCH_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button"
DATE_DONE_BUTTON = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div["
                    "2]/div/div/div[2]/div/div[3]/div[3]/div/button")
FROM_FIRST_XPATH = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div["
                    "1]/div[6]/div[3]/ul/li[1]/div[2]")
T0_FIRST_XPATH = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div["
                  "1]/div[6]/div[2]/div[1]")
CHANGES_XPATH = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div/div[2]/div["
                 "1]/div/div[1]/span/button")
DIRECT_CHANGES_XPATH = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div[2]/div["
                        "3]/div/div[1]/section/div[2]/div[1]/div/div/div[2]/div")
SORT_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[1]/div/button"
SORT_BUTTON_X2 = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/div/div/div/div[1]/div/button"
SORT_BY_TIME_BUTTON = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/div/div/div/div["
                       "2]/div/ul/li[3]")
SUGGESTION_BUTTON = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div[2]/div/div/div["
                     "1]/span/span/span[2]/div/div/div/div[3]")
TO_FIRST_XPATH = ("/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div["
                  "1]/div[6]/div[3]/ul/li[1]/div[2]")

async def web_page_scraper(playwright: Playwright, from_airport, to_airport, dd):
    successful = False
    parser = None
    for _ in range(3):
        # Initial Setup
        print("Starting a scraper...")
        chromium = playwright.chromium
        browser = await chromium.launch()
        date = dd.strftime("%m-%d-%Y")


        # context = await browser.new_context(
        #     record_video_dir="videos/",
        #     record_video_size={"width": 640, "height": 480}
        # )

        page = await browser.new_page()
        page.set_default_timeout(20000)
        await page.goto(PAGE_URI)

        # Refuse cookies
        refuse_cookie = await page.wait_for_selector(COOKIE_REFUSE_SEL)
        await refuse_cookie.click()

        # BASIC INPUT AND ENTER A NEW PAGE
        # Click "trip type selector"
        await page.locator("xpath=" + TRIP_SEL_XPATH).click()
        # Click "one-way"
        await page.locator("xpath=" + ONE_WAY_XPATH).click()
        await page.wait_for_timeout(500)

        # Click and type "From", "To" and "Date"
        # "From"
        from_field = await page.wait_for_selector("/" + FROM_XPATH)
        await from_field.fill(from_airport)
        await page.locator("xpath=" + FROM_FIRST_XPATH).click()
        to_field = await page.wait_for_selector('[placeholder="Where to?"]')
        await to_field.fill(to_airport)
        await page.locator("xpath="+TO_FIRST_XPATH).click()
        date_field = await page.wait_for_selector('[placeholder="Departure"]')
        await date_field.focus()
        await page.wait_for_selector('[placeholder="Departure"]')
        await page.wait_for_timeout(300)
        await page.keyboard.type(date, delay=70)
        await page.keyboard.down("Enter")
        await page.wait_for_timeout(50)
        await page.keyboard.up("Enter")
        aria = aria_button_search(date)
        aria_text = '[aria-label="' + aria + '"]'
        await page.wait_for_timeout(300)
        try:
            date_field_ok = await page.wait_for_selector(aria_text, timeout=1000)
            await date_field_ok.click()
        except Exception as e:
            pass

        # await page.reload()
        await page.wait_for_load_state()
        search_button = await page.wait_for_selector('.xFFcie')
        await page.wait_for_timeout(150)
        await search_button.click()


        await page.locator("xpath=" + CHANGES_XPATH).click()
        await page.wait_for_timeout(150)
        await page.locator("xpath=" + DIRECT_CHANGES_XPATH).click()
        await page.wait_for_timeout(150)

        try:
            if await page.wait_for_selector("xpath=" + SUGGESTION_BUTTON, timeout=1000):
                await page.locator("xpath=" + SUGGESTION_BUTTON).click()
                # print("Suggestion dissmissed...")
        except Exception as e:
            pass

        # CO TO BYLO?
        try:
            await page.wait_for_selector('.vDyvKd', timeout=1000)
            await page.locator('.vDyvKd').click()
        except Exception as e:
            print("Shit aint working ")


        sorts = await page.query_selector(".VfPpkd-StrnGf-rymPhb-b9t22c")
        if sorts is not None:
            await sorts.click()
        #         print("Clicked sort button...")

        # print("Direct flights sorted by time departure...")

        await page.wait_for_timeout(100)

        more_detail_list = await page.query_selector_all(".trZjtf button")
        for i in range(len(more_detail_list)):
            await more_detail_list[i].click()
            await page.wait_for_timeout(25)
        #         print(f"Expanded button {i}")

        page_content = await page.content()
        parser = LexborHTMLParser(page_content)
        await page.close()
        await browser.close()
        print("Finished scraping...")
        successful = True

        if successful:
            break
    return parser


async def main():
    async with async_playwright() as playwright:
        await web_page_scraper(playwright,"KRK", "FRA", "4-05-2024")

if __name__ == '__main__':
    asyncio.run(main())
