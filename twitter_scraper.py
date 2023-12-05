import datetime
import time
import os
import sys

from dotenv import load_dotenv
from random import uniform
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TwitterScraper:
    """
    Scrape tweets from Twitter search. Specifically tailored to searching
    for tweets including cashtags for stock tickers.
    """
    def __init__(self, headless: bool = False):
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        if headless:
            options.add_argument('--headless')

        self._driver = webdriver.Firefox(options=options)
        self._wait = WebDriverWait(self._driver, timeout=10)
        self._open_session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.end_session()

    def _open_session(self):
        """
        Opens a twitter session by logging in.

        Requires user credentials in .env file.
        """
        load_dotenv()
        self._driver.get('https://twitter.com/')
        self._wait.until(EC.presence_of_element_located(
            (By.XPATH, '//span[text()="Sign in"]')
        )).click()

        # enter username
        time.sleep(uniform(1, 2))
        self._wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[autocomplete="username"]')
        )).send_keys(os.getenv('TWITTER_UNAME'))
        self._driver.find_element(
            By.XPATH, '//span[text()="Next"]'
        ).click()

        # enter password
        time.sleep(uniform(1, 2))
        self._wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[name="password"]')
        )).send_keys(os.getenv('TWITTER_PWORD'))
        self._driver.find_element(
            By.XPATH, '//span[text()="Log in"]'
        ).click()

        # if not redirected to homepage, login failed
        time.sleep(uniform(5, 10))
        if self._driver.current_url != "https://twitter.com/home":
            print("Login failed.")
            self.end_session()
            sys.exit()

    def _search(self,
                ticker: str,
                date_from: datetime = None,
                date_to: datetime = None
                ):
        """
        Searches Twitter given params.

        Parameters
        ----------
        ticker : str
            The ticker of the stock being searched for
        date_from : datetime
            The beginning of the daterange for the search
        date_to : datetime
            The end of the daterange for the search
        """
        url = f'https://twitter.com/search?lang=en&q=%24{ticker}'
        if date_to is not None:
            url = url + f'%20until%3A{date_to.isoformat()}'
        if date_from is not None:
            url = url + f'%20since%3A{date_from.isoformat()}'
        url = url + '&src=typed_query&f=live'
        self._driver.get(url)

    def _get_tweet(self) -> str:
        """
        Gets text for the first tweet on the current webpage.

        Returns
        -------
        str
            Tweet text with newlines removed
        """
        tweet_text = None

        # get the first tweet on the webpage
        tweet = self._wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[data-testid=cellInnerDiv]')
        ))

        # get tweet text if not an ad, else move on
        try:
            tweet_text = tweet.find_element(
                By.CSS_SELECTOR,
                '[class="css-1rynq56 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x '
                'r-bcqeeo r-qvutc0 r-1qd0xha r-a023e6 r-rjixqe r-16dba41 r-bnwqim"]'
            ).text.replace('\n', '')
        except NoSuchElementException:
            pass

        # delete tweet from page html
        self._driver.execute_script(
            'var element = arguments[0]; element.remove();',
            tweet
        )
        return tweet_text

    def scrape(self,
               ticker: str,
               date_from: datetime = datetime.date.today(),
               date_to: datetime = datetime.date.today(),
               number: int = 100
               ):
        """
        Scrapes the specified number of tweets for each date in the
        provided daterange and saves to a text file located in ./data.

        Parameters
        ----------
        ticker : str
            The ticker of the stock being scraped
        date_from : datetime
            The beginning of the daterange for the scrape
        date_to : datetime
            The end of the daterange for the scrape
        number : int
            The number of tweets to scrape for each date in range
        """
        ticker = ticker.upper()
        delta = datetime.timedelta(days=1)
        current_date = date_to

        # for each date in the date range, pull specified number of tweets and write to
        # text file. Only dates where num tweets = param number will be written to file
        while current_date >= date_from:
            self._search(ticker, current_date, current_date + delta)
            time.sleep(uniform(2, 5))
            tweets = []

            while len(tweets) < number:
                tweet = self._get_tweet()
                if tweet is not None:
                    tweets.append(tweet)
                if len(tweets) % 5 == 0:
                    print(f'tweets scraped for {current_date}: {len(tweets)}')
                time.sleep(1)
            with open(f'data/{ticker}.txt', 'a+', encoding='utf-8') as f:
                for tweet in tweets:
                    f.write(f'{current_date.strftime("%m/%d/%Y")}: {tweet}\n')
            current_date -= delta

    def end_session(self):
        """
        Closes the selenium webdriver instance.
        """
        self._driver.quit()


if __name__ == '__main__':
    with TwitterScraper(headless=True) as session:
        from_date = datetime.date(2023, 10, 20)
        to_date = datetime.date(2023, 10, 20)
        try:
            session.scrape('tsla', from_date, to_date, 5)
        except KeyboardInterrupt:
            session.end_session()
            sys.exit()
