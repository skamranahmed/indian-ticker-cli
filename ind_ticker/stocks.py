import click
import requests
from prettytable import PrettyTable
from termcolor import colored

from datetime import date

from ind_ticker.values import (
    TICKERTAPE_STOCK_SEARCH_URL, 
    TICKERTAPE_STOCK_SERIES_DATA_SEARCH_URL, 
    TICKERTAPE_STOCK_ANNUAL_ANALYSIS_DATA_URL,
    TICKERTAPE_STOCK_ANNUAL_ANALYSIS_BALANCESHEET_DATA_URL,
    TICKERTAPE_STOCK_ANNUAL_ANALYSIS_NORMAL_DATA_URL
)

# create a request session object for faster results while making http requests
s = requests.Session()

def get_stock_data_for_duration_of_one_day(stock_name):
    duration = colored("1 Day", 'white')
    response = s.get(TICKERTAPE_STOCK_SEARCH_URL % (stock_name))
    json_data = response.json()

    try:
        total_stocks_found = json_data["data"]["total"]
    except:
        total_stocks_found = 0

    if total_stocks_found == 0:
        return None, None, None, None

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
        return None, None, None, None


def get_stock_data_by_duration(stock_sid, duration):
    response = s.get(TICKERTAPE_STOCK_SERIES_DATA_SEARCH_URL % (stock_sid, duration))
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

    elif duration == "max":
        todays_date = date.today()
        ipo_data = stock_data["points"][0]["ts"].split("-")
        ipo_year = int(ipo_data[0])
        year_count = todays_date.year - ipo_year
        investment_duration = colored(f"{year_count} Years", "white")
        duration_count = f"{year_count} years ago"

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
        print(f"No data found for stock name '{stock_ticker_name}'")
        return None
    row_list.append(row_data)

    full_stock_name = click.style(full_stock_name, fg = 'red', bold = True)
    stock_sector = click.style(f"Sector - {sector}", fg = 'yellow', bold = True)
    print()
    print(f"{full_stock_name}".center(170))
    print(f"{stock_sector}".center(170))


    duration_list = ["1w", "1mo", "1y", "5y", "max"]
    for duration in duration_list:
        row_data = get_stock_data_by_duration(stock_sid = stock_id, duration = duration)
        row_list.append(row_data)

    for row in row_list:
        myTable.add_row(row)
        myTable.add_row(['', '', '', '', '', '', ''])

    return myTable

def get_annual_growth_stock_data(stock_name):
    stock_id, full_stock_name, sector, row_data = get_stock_data_for_duration_of_one_day(stock_name = stock_name)
    response = s.get(TICKERTAPE_STOCK_ANNUAL_ANALYSIS_DATA_URL % (stock_id))
    json_data = response.json()

    try:
        last_four_year_annual_data = json_data["data"][-4:]
    except:
        stock_ticker_name = colored(stock_name, 'red')
        print(f"Annual analysis data not found for stock name '{stock_ticker_name}'")
        return None

    eps_growth_data = [colored("EPS Growth (%)", "yellow")]
    net_income_growth_data = [colored("Net Income Growth (%)", "yellow")]
    financial_year_name = []

    for year_data in last_four_year_annual_data:
        eps = round(year_data["incEps"], 2)
        net_income = round(year_data["incNinc"], 2)
        financial_year_period = year_data["displayPeriod"].replace(" ", "").replace("FY'", "20")

        if eps < 0:
            eps = colored(eps, 'red')
        else:
            eps = colored(eps, 'green')

        if net_income < 0:
            net_income = colored(net_income, 'red')
        else:
            net_income = colored(net_income, 'green')

        eps_growth_data.append(eps)
        net_income_growth_data.append(net_income)
        financial_year_name.append(financial_year_period)

    debt_to_equity_ratio_data, current_ratio_data, long_term_debt_data, roe_data, roce_data = get_financial_ratios(stock_id)

    if debt_to_equity_ratio_data is None:
        stock_ticker_name = colored(stock_name, 'red')
        print(f"Annual analysis data not found for stock name '{stock_ticker_name}'")
        return None

    row_list = []
    financial_year_header = colored("Financial Year", 'cyan')
    fy_1 = colored(financial_year_name[0], 'cyan')
    fy_2 = colored(financial_year_name[1], 'cyan')
    fy_3 = colored(financial_year_name[2], 'cyan')
    fy_4 = colored(financial_year_name[3], 'cyan')
    myTable = PrettyTable(
        [financial_year_header, fy_1, fy_2, fy_3, fy_4])

    row_list.append(eps_growth_data)
    row_list.append(net_income_growth_data)
    row_list.append(debt_to_equity_ratio_data)
    row_list.append(current_ratio_data)
    row_list.append(long_term_debt_data)
    row_list.append(roe_data)
    row_list.append(roce_data)

    for row in row_list:
        myTable.add_row(row)
        myTable.add_row(['', '', '', '', ''])
    return myTable

