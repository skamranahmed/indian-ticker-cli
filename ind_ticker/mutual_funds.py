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
    # this is for getting the mutual fund id by using the mutual fund name
    response = s.get(TICKERTAPE_MUTUTAL_FUND_SEARCH_URL % (mf_name), headers = {"accept-version": "6.9.2"})
    json_data = response.json()

    try:
        total_mfs_found = json_data["data"]["total"]
    except:
        total_mfs_found = 0

    if total_mfs_found == 0:
        mutual_fund_name = colored(mf_name, 'red')
        print(f"No data found for mutual fund '{mutual_fund_name}'")
        return None

    try:
        mf_data = json_data["data"]["items"][0]
        mf_name = mf_data["name"]
        mf_id = mf_data["id"]

        full_mf_name = click.style(mf_name, fg = 'red', bold = True)
        print(f"{full_mf_name}".center(170))

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
            if row_data is None:
                continue
            row_list.append(row_data)
        
        if len(row_list) == 0:
            mutual_fund_name = colored(mf_name, 'red')
            print(f"No data found for mutual fund '{mutual_fund_name}'")
            return None

        for row in row_list:
            myTable.add_row(row)
            myTable.add_row(['', '', '', '', '', ''])

        return myTable
    except:
        return None

def get_mutual_fund_data_by_duration(mf_id, duration):
    response = s.get(TICKERTAPE_MUTUAL_FUND_SERIES_DATA_SEARCH_URL % (mf_id, duration), headers = {"accept-version": "6.9.2"})
    json_data = response.json()

    try:
        mf_data = json_data["data"][0]
        high = round(mf_data["h"], 2)
        low = round(mf_data["l"], 2)
        abosulute_returns = round(mf_data["r"], 2)
        current_nav = colored(round(mf_data["points"][-1]["lp"],2), "yellow")
        cagr_returns = mf_data.get("cagr", "-")

        if cagr_returns != "-":
            if cagr_returns < 0:
                cagr_returns = colored(round(cagr_returns, 2), 'red')
            else:
                cagr_returns = colored(round(cagr_returns, 2), 'green')

        if abosulute_returns < 0:
            abosulute_returns = colored(abosulute_returns, 'red')
        else:
            abosulute_returns = colored(abosulute_returns, 'green')

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

        row_data = [investment_duration, current_nav, high, low, abosulute_returns, cagr_returns]
        return row_data
    except:
        return None