import datetime
import time
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


class TwitterScraper:
    def __init__(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-blink-features=AutomationControlled")

        self._driver = webdriver.Firefox(options=options)
        self._wait = WebDriverWait(self._driver, timeout=10)
        self.__open_session()

    def __open_session(self):
        load_dotenv()
        self._driver.get('https://twitter.com/')
        self._wait.until(EC.presence_of_element_located(
            (By.XPATH, '//span[text()="Sign in"]')
        )).click()

        time.sleep(1)
        self._wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[autocomplete="username"]')
        )).send_keys(os.getenv('TWITTER_UNAME'))
        self._driver.find_element(
            By.XPATH, '//span[text()="Next"]'
        ).click()

        time.sleep(1)
        self._wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[name="password"]')
        )).send_keys(os.getenv('TWITTER_PWORD'))
        self._driver.find_element(
            By.XPATH, '//span[text()="Log in"]'
        ).click()

        time.sleep(2)

    def __search(self,
                 ticker: str,
                 date_from: datetime = None,
                 date_to: datetime = None
                 ):
        link = f'https://twitter.com/search?lang=en&q=%24{ticker}'
        if date_to is not None:
            link = link + f'%20until%3A{date_to.isoformat()}'
        if date_from is not None:
            link = link + f'%20since%3A{date_from.isoformat()}'
        link = link + '%20min_faves%3A20&src=typed_query&f=top'
        self._driver.get(link)

    def scrape(self,
               ticker: str,
               date_from: datetime = None,
               date_to: datetime = None,
               number: int = 200
               ):
        self.__search(ticker.upper(), date_from, date_to)

        tweets = set()
        time.sleep(5)
        while len(tweets) <= number:
            displayed_tweets = self._driver.find_elements(
                By.CSS_SELECTOR,
                '[class="css-901oao '
                'css-cens5h r-1nao33i '
                'r-1qd0xha r-a023e6 '
                'r-16dba41 r-rjixqe '
                'r-bcqeeo r-bnwqim '
                'r-qvutc0"]'
            )
            tweets.update(set(tweet.text for tweet in displayed_tweets))
            last_tweet = displayed_tweets[-1]
            try:
                last_tweet.send_keys(Keys.NULL)
            except ElementNotInteractableException:
                pass
            time.sleep(0.5)
        return tweets


if __name__ == '__main__':
    session = TwitterScraper()
    from_date = datetime.date(2022, 11, 9)
    to_date = datetime.date(2022, 11, 30)
    session.scrape('msft', from_date, to_date, 50)
    time.sleep(2)
    session.scrape('aapl', from_date, to_date, 50)
