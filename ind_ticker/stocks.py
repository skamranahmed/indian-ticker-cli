import click
import requests
from prettytable import PrettyTable
from termcolor import colored

from ind_ticker.values import TICKERTAPE_STOCK_SEARCH_URL, TICKERTAPE_STOCK_SERIES_DATA_SEARCH_URL

def get_stock_data_for_duration_of_one_day(stock_name):
    duration = colored("1 Day", 'white')
    response = requests.get(TICKERTAPE_STOCK_SEARCH_URL % (stock_name))
    json_data = response.json()

    try:
        total_stocks_found = json_data["data"]["total"]
    except:
        total_stocks_found = 0

    if total_stocks_found == 0:
        return None, None, None

    try:
        stock_data = json_data["data"]["stocks"][0]
        full_stock_name = stock_data["name"]
        sector = stock_data["sector"]
        stock_quote = stock_data["quote"]

        previous_close = round(stock_quote["close"], 2)
        price = round(stock_quote["price"], 2)
        sid = stock_quote["sid"]
        high = round(stock_quote["high"], 2)
        low = round(stock_quote["low"], 2)

        one_day_return = round((price - previous_close) / (previous_close) * 100, 2)

        principal_amount = 10000
        new_amount = round(principal_amount + (principal_amount * one_day_return/100))

        if one_day_return < 0:
            one_day_return = colored(one_day_return, 'red', attrs=['blink'])
        else:
            one_day_return = colored(one_day_return, 'green')

        investment_fact = f"INR {principal_amount:,} invested yesterday would have become INR {new_amount:,} today"

        data = [
            duration,
            colored(price, 'yellow'),
            colored(previous_close, "magenta"),
            high,
            low,
            one_day_return,
            investment_fact,
        ]

        return sid, full_stock_name, sector, data
    except:
        return None, None, None


def get_stock_data_by_duration(stock_sid, duration):
    response = requests.get(TICKERTAPE_STOCK_SERIES_DATA_SEARCH_URL % (stock_sid, duration))
    json_data = response.json()

    stock_data = json_data["data"][0]
    high = round(stock_data["h"], 2)
    low = round(stock_data["l"], 2)
    previous_close = round(stock_data["points"][0]["lp"], 2)
    price = round(stock_data["points"][-1]["lp"], 2)
    percentage_return = round(stock_data["r"], 2)

    principal_amount = 10000
    new_amount = round(principal_amount + (principal_amount * percentage_return/100))

    if percentage_return < 0:
        percentage_return = colored(percentage_return, 'red', attrs=['blink'])
    else:
        percentage_return = colored(percentage_return, 'green')

    investment_duration = duration
    duration_count = ""

    if duration == "1w":
        investment_duration = colored("1 Week", "white")
        duration_count = "1 week ago"

    elif duration == "1mo":
        investment_duration = colored("1 Month", "white")
        duration_count = "1 month ago"

    elif duration == "1y":
        investment_duration = colored("1 Year", "white")
        duration_count = "1 year ago"

    elif duration == "5y":
        investment_duration = colored("5 Years", "white")
        duration_count = "5 years ago"

    investment_fact = f"INR {principal_amount:,} invested {duration_count} would have become INR {new_amount:,} today"
    
    data = [
        investment_duration,
        colored(price, "yellow"),
        colored(previous_close, "magenta"),
        high,
        low,
        percentage_return,
        investment_fact,
    ]

    return data

def get_stock_data_table(stock_name):
    row_list = []
    duration_header = colored("Duration", 'cyan')
    price_header = colored("Price (INR)", 'cyan')
    prev_close_header = colored("Previous Close (INR)", 'cyan')
    high_header = colored("High (INR)", 'cyan')
    low_header = colored("Low (INR)", 'cyan')
    percentage_return_header = colored("% Return", 'cyan')
    investment_fact_header = colored("Investment Fact", 'cyan')
    myTable = PrettyTable(
        [duration_header, price_header, prev_close_header, high_header, low_header, percentage_return_header, investment_fact_header])

    stock_id, full_stock_name, sector, row_data = get_stock_data_for_duration_of_one_day(stock_name = stock_name)
    if stock_id is None:
        stock_ticker_name = colored(stock_name, 'red')
        print(f"No data found for stock ticker name '{stock_ticker_name}'")
        return None

    row_list.append(row_data)

    row_data = get_stock_data_by_duration(stock_sid = stock_id, duration = "1w")
    row_list.append(row_data)

    row_data = get_stock_data_by_duration(stock_sid = stock_id, duration = "1mo")
    row_list.append(row_data)

    row_data = get_stock_data_by_duration(stock_sid = stock_id, duration = "1y")
    row_list.append(row_data)

    row_data = get_stock_data_by_duration(stock_sid = stock_id, duration = "5y")
    row_list.append(row_data)

    full_stock_name = click.style(full_stock_name, fg = 'red', bold = True)
    stock_sector = click.style(f"Sector - {sector}", fg = 'yellow', bold = True)
    print()
    print(f"{full_stock_name}".center(170))
    print(f"{stock_sector}".center(170))
    for row in row_list:
        myTable.add_row(row)
        myTable.add_row(['', '', '', '', '', '', ''])

    return myTable