from ind_ticker.values import TICKERTAPE_MUTUTAL_FUND_SEARCH_URL

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

        mutual_fund_name = colored("Mutual Fund Name", 'cyan')
        nav = colored("Nav (INR)", 'cyan')
        one_day_change = colored("1 Day change (%)", 'cyan')

        myTable = PrettyTable(
            [mutual_fund_name, one_day_change, nav])

        row_data = [colored(mf_name, 'yellow'), mf_nav_change_1d, colored(mf_nav_close, 'blue')]
        myTable.add_row(row_data)
        myTable.add_row(['', '', ''])

        return myTable
    except:
        return None