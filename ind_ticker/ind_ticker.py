import click
from termcolor import colored
from nifty_50 import get_nifty_50_data

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
        Usage: python main.py nifty-50
    """
    print()
    print(f"{colored('Nifty 50', 'red')}".center(110))
    nifty_50_table = get_nifty_50_data()
    if nifty_50_table is not None:
        print(nifty_50_table)
    return

if __name__ == "__main__":
    main()