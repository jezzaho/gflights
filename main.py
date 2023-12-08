
import asyncio
import json

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
SORT_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/div/div/div/div[1]/div/button"
SORT_BY_TIME_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/div/div/div/div[2]/div/ul/li[3]"
SUGGESTION_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/span/span/span[2]/div/div/div/div[3]"

async def web_page_scraper(playwright: Playwright, from_airport, to_airport, date):
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
        await from_field.fill(from_airport)
        await page.wait_for_timeout(200)
        await page.locator("xpath="+FROM_FIRST_XPATH).click()
        await page.wait_for_timeout(100)

        print("Clicked First field in from")
        await page.keyboard.down("Tab")
        await page.keyboard.up("Tab")
        await page.keyboard.type(to_airport, delay=50)
        print("Typed to field")
        await page.wait_for_timeout(200)
        await page.keyboard.down("Tab")
        await page.wait_for_timeout(100)
        await page.keyboard.up("Tab")
        await page.wait_for_timeout(50)
        await page.keyboard.down("Tab")
        await page.wait_for_timeout(100)
        await page.keyboard.up("Tab")
        await page.wait_for_timeout(100)
        await page.keyboard.type(date, delay=200)
        print("Typed date field")
        await page.wait_for_timeout(150)
        await page.keyboard.down("Tab")
        await page.keyboard.up("Tab")
        await page.wait_for_timeout(100)
        await page.keyboard.down("Enter")
        await page.keyboard.up("Enter")
        await page.wait_for_timeout(2000)
        print(f"Searching for flights from {from_airport} to {to_airport} on {date}")

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
    print("Found sort button...")
    await page.wait_for_timeout(150)
    await page.locator("xpath=" + SORT_BY_TIME_BUTTON).click()
    print("Clicked sort button...")

    print("Direct flights sorted by time departure...")

    await page.wait_for_timeout(4000)







    moreDetailList = await page.query_selector_all(".trZjtf button")
    for i in range(len(moreDetailList)):
        await moreDetailList[i].click()
        await page.wait_for_timeout(100)
        print(f"Expanded button {i}")



    page_content = await page.content()
    parser = LexborHTMLParser(page_content)
    await page.close()
    await context.close()
    return parser

def getPageContent(parser):
    all_data = []
    # categories = parser.root.css('.zBTtmb')
    # category_results = parser.root.css('.Rk10dc')
    parent_category = parser.root.css('.pIav2d')
    # time departure
    # time arrival
    # Airline
    # Airplane
    # Flight number
    for result in parent_category:

        date_info = result.css('[jscontroller="cNtv4b"] span')
        time_departure = date_info[0].text()
        time_arrival = date_info[1].text()
        company = result.css_first('.MX5RWe span:nth-child(2)').text()
        airplane = result.css_first('.MX5RWe span:nth-child(8)').text()
        # TODO napraw operatora
        operator = result.css_first('kSwLQc sSHqwe y52p7d')
        flightNumber = result.css_first('.MX5RWe span:nth-child(4)').text()


        flightData = {
            'time_departure': time_departure,
            'time_arrival': time_arrival,
            'company': company,
            'airplane': airplane,
            'flight_number': flightNumber,
            'Operator': company if operator is None else operator.text()
        }
        all_data.append(flightData)
    return all_data

    #TODO Tailor it to my needs
    #
    # for category, category_result in zip(categories, category_results):
    #     category_data = []
    #
    #     for result in category_result.css('.yR1fYc'):
    #         date = result.css('[jscontroller="cNtv4b"] span')
    #         departure_date = date[0].text()
    #         arrival_date = date[1].text()
    #         company = result.css_first('.Ir0Voe .sSHqwe').text()
    #         duration = result.css_first('.AdWm1c.gvkrdb').text()
    #         stops = result.css_first('.EfT7Ae .ogfYpf').text()
    #         emissions = result.css_first('.V1iAHe .AdWm1c').text()
    #         emission_comparison = result.css_first('.N6PNV').text()
    #         price = result.css_first('.U3gSDe .FpEdX span').text()
    #         price_type = result.css_first('.U3gSDe .N872Rd').text() if result.css_first('.U3gSDe .N872Rd') else None
    #
    #         flight_data = {
    #             'departure_date': departure_date,
    #             'arrival_date': arrival_date,
    #             'company': company,
    #             'duration': duration,
    #             'stops': stops,
    #             'emissions': emissions,
    #             'emission_comparison': emission_comparison,
    #             'price': price,
    #             'price_type': price_type
    #         }
    #
    #         airports = result.css_first('.Ak5kof .sSHqwe')
    #         service = result.css_first('.hRBhge')
    #
    #         if service:
    #             flight_data['service'] = service.text()
    #         else:
    #             flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text()
    #             flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text()
    #
    #         category_data.append(flight_data)
    #
    #     data[category.text().lower().replace(' ', '_')] = category_data
    #
    # return data
async def run(playwright):
    FROM = "MUC"
    TO = "KRK"
    DATE = "5-21-2024"  # mm-dd-yyyy

    parser = await web_page_scraper(playwright, FROM, TO, DATE)
    total_result = getPageContent(parser)
    for obj in total_result:
        obj["From"] = FROM
        obj["To"] = TO
        obj["Date"] = DATE

    modify_results(total_result)

async def main():
    async with async_playwright() as playwright:
         await run(playwright)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())

def modify_results(list):
    for obj in list:
        obj["Days"] = get_day_of_week(obj["Date"])
def get_day_of_week(date_string):
    year, month, day = map(int, date_string.split('-'))
    day_of_week = (int(f"{year}{month:02d}{day:02d}") - 1) % 7

    return '.'.join(str(i) if i != day_of_week else str(day_of_week) for i in range(7))
