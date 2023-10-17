# Final Project
Name: Spencer Ellis <br>
CnetID: sjne <br>
Student number: 12411706

## Proposal
### Original Proposal

Perform sentiment analysis on stocks by using NLP on tweets and/or news articles. The output of this data can then be 
compared with analyst estimates/sentiment to identify discrepancies between professional opinions and those of the 
public, which could potentially identify short-term investment opportunities.

### Modified Proposal

My original proposal was too ambitious in scope and not well-defined, so I have modified it to fit more with the 
learning objectives of this class and add some finer detail.

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
