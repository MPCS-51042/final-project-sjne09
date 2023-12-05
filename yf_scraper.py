import datetime
import http
import requests
import pandas as pd

from dateutil.relativedelta import relativedelta
from typing import Optional


class YfScraper:
    """
    Scrape stock data from yahoo finance.
    """

    # html request headers
    _HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
                      'Win64; x64; rv:109.0) '
                      'Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,'
                  'application/xml;q=0.9,image/avif,'
                  'image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers'
    }

    # yahoo finance API URLs
    _URLS = {
        'validate':
            'https://query2.finance.yahoo.com/v6/finance/quote/validate',
        'quote_summary':
            'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}',
        'historical_prices':
            'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'
    }

    def __init__(self):
        self._session = requests.Session()
        self._cookie = self._get_cookie()
        self._crumb = self._get_crumb()

    def _get_cookie(self) -> http.cookiejar.Cookie:
        """
        Get a cookie from yahoo. Required in order to get a crumb.

        Returns
        -------
        http.cookiejar.Cookie
            A Cookie object that is a valid cookie for the current requests
            session
        """
        url = 'https://www.yahoo.com'
        response = self._session.get(
            url, headers=self._HEADERS,
            allow_redirects=True
        )
        return list(response.cookies)[0]

    def _get_crumb(self) -> str:
        """
        Get a crumb from yahoo finance. Some API queries require a crumb
        in order to get a response.

        Returns
        -------
        str
            A crumb for the current requests session corresponding to session
            cookie
        """
        url = 'https://query2.finance.yahoo.com/v1/test/getcrumb'
        response = self._session.get(
            url, headers=self._HEADERS,
            cookies={self._cookie.name: self._cookie.value},
            allow_redirects=True
        )
        return response.text

    def _validate(self, ticker: str):
        """
        Utilizes yahoo finance's API to validate that ticker param exists.
        If ticker is invalid, raise exception.

        Parameters
        ----------
        ticker : str
            Stock ticker/symbol to be validated
        """
        url = self._URLS['validate']
        params = {
            'symbols': ticker
        }
        response = self._session.get(
            url, params=params,
            headers=self._HEADERS,
            cookies={self._cookie.name: self._cookie.value},
            allow_redirects=True
        )
        result = response.json()['symbolsValidation']['result'][0][ticker]
        try:
            assert result is True
        except AssertionError:
            raise ValueError(f'{ticker} is not valid.')

    def get_upgrades_downgrades(self, ticker: str) -> Optional[pd.DataFrame]:
        """
        Gets historical analyst report data for specified ticker.

        Parameters
        ----------
        ticker : str
            Stock ticker/symbol

        Returns
        -------
        pd.DataFrame
            A dataframe containing all report history in yahoo finance's API
            for specified stock ticker
            If no data is available, returns None.
        """
        modules = ['upgradeDowngradeHistory']
        data = self.get_quote_summary(ticker.upper(), modules)
        if data['quoteSummary']['result'] is None:
            return

        df = pd.DataFrame.from_dict(
            data['quoteSummary']['result'][0]['upgradeDowngradeHistory']['history']
        )
        return df

    def get_recommendation_trend(self, ticker: str) -> dict:
        """
        Gets recommendation trend data for specified ticker.

        Parameters
        ----------
        ticker : str
            Stock ticker/symbol

        Returns
        -------
        dict
            A raw json response from yahoo finance API
        """
        modules = ['recommendationTrend']
        data = self.get_quote_summary(ticker, modules)
        return data

    def get_asset_profile(self, ticker: str):
        """
        Gets asset profile data for specified ticker.

        Parameters
        ----------
        ticker : str
            Stock ticker/symbol

        Returns
        -------
        dict
            A raw json response from yahoo finance API
        """
        modules = ['assetProfile']
        data = self.get_quote_summary(ticker, modules)
        return data

    def get_calendar_events(self, ticker: str):
        """
        Gets calendar events data for specified ticker.

        Parameters
        ----------
        ticker : str
            Stock ticker/symbol

        Returns
        -------
        dict
            A raw json response from yahoo finance API
        """
        modules = ['calendarEvents']
        data = self.get_quote_summary(ticker, modules)
        return data

    def get_summary_profile(self, ticker: str):
        """
        Gets summary profile data for specified ticker.

        Parameters
        ----------
        ticker : str
            Stock ticker/symbol

        Returns
        -------
        dict
            A raw json response from yahoo finance API
        """
        modules = ['summaryProfile']
        data = self.get_quote_summary(ticker, modules)
        return data

    def get_quote_summary(self, ticker: str, modules: list) -> dict:
        """
        Gets requested data from yahoo finance

        Parameters
        ----------
        ticker : str
            Stock ticker/symbol
        modules : list
            The data to be returned. Valid modules are:
            'assetProfile', 'summaryProfile', 'summaryDetail', 'esgScores', 'price',
            'incomeStatementHistory', 'incomeStatementHistoryQuarterly',
            'balanceSheetHistory', 'balanceSheetHistoryQuarterly',
            'cashflowStatementHistory', 'cashflowStatementHistoryQuarterly',
            'defaultKeyStatistics', 'financialData', 'calendarEvents',
            'secFilings', 'recommendationTrend', 'upgradeDowngradeHistory',
            'institutionOwnership', 'fundOwnership', 'majorDirectHolders',
            'majorHoldersBreakdown', 'insiderTransactions', 'insiderHolders',
            'netSharePurchaseActivity', 'earnings', 'earningsHistory',
            'earningsTrend', 'industryTrend', 'indexTrend', 'sectorTrend'

        Returns
        -------
        dict
            A raw json response from yahoo finance API
        """
        ticker = ticker.upper()
        self._validate(ticker)
        url = self._URLS['quote_summary'].format(ticker=ticker)
        params = {
            'modules': modules,
            'crumb': self._crumb
        }
        response = self._session.get(
            url, params=params,
            headers=self._HEADERS,
            cookies={self._cookie.name: self._cookie.value},
            allow_redirects=True
        )
        return response.json()

    def get_historical_prices(self,
                              ticker: str,
                              date_from: datetime = None,
                              date_to: datetime = None,
                              interval: str = '1d') -> pd.DataFrame:
        """
        Gets historical price and volume data for a stock.

        Parameters
        ----------
        ticker : str
            Stock ticker/symbol
        date_from : datetime
            Beginning of the date interval to get prices for
        date_to : datetime
            End of the date interval to get prices for
        interval : str
            The frequency of prices in the return dataframe. Valid options are:
            1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

        Returns
        -------
        pd.DataFrame
            A dataframe containing the historical price and volume data
        """
        ticker = ticker.upper()
        self._validate(ticker)
        if date_to is None:
            date_to = datetime.datetime.now()
        if date_from is None:
            date_from = date_to - relativedelta(years=1)

        url = self._URLS['historical_prices'].format(ticker=ticker)
        params = {
            'period1': str(int(date_from.timestamp())),
            'period2': str(int(date_to.timestamp())),
            'interval': interval
        }
        response = self._session.get(
            url, params=params,
            headers=self._HEADERS,
            cookies={self._cookie.name: self._cookie.value},
            allow_redirects=True
        )

        # build dataframe from response data
        data = response.json()['chart']['result'][0]
        timestamps = data['timestamp']
        close_prices = data['indicators']['quote'][0]['close']
        volume = data['indicators']['quote'][0]['volume']
        df = pd.DataFrame()
        df['date'] = timestamps
        df['price'] = close_prices
        df['volume'] = volume
        return df

    def get_chart_data(self, ticker: str) -> dict:
        """
        Gets chart data including basic stock data, current price, etc.

        Parameters
        ----------
        ticker : str
            Stock ticker/symbol

        Returns
        -------
        dict
            A raw json response from yahoo finance API
        """
        ticker = ticker.upper()
        self._validate(ticker)
        url = self._URLS['historical_prices'].format(ticker=ticker)
        response = self._session.get(
            url, headers=self._HEADERS,
            cookies={self._cookie.name: self._cookie.value},
            allow_redirects=True
        )
        return response.json()['chart']['result'][0]['meta']

    def get_current_price(self, ticker: str) -> float:
        """
        Gets the current market price for a stock

        Parameters
        ----------
        ticker : str
            Stock ticker/symbol

        Returns
        -------
        float
            Current market price
        """
        return self.get_chart_data(ticker)['regularMarketPrice']

    def get_previous_close(self, ticker: str) -> float:
        """
        Gets the previous closing price for a stock

        Parameters
        ----------
        ticker : str
            Stock ticker/symbol

        Returns
        -------
        float
            Previous closing price
        """
        return self.get_chart_data(ticker)['chartPreviousClose']


if __name__ == '__main__':
    pass
