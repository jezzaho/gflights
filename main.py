
import asyncio
from playwright.async_api import async_playwright, Playwright
from selectolax.lexbor import LexborHTMLParser

PAGE_URI = "https://www.google.com/travel/flights?hl=en-US&curr=USD"
COOKIE_REFUSE_SEL = ".VfPpkd-dgl2Hf-ppHlrf-sM5MNb button"
TRIP_SEL_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div[1]"
ONE_WAY_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div[2]/ul/li[2]"
FROM_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input"
TO_XPATH =   "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input"
DATE_XPATH ="/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input"
SEARCH_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button"
DATE_DONE_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/div[3]/div/button"
FROM_FIRST_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]/div[2]"
T0_FIRST_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[1]"
CHANGES_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div/div[2]/div[1]/div/div[1]/span/button"
DIRECT_CHANGES_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div[2]/div[3]/div/div[1]/section/div[2]/div[1]/div/div/div[2]/div"
SORT_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[1]/div/button"
SORT_BY_TIME_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[2]/div/ul/li[3]"
SUGGESTION_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/span/span/span[2]/div/div/div/div[3]"
FROM = "KRK"
TO = "WAW"
DATE = "12-15-2023"     # mm-dd-yyyy
async def web_page_scraper(playwright: Playwright):
    # Initial Setup
    print("Starting a webscraper...")
    chromium = playwright.chromium
    browser = await chromium.launch()


    context = await browser.new_context(
        record_video_dir="videos/",
        record_video_size={"width": 640, "height": 480}
    )
    page = await context.new_page()
    await page.goto(PAGE_URI)



    # Refuse cookies
    refuse_cookie = await page.wait_for_selector(COOKIE_REFUSE_SEL)
    await refuse_cookie.click()


    # BASIC INPUT AND ENTER A NEW PAGE
    # Click "trip type selector"
    await page.locator("xpath="+TRIP_SEL_XPATH).click()
    # Click "one-way"
    await page.locator("xpath="+ONE_WAY_XPATH).click()
    await page.wait_for_timeout(500)


    # Click and type "From", "To" and "Date"
    # "From"
    from_field = await page.wait_for_selector("/" + FROM_XPATH)
    await page.wait_for_timeout(300)
    if from_field:
        await from_field.fill(FROM)
        await page.wait_for_timeout(200)
        await page.locator("xpath="+FROM_FIRST_XPATH).click()
        await page.wait_for_timeout(100)

        print("Clicked First field in from")
        await page.keyboard.down("Tab")
        await page.keyboard.up("Tab")
        await page.keyboard.type(TO, delay=50)
        await page.wait_for_timeout(100)
        await page.keyboard.down("Tab")
        await page.keyboard.up("Tab")
        await page.keyboard.press("Tab")
        await page.wait_for_timeout(150)
        await page.keyboard.type(DATE, delay=150)
        await page.wait_for_timeout(150)
        await page.keyboard.down("Tab")
        await page.keyboard.up("Tab")
        await page.wait_for_timeout(100)
        await page.keyboard.down("Enter")
        await page.keyboard.up("Enter")
        await page.wait_for_timeout(2000)
        print(f"Searching for flights from {FROM} to {TO} on {DATE}")

    await page.locator("xpath="+CHANGES_XPATH).click()
    await page.wait_for_timeout(150)
    await page.locator("xpath="+DIRECT_CHANGES_XPATH).click()
    await page.wait_for_timeout(150)

    try:
        if await page.wait_for_selector("xpath="+SUGGESTION_BUTTON, timeout=3000):
            await page.locator("xpath="+SUGGESTION_BUTTON).click()
            print("Suggestion dissmissed...")
    except Exception as e:
        print("Suggestion button not found...", e)


    await page.locator("xpath="+SORT_BUTTON).click()
    await page.wait_for_timeout(150)
    await page.locator("xpath=" + SORT_BY_TIME_BUTTON).click()

    print("Direct flights sorted by time departure...")

    await page.wait_for_timeout(5000)
    print("Done...")



    await page.close()
    await context.close()

    parser = LexborHTMLParser(page.content())
    return  parser

def getPageContent(parser):
    data = {}
    categories = parser.root.css('.zBTtmb')
    category_results = parser.root.css('.Rk10dc')

    #TODO Tailor it to my needs

    for category, category_result in zip(categories, category_results):
        category_data = []

        for result in category_result.css('.yR1fYc'):
            date = result.css('[jscontroller="cNtv4b"] span')
            departure_date = date[0].text()
            arrival_date = date[1].text()
            company = result.css_first('.Ir0Voe .sSHqwe').text()
            duration = result.css_first('.AdWm1c.gvkrdb').text()
            stops = result.css_first('.EfT7Ae .ogfYpf').text()
            emissions = result.css_first('.V1iAHe .AdWm1c').text()
            emission_comparison = result.css_first('.N6PNV').text()
            price = result.css_first('.U3gSDe .FpEdX span').text()
            price_type = result.css_first('.U3gSDe .N872Rd').text() if result.css_first('.U3gSDe .N872Rd') else None

            flight_data = {
                'departure_date': departure_date,
                'arrival_date': arrival_date,
                'company': company,
                'duration': duration,
                'stops': stops,
                'emissions': emissions,
                'emission_comparison': emission_comparison,
                'price': price,
                'price_type': price_type
            }

            airports = result.css_first('.Ak5kof .sSHqwe')
            service = result.css_first('.hRBhge')

            if service:
                flight_data['service'] = service.text()
            else:
                flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text()
                flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text()

            category_data.append(flight_data)

        data[category.text().lower().replace(' ', '_')] = category_data

    return data

async def main():
    async with async_playwright() as playwright:
         await web_page_scraper(playwright)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())



