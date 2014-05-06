README
======

The purpose of this set of the scripts is to:

- Retrieve a set of the tweets from Twitter, given a query and target language
- Detects the most-likely-intersting tweet based on the Naive-Bayes classifier

One still needs to create training data, which can (and should) be accomplished by manually classifying an already obtained tweets. 

This git repo contains following files: 

- data.yaml: trained data is stored. 
- naive_bayes_retweet.py: given the data.yaml and a file with list of the tweets in question, it then takes the tweets with the highest naive-bayes score and retweets that tweet on the Twitter account, accositate to the API keys in twitter_conf.yaml.
- requirements: required packages are listed. 
- search_tweets.py: Twitter search results would be returned given a query and target language. 
- train.py: based on the true and false sets of the tweets, it conducts n-gram tokenization and stores the results to data.yaml.
- twitter_conf.yaml: Twitter-API keys (needed to run the script) are stored. 

