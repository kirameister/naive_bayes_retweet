# -*- coding: utf-8 -*-
import sys

import yaml

import naive_bayes_retweet


def main(data_yaml_file, tweet_true_file, tweet_false_file):
    bayes = naive_bayes_retweet.NaiveBayes(data_yaml_file)
    bayes.train(tweet_true_file, tweet_false_file)
    bayes.write_yaml(data_yaml_file)

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 4:
        sys.stderr.write( ("Usage: python " + args[0] + " DATA_YAML_file tweet_true_file  tweet_false_file\n"))
        sys.exit()
    main(args[1], args[2], args[3])

