import asyncio
import json
from datetime import datetime
import datetime as dt
import sys
import pandas as pd


from playwright.async_api import async_playwright, Playwright
from selectolax.lexbor import LexborHTMLParser

PAGE_URI = "https://www.google.com/travel/flights?hl=en-US&curr=USD"
COOKIE_REFUSE_SEL = ".VfPpkd-dgl2Hf-ppHlrf-sM5MNb button"
TRIP_SEL_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div[1]"
ONE_WAY_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div[2]/ul/li[2]"
FROM_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input"
TO_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input"
DATE_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input"
SEARCH_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button"
DATE_DONE_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/div[3]/div/button"
FROM_FIRST_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]/div[2]"
T0_FIRST_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[1]"
CHANGES_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div/div[2]/div[1]/div/div[1]/span/button"
DIRECT_CHANGES_XPATH = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div[2]/div[3]/div/div[1]/section/div[2]/div[1]/div/div/div[2]/div"
SORT_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[1]/div/button"
SORT_BUTTON_X2 = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/div/div/div/div[1]/div/button"
SORT_BY_TIME_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/div/div/div/div[2]/div/ul/li[3]"
SUGGESTION_BUTTON = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/span/span/span[2]/div/div/div/div[3]"


### HELPER FUNCTIONS ####
def convert_time(time):
    t = time.replace('\\u202f', ' ')
    dt = datetime.strptime(t, "%I:%M %p")
    return dt.strftime("%H:%M")


def modify_results(list):
    for obj in list:
        obj["Days"] = get_day_of_week(obj["Date"])


def get_day_of_week(date_string):
    date = datetime.strptime(date_string, "%m-%d-%Y")
    day_of_week = date.weekday() + 1
    return (day_of_week - 1) * '.' + str(day_of_week) + (7 - day_of_week) * '.'


async def web_page_scraper(playwright: Playwright, from_airport, to_airport, dd):
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
    await page.wait_for_timeout(300)
    if from_field:
        await from_field.fill(from_airport)
        await page.wait_for_timeout(200)
        await page.locator("xpath=" + FROM_FIRST_XPATH).click()
        await page.wait_for_timeout(100)

        # print("Clicked First field in from")
        await page.keyboard.down("Tab")
        await page.keyboard.up("Tab")
        await page.keyboard.type(to_airport, delay=50)
        # print("Typed to field")
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
        # print("Typed date field")
        await page.wait_for_timeout(150)
        await page.keyboard.down("Tab")
        await page.keyboard.up("Tab")
        await page.wait_for_timeout(100)
        await page.keyboard.down("Enter")
        await page.keyboard.up("Enter")
        await page.wait_for_timeout(2000)
#         print(f"Searching for flights from {from_airport} to {to_airport} on {date}")

    await page.locator("xpath=" + CHANGES_XPATH).click()
    await page.wait_for_timeout(150)
    await page.locator("xpath=" + DIRECT_CHANGES_XPATH).click()
    await page.wait_for_timeout(150)

    try:
        if await page.wait_for_selector("xpath=" + SUGGESTION_BUTTON, timeout=3000):
            await page.locator("xpath=" + SUGGESTION_BUTTON).click()
            # print("Suggestion dissmissed...")
    except Exception as e:
        pass

    try:
        await page.wait_for_selector('.vDyvKd', timeout=3000)
        await page.locator('.vDyvKd').click()
    except Exception as e:
        # print("Shit aint working ")
        sys.exit(1)
    # try:
    #     await page.wait_for_selector('[aria-label="Best Flights, Change sort order"]', timeout=3000)
    #     await page.locator('[aria-label="Best Flights, Change sort order"]').click()
    # except Exception as e:
    #     print("FATAL! WONT WORK")
    #     sys.exit(1)

    # print("Found sort button...")
    await page.wait_for_timeout(150)
    sorts = await page.query_selector(".VfPpkd-StrnGf-rymPhb-b9t22c")
    if sorts is not None:
        await sorts.click()
#         print("Clicked sort button...")

    # print("Direct flights sorted by time departure...")

    await page.wait_for_timeout(4000)

    moreDetailList = await page.query_selector_all(".trZjtf button")
    for i in range(len(moreDetailList)):
        await moreDetailList[i].click()
        await page.wait_for_timeout(100)
#         print(f"Expanded button {i}")

    page_content = await page.content()
    parser = LexborHTMLParser(page_content)
    await page.close()
    await browser.close()
    print("Finished scraping...")
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
        operator = result.css_first('.kSwLQc')
        optext = "" if operator is None else operator.text()
        op = optext.split("by", 1)[1].strip() if "by" in optext else optext
        flightNumber = result.css_first('.MX5RWe span:nth-child(4)').text()

        flightData = {
            'Time_departure': time_departure,
            'Time_arrival': time_arrival,
            'company': company,
            'airplane': airplane,
            'Flight_number': flightNumber,
            'Operator': company if operator is None else op
        }
        all_data.append(flightData)
    return all_data


def iterate_dates(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += dt.timedelta(days=1)


# def getEverything(from_airport, to_airport_list, date_start, date_end):
#     # DATE_START = "3-31-2024"
#     # DATE_END = "10-27-2024"
#     bigDataObject = []
#     datetime_start = datetime.strptime(date_start, "%m-%d-%Y")
#     datetime_end = datetime.strptime(date_end, "%m-%d-%Y")
#
#     for date in iterate_dates(datetime_start, datetime_end):
#         ### what to put there


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


async def run(from_airport, to_airports, playwright):
    DATE_START = "3-31-2024"
    DATE_END = "4-27-2024" # "10-27-2024"
    bigDataObject = []
    datetime_start = datetime.strptime(DATE_START, "%m-%d-%Y")
    datetime_end = datetime.strptime(DATE_END, "%m-%d-%Y")

    semaphore = asyncio.Semaphore(10)
    async def scrape_and_parse(to_airport, date):
        nonlocal semaphore
        async with semaphore:
            print(f"Acquired semaphore: {semaphore}")
            try:
                parser = await web_page_scraper(playwright, from_airport, to_airport, date)
                total_result = getPageContent(parser)
                for obj in total_result:
                    obj["Time_departure"] = convert_time(obj["Time_departure"])
                    obj["Time_arrival"] = convert_time(obj["Time_arrival"])
                    obj["Flight_number"] = obj["Flight_number"].replace("\\u00a0", " ")
                    obj["From"] = from_airport
                    obj["To"] = to_airport
                    obj["Date"] = date.strftime("%m-%d-%Y")
                    obj["Days"] = get_day_of_week(obj["Date"])

                bigDataObject.append(total_result)
            except Exception as e:
                print(f"Error in scrape_and_parse: {e}")
    tasks = []
    for to_airport in to_airports:
        for date in iterate_dates(datetime_start, datetime_end):
            tasks.append(scrape_and_parse(to_airport, date))

    await asyncio.gather(*tasks)
    fobj = flatten_json(bigDataObject)
    df = pd.json_normalize(fobj)
    df.to_excel("baza.xlsx", index=False, engine="openpyxl")
    print("Data has been transfered to a file.")



async def main():
    async with async_playwright() as playwright:
        await run("KRK", ["FRA", "MUC"], playwright)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())
