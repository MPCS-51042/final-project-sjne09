import datetime
import requests
import pandas as pd

from dateutil.relativedelta import relativedelta


class YfScraper:

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

    _URLS = {
        'validate':
            'https://query2.finance.yahoo.com/v6/finance/quote/validate',
        'quote_summary':
            'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}',
        'historical_prices':
            'https://query1.finance.yahoo.com/v8/finance/chart'
    }

    def __init__(self):
        self._session = requests.Session()
        self._cookie = self._get_cookie()
        self._crumb = self._get_crumb()

    def _get_cookie(self):
        url = 'https://www.yahoo.com'
        response = self._session.get(
            url, headers=self._HEADERS,
            allow_redirects=True
        )
        return list(response.cookies)[0]

    def _get_crumb(self):
        url = 'https://query2.finance.yahoo.com/v1/test/getcrumb'
        response = self._session.get(
            url, headers=self._HEADERS,
            cookies={self._cookie.name: self._cookie.value},
            allow_redirects=True
        )
        return response.text

    def _validate(self, ticker: str):
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

    def get_upgrades_downgrades(self, ticker: str):
        modules = ['upgradeDowngradeHistory']
        data = self.get_quote_summary(ticker, modules)
        if data['quoteSummary']['result'] is None:
            return

        df = pd.DataFrame.from_dict(
            data['quoteSummary']['result'][0]['upgradeDowngradeHistory']['history']
        )
        return df

    def get_recommendation_trend(self, ticker: str):
        modules = ['recommendationTrend']
        data = self.get_quote_summary(ticker, modules)
        return data

    def get_asset_profile(self, ticker: str):
        modules = ['assetProfile']
        data = self.get_quote_summary(ticker, modules)
        return data

    def get_calendar_events(self, ticker: str):
        modules = ['calendarEvents']
        data = self.get_quote_summary(ticker, modules)
        return data

    def get_summary_profile(self, ticker: str):
        modules = ['summaryProfile']
        data = self.get_quote_summary(ticker, modules)
        return data

    def get_quote_summary(self, ticker: str, modules: list):
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
                              interval: str = '1d'):
        self._validate(ticker)
        if date_to is None:
            date_to = datetime.datetime.now()
        if date_from is None:
            date_from = date_to - relativedelta(years=1)

        url = self._URLS['historical_prices'] + f'/{ticker}'
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

        data = response.json()['chart']['result'][0]
        timestamps = data['timestamp']
        close_prices = data['indicators']['quote'][0]['close']
        volume = data['indicators']['quote'][0]['volume']
        df = pd.DataFrame()
        df['date'] = timestamps
        df['price'] = close_prices
        df['volume'] = volume
        return df


if __name__ == '__main__':
    scraper = YfScraper()
    tickers = ['^GSPC']
    # with open('data/sp500.csv', 'r') as f:
    #     reader = csv.DictReader(f)
    #     for line in reader:
    #         ticker = line['Symbol'].replace('.', '-')
    #         tickers.append(ticker)

    # with open('data/gradingHistory.csv', 'w') as f:
    #     for i, ticker in enumerate(tickers):
    #         print(ticker)
    #         df = scraper.get_upgrades_downgrades(ticker)
    #         if df is not None:
    #             df['ticker'] = ticker
    #             if i == 0:
    #                 df.to_csv(f, header=True, index=False, lineterminator='\n')
    #             else:
    #                 df.to_csv(f, header=False, index=False, lineterminator='\n')

    with open('data/spxHistory.csv', 'w') as f:
        for i, ticker in enumerate(tickers):
            print(ticker)
            df = scraper.get_historical_prices(
                ticker,
                date_from=datetime.datetime(2014, 11, 1),
                date_to=datetime.datetime(2023, 11, 25),
                interval='1d'
            )
            df['ticker'] = ticker
            if df is not None:
                if i == 0:
                    df.to_csv(f, header=True, index=False, lineterminator='\n')
                else:
                    df.to_csv(f, header=False, index=False, lineterminator='\n')
