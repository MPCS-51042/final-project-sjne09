from nltk.downloader import download
from nltk.sentiment.vader import SentimentIntensityAnalyzer

download('vader_lexicon')


def main(n: int):
    tweets = {}
    with open('data/MSFT.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            splt = line.split(':', 1)
            date = splt[0]
            tweet = splt[1]

            if date in tweets.keys():
                tweets[date].append(tweet)
            else:
                tweets[date] = [tweet]

    for day in tweets.keys():
        sum_neg = 0
        sum_neu = 0
        sum_pos = 0

        for tweet in tweets[day]:
            sid = SentimentIntensityAnalyzer()
            ss = sid.polarity_scores(tweet)
            sum_neg += ss['neg']
            sum_neu += ss['neu']
            sum_pos += ss['pos']

        avg_neg = sum_neg / n
        avg_neu = sum_neu / n
        avg_pos = sum_pos / n

        print(f'{day}: {avg_pos / avg_neg}')


if __name__ == '__main__':
    main(100)
