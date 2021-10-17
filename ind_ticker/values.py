HEADERS = {'content-type': 'application/json;charset=UTF-8'}

NITFY_50_PAYLOAD = '{"match":{},"sortBy":"mrktCapf","sortOrder":-1,"sids":["APSE","ASPN","AXBK","BPCL","BAJA","BJFN","BJFS","BRTI","BRIT","CIPL","COAL","DIVI","REDY","EICH","GRAS","HDFC","HCLT","HDBK","HDFL","HROM","HLL","HALC","IOC","ICBK","INBK","INFY","ITC","JSTL","KTKM","LART","MAHM","MRTI","NEST","NTPC","ONGC","PGRD","RELI","SBIL","SHCM","SBI","SUN","TACN","TAMO","TISC","TCS","TEML","TITN","ULTC","UPLL","WIPR"],"project":["subindustry","mrktCapf","lastPrice","apef"],"offset":0,"count":50}'

TICKERTAPE_SCREENER_QUERY_URL = 'https://api.tickertape.in/screener/query'

TICKERTAPE_STOCK_SEARCH_URL = 'https://api.tickertape.in/search?text=%s&types=stock'

TICKERTAPE_STOCK_SERIES_DATA_SEARCH_URL = 'https://api.tickertape.in/stocks/charts/inter/%s?duration=%s'

TICKERTAPE_STOCK_ANNUAL_ANALYSIS_DATA_URL = 'https://api.tickertape.in/stocks/financials/income/%s/annual/growth?count=10'

TICKERTAPE_STOCK_ANNUAL_ANALYSIS_BALANCESHEET_DATA_URL = 'https://api.tickertape.in/stocks/financials/balancesheet/%s/annual/normal?count=10'