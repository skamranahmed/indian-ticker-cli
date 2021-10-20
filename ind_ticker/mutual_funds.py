from ind_ticker.values import (
    TICKERTAPE_MUTUTAL_FUND_SEARCH_URL,
    TICKERTAPE_MUTUAL_FUND_SERIES_DATA_SEARCH_URL
)

import click
from prettytable import PrettyTable
import requests
from termcolor import colored

# create a request session object for faster results while making http requests
s = requests.Session()

def get_mutual_fund_data(mf_name):
    response = s.get(TICKERTAPE_MUTUTAL_FUND_SEARCH_URL % (mf_name), headers = {"accept-version": "6.9.2"})
    json_data = response.json()

    try:
        total_mfs_found = json_data["data"]["total"]
    except:
        total_mfs_found = 0

    if total_mfs_found == 0:
        return None

    try:
        mf_data = json_data["data"]["items"][0]
        mf_name = mf_data["name"]
        mf_id = mf_data["id"]
        mf_quote = mf_data["quote"]
        mf_nav_close = round(mf_quote["navClose"], 2)
        mf_nav_change_1d = round(mf_quote["navCh1d"],2)

        if mf_nav_change_1d < 0:
            mf_nav_change_1d = colored(mf_nav_change_1d, 'red')
        else:
            mf_nav_change_1d = colored(mf_nav_change_1d, 'green')

        full_mf_name = click.style(mf_name, fg = 'red', bold = True)
        print(f"{full_mf_name}".center(170))

        # mutual_fund_name = colored("Mutual Fund Name", 'cyan')
        # nav = colored("Nav (INR)", 'cyan')
        # one_day_change = colored("1 Day change (%)", 'cyan')

        # myTable = PrettyTable(
        #     [mutual_fund_name, one_day_change, nav])

        # row_data = [colored(mf_name, 'yellow'), mf_nav_change_1d, colored(mf_nav_close, 'blue')]
        # myTable.add_row(row_data)
        # myTable.add_row(['', '', ''])

        row_list = []
        duration_header = colored("Duration", 'cyan')
        current_nav_header = colored("Current NAV (INR)", 'cyan')
        high_header = colored("High (INR)", 'cyan')
        low_header = colored("Low (INR)", 'cyan')
        percentage_abs_return_header = colored("Absolute Returns (%)", 'cyan')
        percentage_cagr_return_header = colored("CAGR Returns (%)", 'cyan')

        myTable = PrettyTable(
            [duration_header, current_nav_header, high_header, low_header, percentage_abs_return_header, percentage_cagr_return_header])


        duration_list = ["1mo", "6mo", "1y", "3y", "5y"]
        for duration in duration_list:
            row_data = get_mutual_fund_data_by_duration(mf_id = mf_id, duration = duration)
            row_list.append(row_data)


        for row in row_list:
            myTable.add_row(row)
            myTable.add_row(['', '', '', '', '', ''])

        return myTable
    except:
        print("I am here")
        return None

def get_mutual_fund_data_by_duration(mf_id, duration):

    # Duration, Current NAV, High, Low, Absolute Returns, CAGR
    response = s.get(TICKERTAPE_MUTUAL_FUND_SERIES_DATA_SEARCH_URL % (mf_id, duration), headers = {"accept-version": "6.9.2"})
    json_data = response.json()

    mf_data = json_data["data"][0]
    high = mf_data["h"]
    low = mf_data["l"]
    abosulute_returns = mf_data["r"]
    current_nav = mf_data["points"][-1]["lp"]
    carg_returns = "-"

    if duration == "1mo":
        investment_duration = colored("1 Month", "white")

    elif duration == "6mo":
        investment_duration = colored("6 Month", "white")

    elif duration == "1y":
        investment_duration = colored("1 Year", "white")

    elif duration == "3y":
        investment_duration = colored("3 Years", "white")

    elif duration == "5y":
        investment_duration = colored("5 Years", "white")

    row_data = [investment_duration, current_nav, high, low, abosulute_returns, carg_returns]

    return row_data