import click
from termcolor import colored

from ind_ticker.nifty_50 import get_nifty_50_data
from ind_ticker.stocks import (
    get_stock_data_table,
    get_stock_data_table_for_list_of_stocks,
    get_annual_growth_stock_data,
    get_quarterly_growth_stock_data
)
from ind_ticker.mutual_funds import get_mutual_fund_data

version = "0.0.4"

@click.group()
def main():
    """A CLI Tool to get data of Indian Stocks and Mutual Funds"""
    pass

#  get nifty-50 data
@main.command()
@click.option("--nifty50")
def nifty_50(nifty50):
    """
        Usage: ind-ticker nifty-50
    """
    print()
    print(f"{colored('Nifty 50', 'red')}".center(110))
    nifty_50_table = get_nifty_50_data()
    if nifty_50_table is not None:
        print(nifty_50_table)
    return

#  get stock data of a single company
@main.command()
@click.argument("stock_name", nargs = 1)
@click.option("--annualanalysis", "-aa", is_flag = True, type = bool)
@click.option("--quarteranalysis", "-qa", is_flag = True, type = bool)
def stock(stock_name, annualanalysis, quarteranalysis):
    """
    Usage: ind-ticker stock <stock_name_without_spaces>
    Example: ind-ticker stock State-Bank-Of-India
    """
    print(f"Getting stock data of {stock_name}!")
    stock_data_table = get_stock_data_table(stock_name)

    if stock_data_table is None:
        # if no data is found for the given stock, then no need to perform any other operations
        return
    else:
        print(stock_data_table)

    if annualanalysis:
        print(f"Getting annual analysis data of {stock_name}!")
        annual_analysis_table = get_annual_growth_stock_data(stock_name)
        if annual_analysis_table is not None:
            annual_analysis = click.style("Annual Analysis", fg='red', bold=True)
            print()
            print(f"{annual_analysis}".center(90))
            print(annual_analysis_table)

    if quarteranalysis:
        print(f"Getting quarterly analysis data of {stock_name}!")
        quarter_analysis_table = get_quarterly_growth_stock_data(stock_name)
        if quarter_analysis_table is not None:
            quarterly_analysis = click.style("Quarterly Analysis", fg='red', bold=True)
            print()
            print(f"{quarterly_analysis}".center(90))
            print(quarter_analysis_table)
        
    return

#  get stock data of multiple companies
@main.command()
@click.argument("stock_names", nargs = -1)
def stocks(stock_names):
    """
        Usage: ind-ticker stocks tickers <stock_name_1_without_spaces> <stock_name_2_without_spaces> ......
        Example: ind-ticker stocks Airtel Reliance MRF
    """
    stock_names = list(stock_names)
    print(f"Getting stock data of {stock_names}!")
    get_stock_data_table_for_list_of_stocks(stock_names)
    return

#  get mutual fund data
@main.command()
@click.argument("mutual_fund_name", nargs = 1)
def mf(mutual_fund_name):
    """
    Usage: ind-ticker stock <stock_name_without_spaces>
    Example: ind-ticker stock State-Bank-Of-India
    """
    print(f"Getting mutual fund data of {mutual_fund_name}!")
    mf_data_table = get_mutual_fund_data(mutual_fund_name)
    if mf_data_table is None:
        # if no data is found for the given mutual fund, then no need to perform any other operations
        return
    else:
        print(mf_data_table)

    return

if __name__ == "__main__":
    main()