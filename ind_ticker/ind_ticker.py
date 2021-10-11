import click
from termcolor import colored

from ind_ticker.nifty_50 import get_nifty_50_data

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
def stock(stock_name):
    """
    Usage: ind-ticker stock <stock_name_without_spaces>
    Example: ind-ticker stock State-Bank-Of-India
    """

    print(f"Getting stock data of {stock_name}!")
    return

if __name__ == "__main__":
    main()