import datetime
import time
import os
import sys

from dotenv import load_dotenv
from random import uniform
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TwitterScraper:
    def __init__(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--height=1500')
        options.add_argument('--disable-gpu')

        self._driver = webdriver.Firefox(options=options)
        self._wait = WebDriverWait(self._driver, timeout=30)
        self.__open_session()

    # TODO: new session for each date? might need to just save when successful and go to next date
    def __open_session(self):
        load_dotenv()
        self._driver.get('https://twitter.com/')
        self._wait.until(EC.presence_of_element_located(
            (By.XPATH, '//span[text()="Sign in"]')
        )).click()

        time.sleep(uniform(1, 2))
        self._wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[autocomplete="username"]')
        )).send_keys(os.getenv('TWITTER_UNAME'))
        self._driver.find_element(
            By.XPATH, '//span[text()="Next"]'
        ).click()

        time.sleep(uniform(1, 2))
        self._wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[name="password"]')
        )).send_keys(os.getenv('TWITTER_PWORD'))
        self._driver.find_element(
            By.XPATH, '//span[text()="Log in"]'
        ).click()

        time.sleep(uniform(5, 10))

    def __search(self,
                 ticker: str,
                 date_from: datetime = None,
                 date_to: datetime = None
                 ):
        url = f'https://twitter.com/search?lang=en&q=%24{ticker}'
        if date_to is not None:
            url = url + f'%20until%3A{date_to.isoformat()}'
        if date_from is not None:
            url = url + f'%20since%3A{date_from.isoformat()}'
        url = url + '&src=typed_query&f=live'
        self._driver.get(url)

    def __get_tweet(self) -> str:
        tweet_text = None
        try:
            # get the first tweet on the webpage
            tweet = self._wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[data-testid=cellInnerDiv]')
            ))
            # get tweet text if not an ad
            try:
                tweet_content = tweet.find_element(
                    By.CSS_SELECTOR,
                    '[class="css-901oao css-cens5h r-1nao33i r-1qd0xha '
                    'r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"]'
                )
                tweet_text = tweet_content.text
            except NoSuchElementException:
                pass
            try:
                self._driver.execute_script(
                    'var element = arguments[0]; element.remove();',
                    tweet
                )
            except StaleElementReferenceException:
                pass
        except Exception as e:
            print(e)
            self.end_session()
            sys.exit(-1)
        return tweet_text

    def scrape(self,
               ticker: str,
               date_from: datetime = None,
               date_to: datetime = None,
               number: int = 200
               ) -> dict[list]:
        tweets = {}
        delta = datetime.timedelta(days=1)
        current_date = date_to
        while current_date >= date_from:
            self.__search(ticker.upper(), current_date, current_date + delta)
            time.sleep(uniform(2, 5))
            tweets[current_date] = set()
            while len(tweets[current_date]) < number:
                tweet = self.__get_tweet()
                if tweet is not None:
                    tweets[current_date].add(tweet)
                if len(tweets[current_date]) % 5 == 0:
                    print(f'tweets scraped for {current_date}: {len(tweets[current_date])}')
                time.sleep(1)
            tweets[current_date] = list(tweets[current_date])
            current_date -= delta
        return tweets

    def end_session(self):
        self._driver.quit()


if __name__ == '__main__':
    session = TwitterScraper()
    from_date = datetime.date(2022, 11, 30)
    to_date = datetime.date(2022, 11, 30)
    try:
        print(session.scrape('msft', from_date, to_date, 5))
    except KeyboardInterrupt:
        session.end_session()
        sys.exit(-1)
    session.end_session()
