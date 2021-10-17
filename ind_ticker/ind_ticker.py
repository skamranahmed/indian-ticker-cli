import click
from termcolor import colored

from ind_ticker.nifty_50 import get_nifty_50_data
from ind_ticker.stocks import get_stock_data_table, get_annual_growth_stock_data

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
def stock(stock_name, annualanalysis):
    """
    Usage: ind-ticker stock <stock_name_without_spaces>
    Example: ind-ticker stock State-Bank-Of-India
    """
    print(f"Getting stock data of {stock_name}!")
    stock_data_table = get_stock_data_table(stock_name)
    if stock_data_table is not None:
        print(stock_data_table)

    if annualanalysis:
        print(f"Getting annual analysis data {stock_name}!")
        annual_analysis_table = get_annual_growth_stock_data(stock_name)
        if annual_analysis_table is not None:
            annual_analysis = click.style("Annual Analysis", fg='red', bold=True)
            print()
            print(f"{annual_analysis}".center(90))
            print(annual_analysis_table)
        else:
            print(f"Annual analysis for {stock_name} not found")
        
    return

if __name__ == "__main__":
    main()