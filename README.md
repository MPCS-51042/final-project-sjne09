# Final Project
Name: Spencer Ellis <br>
CNetID: sjne <br>
Student number: 12411706

## Project Description

This project seeks to answer the question: are equity research analyst ratings (buy/hold/sell) a reliable predictor of 
short term equity performance? I answer this question through the analysis of ten years of research analyst ratings and 
subsequent stock price performance for S&P 500 index constituents over periods of 1 week, 1 month, and 3 months after 
an analyst report was issued. Through the use of logistic regression, I calculate the conditional probabilities of 
performance relative to the index given a particular analyst rating.

For this project, I scraped equity research analyst rating history and historical price data for all stocks within the 
S&P 500 index from yahoo finance. The analysis of the data was achieved through the use of scikit-learn's logistic 
regression model.

## To Run

The project can be run in a pipenv virtual environment.

Data files can be downloaded from: https://drive.google.com/drive/folders/1Jnf9D3L0KMJSvKGlFJ1N89DUKwhIWh7N?usp=sharing  
Data files should be stored in `./data`.

The analysis for the project is all contained in `Recommendation-Analysis.ipynb`.

To run the notebook, navigate to the project directory in a terminal window and run:
```bash
pipenv shell
pipenv run jupyter notebook
```
The project directory will open in a browser window. Navigate to the notebook to view and run.

## File Summary
`Recommendation-Analysis.ipynb` - This is a jupyter notebook containing the data analysis portion of the project. It 
                                  requires the data files available from the google drive link above.

`twitter_scraper.py` - This module defines a `TwitterScraper` class that initializes a selenium session in firefox and 
                       logs into twitter. The `scrape()` function can be called on an instance of the class in order 
                       to scrape tweets. This module is not actually used in my final analysis, but I have included it 
                       since I completed it while working on my original proposal.  
                       **NOTE: this module requires that Firefox is installed in order to run. It also requires user 
                       twitter credentials to be updated in `.env`

`sentiment_analyzer.py` - This module performs very basic sentiment analysis on tweets scraped using `TwitterScraper`.
                          It utilizes a pre-trained model (NLTK VADER) to analyze tweets for sentiment. The output 
                          is simply the ratio of positive sentiment to negative sentiment tweets by date. This is 
                          included as a proof-of-concept, but was not used in my final analysis.

`yf_scraper.py` - This module defines a `YfScraper` class that initializes a `requests` session. The various functions 
                  can be called to get data from yahoo finance. The class functions as an unofficial API for yahoo 
                  finance.


## Project Write-up

As you can see in the 'Proposal' section below, this project went through a couple of iterations of detail and 
development before I even started working on it. However, once I began work on it, it developed further as certain 
limitations exposed themselves.

I spent a lot of time trying to develop a functioning tweet scraper. The challenge with this part of the project was 
that twitter has a paid API for pulling such data, and as a result it is quite difficult to actually scrape the site 
using traditional web scraping methods. Also, Elon has a firm stance against bots on twitter, so that further led to 
challenges in scraping the site. After a lot of time analyzing the site's html to locate the elements that I needed 
to extract, it became clear that the standard python requests package wouldn't work for the site given that it is all 
populated dynamically with javascript. So I went about learning how to use selenium to automate a browser window to 
load the site, login, perform a search query, and start pulling tweets. This all worked pretty well, although was 
limited in reliability due to the poor reliability of the twitter website itself.

Once I started trying to pull a large set of tweets though, it was clear that I would have to pivot away from this 
aspect of my project. It seems there is a limit of around 300 tweets that can be loaded for a user during a particular 
period of time. As a result, it was going to take an extraordinary amount of time to pull any significant amount of 
data from the site, which made my plans for sentiment analysis infeasible. At this point, I decided to complete the 
twitter scraper to have it in working order, put together some sort of function to perform the sentiment analysis, and 
then move on to the parts of my project that I knew were possible.

The yahoo finance scraper was much simpler to put together than the twitter scraper, given that the yahoo finance API 
endpoints are publicly available (although access is not condoned by yahoo). I located the API endpoints through use of 
the inspector in my browser, searching through the html and the network tabs to try to figure out where all the data 
was being populated from. The analysis stage for both scrapers was interesting because it required a lot of 
investigative work and use of tools that I was not at all familiar with. Once I located the endpoints, the only real 
hiccup was trying to figure out how I could get the python requests module to get a cookie and crumb for access to 
certain API endpoints. 

