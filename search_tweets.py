#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys

import tweepy
import yaml


def main(yaml_file, argquery, arglang):
    data = yaml.load(open(yaml_file).read())
    auth = tweepy.OAuthHandler(data["consumer_key"], data["consumer_secret"])
    auth.set_access_token(data["access_token"], data["access_token_secret"])
    api = tweepy.API(auth)
    statuses = api.search(argquery, lang=arglang, rpp='100')
    for status in statuses:
        status.text = re.sub(r'[\n\t]', ' ', status.text)
        status.user.screen_name = re.sub(r'[\n\r]', ' ', status.user.screen_name)
        status.user.name = re.sub(r'[\n\r]', ' ', status.user.name)
        if status.retweeted or re.search('^RT', status.text):
            # I only want the non-RTed tweets!
            continue
        # Tweet ID and its content shall be retrieved..
        print(str(status.id) + "\t" + status.text)

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 4:
        sys.stderr.write("Usage: python " + args[0] + " twitter_conf.yaml twitter_query lang_code\n")
        sys.exit()
    main(args[1], args[2], args[3])
