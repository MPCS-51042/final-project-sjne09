import requests


class YfScraper:
    def __init__(self):
        # Referer: https://finance.yahoo.com/quote/{ticker}/analysis?p={ticker}
        # Origin: https://finance.yahoo.com
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
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
        self._session = requests.Session()
        self._cookie = self.__get_cookie()
        self._crumb = self.__get_crumb()

    def __get_cookie(self):
        url = 'https://www.yahoo.com'
        response = self._session.get(
            url, headers=self._headers, allow_redirects=True
        )
        return list(response.cookies)[0]

    def __get_crumb(self):
        url = 'https://query2.finance.yahoo.com/v1/test/getcrumb'
        response = self._session.get(
            url, headers=self._headers,
            cookies={self._cookie.name: self._cookie.value}, allow_redirects=True
        )
        return response.text

    def analyst_history(self, ticker):
        url = (f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
               f'{ticker}?modules=upgradeDowngradeHistory&formatted=false'
               f'&lang=en-US&region=US&corsDomain=finance.yahoo.com&crumb={self._crumb}'
               )
        response = self._session.get(url, headers=self._headers,
                                     cookies={self._cookie.name: self._cookie.value},
                                     allow_redirects=True
                                     )
        print(response.json())


if __name__ == '__main__':
    scraper = YfScraper()
    scraper.analyst_history('MSFT')
