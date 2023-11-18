import datetime
import sys

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from twitter_scraper import TwitterScraper


def main(session: TwitterScraper):
    from_date = datetime.date(2022, 11, 15)
    to_date = datetime.date(2022, 11, 16)
    n = 200
    tweets = session.scrape('msft', from_date, to_date, n)

    for day in tweets.keys():
        sum_neg = 0
        sum_neu = 0
        sum_pos = 0

        for tweet in tweets[day]:
            sid = SentimentIntensityAnalyzer()
            ss = sid.polarity_scores(tweet)
            print(ss)
            sum_neg += ss['neg']
            sum_neu += ss['neu']
            sum_pos += ss['pos']

        avg_neg = sum_neg / n
        avg_neu = sum_neu / n
        avg_pos = sum_pos / n

        print(f'{day}: {avg_neg}, {avg_neu}, {avg_pos}, {avg_neg + avg_neu + avg_pos}')


if __name__ == '__main__':
    session = TwitterScraper()
    try:
        main(session)
        session.end_session()
    except KeyboardInterrupt:
        session.end_session()
        sys.exit(-1)
