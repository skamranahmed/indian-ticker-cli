import click

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
    print("Nifty 50 Data")
    return

if __name__ == "__main__":
    main()