def get_financial_ratios(stock_id):
    balance_sheet_response = s.get(TICKERTAPE_STOCK_ANNUAL_ANALYSIS_BALANCESHEET_DATA_URL % (stock_id))
    json_data = balance_sheet_response.json()

    try:
        last_four_year_balance_sheet_data = json_data["data"][-4:]
    except:
        return None, None, None, None, None

    debt_to_equity_ratio_data = [colored("Debt/Equity Ratio", "yellow")]
    current_ratio_data = [colored("Current Ratio", "yellow")]
    roe_data = [colored("ROE (%)", "yellow")]
    roce_data = [colored("ROCE (%)", "yellow")]
    long_term_debt_data = [colored("Long Term Debt (in Cr)", "yellow")]

    annual_normal_response = s.get(TICKERTAPE_STOCK_ANNUAL_ANALYSIS_NORMAL_DATA_URL % (stock_id))
    annual_normal_json_data = annual_normal_response.json()

    try:
        last_four_year_annual_normal_data = annual_normal_json_data["data"][-4:]
    except:
        return None, None, None, None, None

    for yearly_bs_data, yearly_income_data in zip(last_four_year_balance_sheet_data, last_four_year_annual_normal_data):
        total_long_term_debt = yearly_bs_data["balTltd"]
        total_equity = yearly_bs_data["balTeq"]
        net_income = yearly_income_data["incNinc"]
        pbit = yearly_income_data["incPbi"]
        total_assets = yearly_bs_data["balTota"]
        current_liabilities = yearly_bs_data["balTcl"]
        accounts_payable = yearly_bs_data["balAccp"]
        total_current_assets = yearly_bs_data["balTca"]

        long_term_debt = round(total_long_term_debt, 2)

        # return_on_equity = (net_income / total_equity) * 100
        roe = round((net_income/total_equity)*100, 2)
        
        # return_on_captial_employed = ( (PBIT) / (total_assets - current_liabilities) ) * 100 
        roce = round(pbit/(total_assets-current_liabilities)*100, 2)

        # debt_to_equity_ratio = ( (accounts_payable + total_long_term_debt) / total_equity )
        debt_to_equity_ratio = round((accounts_payable + total_long_term_debt)/total_equity, 2)

        if debt_to_equity_ratio > 2 or debt_to_equity_ratio < 0:
            debt_to_equity_ratio = colored(debt_to_equity_ratio, "red")
        else:
            debt_to_equity_ratio = colored(debt_to_equity_ratio, "green")

        #  current_ratio = total_current_assets/total_current_liabilities
        current_ratio = round(total_current_assets/current_liabilities, 2) 
        debt_to_equity_ratio_data.append(debt_to_equity_ratio)
        current_ratio_data.append(current_ratio)
        roe_data.append(roe)
        roce_data.append(roce)
        long_term_debt_data.append(long_term_debt)

    return debt_to_equity_ratio_data, current_ratio_data, long_term_debt_data, roe_data, roce_data