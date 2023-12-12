import asyncio
from itertools import chain

import pandas as pd
from playwright.async_api import async_playwright

from scraper import web_page_scraper
from utils import *


async def run(from_airport, to_airports, playwright):
    date_start = "3-31-2024"
    date_end = "4-10-2024"  # "10-27-2024"
    big_data_object = []
    datetime_start = datetime.strptime(date_start, "%m-%d-%Y")
    datetime_end = datetime.strptime(date_end, "%m-%d-%Y")

    semaphore = asyncio.Semaphore(10)

    async def scrape_and_parse(from_airport_outer, airport_target, date_inscope):
        nonlocal semaphore
        async with semaphore:
            print(f"Acquired semaphore: {semaphore}")
            try:
                parser = await web_page_scraper(playwright, from_airport_outer, airport_target, date_inscope)
                total_result = get_page_content(parser)
                for obj in total_result:
                    obj["Time_departure"] = convert_time(obj["Time_departure"])
                    obj["Time_arrival"] = convert_time(obj["Time_arrival"])
                    obj["Flight_number"] = obj["Flight_number"].replace("\\u00a0", " ")
                    obj["From"] = from_airport_outer
                    obj["To"] = airport_target
                    obj["Date"] = date_inscope.strftime("%m-%d-%Y")
                    obj["Days"] = get_day_of_week(obj["Date"])

                big_data_object.append(total_result)
            except Exception as e:
                print(f"Error in scrape_and_parse: {e}")

    tasks = []
    for to_airport in to_airports:
        for date in iterate_dates(datetime_start, datetime_end):
            tasks.append(scrape_and_parse(from_airport, to_airport, date))
            tasks.append(scrape_and_parse(to_airport, from_airport, date))


    await asyncio.gather(*tasks)
    fobj = list(chain(*big_data_object))
    df = pd.json_normalize({"flights": fobj}, "flights")
    df["Date"] = pd.to_datetime(df['Date'], format='%m-%d-%Y')
    df.to_excel("baza.xlsx", index=False, engine="openpyxl")
    print("Zapisano plik baza.xlsx.")


async def main():
    from_airport = input("Podaj lotnisko wylotu:")
    print(f"Wprowadziłeś: {from_airport}\n")
    to_airports_user = input("Podaj lotnisko docelowe: (wiele lotnisk oddziel spacją.")
    print(f"Wprowadziłeś: {to_airports_user}")
    to_airports = to_airports_user.split()
    async with async_playwright() as playwright:
        await run(from_airport, to_airports, playwright)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())
