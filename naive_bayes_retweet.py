# -*- coding: utf-8 -*-
import csv
import math
import operator
import re
import sys

import tweepy
import yaml


class NaiveBayes(object):
    def __init__(self, yaml_file):
        # open YAML file
        self.data = yaml.load(open(yaml_file).read())

    def train(self, true_file, false_file):
        self.data["true_category_count"] = 0
        self.data["false_category_count"] = 0
        self.data["true_category_word_count"] = 0
        self.data["false_category_word_count"] = 0
        self.data["true_words"] = {}
        self.data["false_words"] = {}

        with open(true_file, "r") as true_data:
            reader = csv.reader(true_data, delimiter='\t', skipinitialspace=True)
            for row in reader:
                # ID TWEET
                tweet_id, line = row
                # This is to accept only the ASCII and ja-JP chars..
                line = re.sub(u'[^\U00000030-\U0000007F\U00003000-\U0001F000]', '', segments[1].decode("utf-8"))
                # This is to surppress white space in the message (for the training purpose)
                line = re.sub(' ', '', line)
                tokens = list(line)
                # Following is the actual training part..
                self.data["true_category_count"] += 1
                for token in tokens:
                    self.data["true_category_word_count"] += 1
                    try:
                        self.data["true_words"][token] += 1
                    except KeyError:
                        self.data["true_words"][token] = 1

        with open(false_file, "r") as false_data:
            reader = csv.reader(false_data, delimiter='\t', skipinitialspace=True)
            for row in reader:
                # ID TWEET
                tweet_id, line = row
                line = re.sub(u'[^\U00000030-\U0000007F\U00003000-\U0001F000]', '', segments[1].decode("utf-8"))
                line = re.sub(' ', '', line)
                tokens = list(line)
                self.data["false_category_count"] += 1
                for token in tokens:
                    self.data["false_category_word_count"] += 1
                    try:
                        self.data["false_words"][token] += 1
                    except KeyError:
                        self.data["false_words"][token] = 1

    def predicted_score(self, tweet_in_question):
        # In order to predict only the likelihood score, you don't need false category. I'm including this just for fun..
        tweet_in_question = re.sub('[\r\n]', '', tweet_in_question)
        tweet_in_question = re.sub(u'[^\U00000030-\U0000007F\U00003000-\U0001F000]', '', tweet_in_question.decode("utf-8"))
        tweet_in_question = re.sub(' ', '', tweet_in_question)
        tokens = list(tweet_in_question)
        all_category_count = self.data["false_category_count"] + self.data["true_category_count"]
        score_true = math.log(float(self.data["true_category_count"]) / float(all_category_count))    # P(category_true)
        score_false = math.log(float(self.data["false_category_count"]) / float(all_category_count))  # P(category_false)
        for token in tokens:
            try:
                score_true += math.log(float(self.data["true_words"][token]) / float(self.data["true_category_word_count"]))
            except KeyError:
                pass
            try:
                score_false += math.log(float(self.data["false_words"][token]) / float(self.data["false_category_word_count"]))
            except KeyError:
                pass
        return score_true

    def write_yaml(self, yaml_file):
        stream = file(yaml_file, 'w')
        yaml.dump(self.data, stream, encoding=("utf-8"), allow_unicode=True)


def main(data_yaml_file, twitter_yaml_file, tweet_file, tweeted_file):
    # Following lines are to read Twitter-API access keys from YAML file. 
    # This is only a temporary solution; it shall eventually be handled by
    # an independent class. 
    yaml_data = yaml.load(open(twitter_yaml_file).read())
    auth = tweepy.OAuthHandler(yaml_data["consumer_key"], yaml_data["consumer_secret"])
    auth.set_access_token(yaml_data["access_token"], yaml_data["access_token_secret"])
    api = tweepy.API(auth)

    bayes = NaiveBayes(data_yaml_file)
    # Following lines should be used only for (re-)training the model and store it to YAML file
    # bayes.train("tweets_data/violin.true", "tweets_data/violin.false")
    # bayes.write_yaml(yaml_file)

    tweeted_set = {}
    with open(tweeted_file, "r") as tweeted_data:
        for retweeted_status in tweeted_data:
            retweeted_status  = re.sub('[\r\n]', '', retweeted_status)
            tweeted_set[retweeted_status] = 1

    tweet_list = []
    with open(tweet_file, "r") as tweet_data:
        reader = csv.reader(tweet_data, delimiter='\t', skipinitialspace=True)
        for row in reader:
            tweet_id, tweet = row
            tweet_list.append([bayes.predicted_score(tweet), tweet_id, tweet])
        tweet_list.sort(key=operator.itemgetter(0), reverse=True)

    for id_tweet_to_be_retweeted in tweet_list:
        id_tweet_to_be_retweeted[2] = re.sub('[\r\n]', '', id_tweet_to_be_retweeted [2])
        if (id_tweet_to_be_retweeted[2] in tweeted_set):
            # This tweet has already been RTed, so should be skipped
            continue
        # Write the retweeted value to the file and retweet
        with open(tweeted_file, 'a') as tweeted_data:
            tweeted_data.write(id_tweet_to_be_retweeted[2])
            tweeted_data.write('\n')
        api.retweet(id_tweet_to_be_retweeted[1])
        print("RTed: " + id_tweet_to_be_retweeted[1] + " " + id_tweet_to_be_retweeted[2])
        break


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 5:
        sys.stderr.write("Usage: python " + args[0] + " DATA_YAML_file Twitter_YAML_file Tweet_file Tweeted_file\n")
        sys.exit()

    main(args[1], args[2], args[3], args[4])
