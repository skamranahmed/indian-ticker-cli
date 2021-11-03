# 🔥 Indian Ticker

👨‍💻 CLI Tool for getting data of Indian Stocks and Mutual Funds 📈

## Installation

Make sure that you are running Python 3.7 or later

```bash
pip install termcolor ind-ticker
```

#### To get Nifty-50 data:

```bash
  ind-ticker nifty-50
```

![](./.assets/nifty50.gif)

#### To get the stock data of a single company:

```bash
  ind-ticker stock <comapny_name_without_spaces>
```

Example:

```bash
  ind-ticker stock Reliance
```

![](./.assets/single-stock-data.gif)

#### To get the stock data of multiple companies:

```bash
  ind-ticker stocks <comapny_name1_without_spaces> <company_name2_without_spaces>
```

Example:

```bash
  ind-ticker stocks Biocon Cipla
```

![](./.assets/multiple-stocks-data.gif)

#### To get the stock data of a company including the annual analysis:

```bash
  ind-ticker stock <comapny_name_without_spaces> -aa
```

Example:

```bash
  ind-ticker stock Avanti-Feeds -aa
```

![](./.assets/annual-analysis.gif)

#### To get the stock data of a company including the quarterly analysis:

```bash
  ind-ticker stock <comapny_name_without_spaces> -qa
```

Example:

```bash
  ind-ticker stock Titan -qa
```

![](./.assets/quarterly-analysis.gif)

#### To get the stock data of a company including both the analysis:

```bash
  ind-ticker stock <comapny_name_without_spaces> -aa -qa
```

Example:

```bash
  ind-ticker stock Adani-Green -aa -qa
```

![](./.assets/both-analysis.gif)

#### To get data of a Mutual Fund Scheme:

```bash
  ind-ticker mf <mutual_fund_scheme_name>
```

Example:

```bash
  ind-ticker mf mirae-asset-tax-saver
```

![](./.assets/mutual-fund.gif)