Since I was able to locate so much interesting data from yahoo finance, I decided to build out extra functions within 
my scraper so that it could function largely as its own unofficial API - hence why there are a bunch of extra 
functions within `yf_scraper.py` that aren't actually relevant to my project.

Having had some success with pulling the data I needed from yahoo finance, I finally decided on the analysis that I 
would carry out for my project. Rather than focusing on sentiment vs. analyst recommendations as I had originally 
set out to do, I decided to just focus on analyst recommendations vs. stock performance to see if recommendations were 
a useful predictor of stock performance.

---

## Proposal
### Original Proposal

Perform sentiment analysis on stocks by using NLP on tweets and/or news articles. The output of this data can then be 
compared with analyst estimates/sentiment to identify discrepancies between professional opinions and those of the 
public, which could potentially identify short-term investment opportunities.

### Modified Proposal

My original proposal was too ambitious in scope and not well-defined, so I have modified it to fit more with the 
learning objectives of this class and add some finer detail. After feedback from the professor, I have come up with a 
modified proposal that covers the following to-do list:
- Write a scraper that pulls search results for a particular stock ticker from Twitter
- Use an existing NLP tool (such as NLTK VADER) to analyze the scraped data for sentiment
- Aggregate that data
- Scrape Analyst data and performance data
- Chart the results

---

My proposal is to create a program that can scrape tweets based on user-provided parameters including a stock ticker 
and time period. The scraper will then search twitter using the input params, parse the HTML to pull out the actual 
tweet content, and then return the data. From there, I will utilize an existing NLP tool such as NLTK vader to perform 
sentiment analysis on the returned data. What I have in mind is that the return value from this analysis will be a 
simple ratio of positive to negative (or something along those lines). The final step in data collection will be to 
pull analyst data (buy/hold/sell recommendations) and performance data for the specified stock, 
recommendations - I'm hoping to find a source where I can scrape this data or obtain it via an API call.

Once all the data has been collected and processed, I want to create an interactive data visualization to display the 
output of the analysis. If I can find historical analyst data, this would be a time-series chart to show performance vs 
public and analyst sentiment. The goal is to discover if this data can be used to find short-term investment 
opportunities, which will be (hopefully) apparent with a data visualization.

## Execution Plan

Workflows I will complete by the end of each week:

- [ ] Week 4 - Compile a list of dependencies and explore how they work and how I will use them. This will consist of 
research into requirements for each portion of my proposal:
  - First is to figure out what is required to scrape tweets from twitter/X. They have a paid API, so I imagine that 
  scraping data will require a bit of creativity and engineering (and a lot of time looking at the inspector in my web 
  browser).
  - Second is to research and understand the different NLP tools that are available for the sentiment analysis. I would 
  prefer something that doesn't exactly do all the work for me, so I am looking for a balance that allows me to learn 
  about NLP while also not being out of my depth.
  - Third is to identify a source for analyst data. One that I have in mind is OpenBB, which has an SDK. However, I'm 
  not familiar with what data they have so this will be an important step. Typically, analyst data isn't exactly the 
  most available for the public, so if I am unable to find anything for this step I will need to pivot a bit.
  - Fourth is to find a source for performance data. I can easily scrape this from yahoo finance and have in the past, 
  so that is what I will probably end up doing.
  - Fifth is to research and decide on a data visualization tool.
- [ ] Week 5-6 - Complete the scrapers that will pull data from both twitter and yahoo finance/whatever source I choose for 
historical performance data. If I can find a source for analyst data, I will build a scraper for that as well, or 
figure out how to pull the data from the OpenBB SDK if it is available. The big task here will be building the twitter 
scraper, since I expect a lot of difficulty in parsing the information and turning it into usable data.
- [ ] Week 6 - Have the sentiment analyzer built. I'm not exactly sure how much time and effort this step will require 
since I don't have familiarity with NLP, but I will need to learn how to use the tools chosen and then use the outputs 
to ensure that everything is working as it should. This step will require manual review of test inputs and outputs, 
which I foresee taking a significant amount of time.
- [ ] Week 7 - Complete the data visualization, which will require decisions on how to display the data, what data to 
actually display, and what I want to actually get out of the data that I've accumulated (which in turn will require 
careful analysis of the data itself). Since I want the visualization to be interactive as well, there will be 
additional decisions to make for that. This step will be where the results of my analysis are actually shown, and 
will indicate whether I achieved the goal of my project.
- [ ] Week 8 - Create a Jupyter Notebook to display my project and its outputs and film the YouTube video required for 
project submission.
