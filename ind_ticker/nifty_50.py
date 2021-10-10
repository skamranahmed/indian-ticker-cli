import requests
from prettytable import PrettyTable
from termcolor import colored
from values import TICKERTAPE_SCREENER_QUERY_URL, NITFY_50_PAYLOAD, HEADERS

def get_nifty_50_data():
    # TODO: dynamically fetch NIFTY_50_PAYLOAD
    try:
        response = requests.post(TICKERTAPE_SCREENER_QUERY_URL, headers = HEADERS, data = NITFY_50_PAYLOAD)
        json_data = response.json()
        results = json_data["data"]["results"]
    except:
        print("Error in fetching Nifty data")
        return None

    if len(results) == 0:
        print("Error in fetching Nifty data")
        return None

    index_header = colored("Index", 'cyan')
    company_name_header = colored("Company Name", 'cyan')
    ticker_header = colored("Ticker", 'cyan')
    sector_header = colored("Sector", 'cyan')
    price_header = colored("Price (INR)", 'cyan')
    pe_ratio_header = colored("P/E Ratio", 'cyan')

    myTable = PrettyTable([index_header, company_name_header, ticker_header, sector_header, price_header, pe_ratio_header])

    company_name_list = []
    ticker_list = []
    sector_list = []
    last_price_list = []
    pe_ratio_list = []

    for result in results:
        info = result["stock"]["info"]
        company_name = colored(info["name"], 'red')
        ticker = colored(info["ticker"], 'yellow')
        sector = info["sector"]
        last_price = colored(result["stock"]["advancedRatios"]["lastPrice"], 'blue')
        pe_ratio = colored(round(result["stock"]["advancedRatios"]["apef"], 2), 'magenta')

        company_name_list.append(company_name)
        ticker_list.append(ticker)
        sector_list.append(sector)
        last_price_list.append(last_price)
        pe_ratio_list.append(pe_ratio)

    index = 1
    for company_name, ticker, sector, last_price, pe_ratio in zip(company_name_list, ticker_list, sector_list, last_price_list, pe_ratio_list):
        index_value = colored(index, 'white')
        myTable.add_row([index_value, company_name, ticker, sector, last_price, pe_ratio])
        myTable.add_row(['', '', '', '', '', ''])
        index += 1

    return myTable