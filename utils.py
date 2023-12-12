from datetime import datetime
import datetime as dt

from playwright.async_api import expect


# HELPER FUNCTIONS
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


def iterate_dates(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += dt.timedelta(days=1)

def aria_button_search(date_string):
    try:
        # Parse input date string
        input_date = datetime.strptime(date_string, "%m-%d-%Y")

        # Format the output message
        formatted_message = (
            f"Done. Search for one-way flights, departing on {input_date.strftime('%B %d, %Y')}"
        )

        return formatted_message

    except ValueError:
        # Handle invalid date format
        return "Invalid date format. Please use 'mm-dd-yyyy'."

async def fill_and_assert(element, fill_value, times):
    await element.fill(fill_value)
    expect(element).toHaveValue(fill_value)

def get_page_content(parser):
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
        operator = result.css_first('.kSwLQc')
        optext = "" if operator is None else operator.text()
        op = optext.split("by", 1)[1].strip() if "by" in optext else optext
        flight_number = result.css_first('.MX5RWe span:nth-child(4)').text()

        flight_data = {
            'Time_departure': time_departure,
            'Time_arrival': time_arrival,
            'company': company,
            'airplane': airplane,
            'Flight_number': flight_number,
            'Operator': company if operator is None else op
        }
        all_data.append(flight_data)
    return all_data