#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys

import tweepy


# It may be worth having api keys stored in YAML file as well (if it's worth..)
auth = tweepy.OAuthHandler('consumer_key', 'consumer_secret')
auth.set_access_token('access_token', 'access_token_secret')
api = tweepy.API(auth)


def main(argquery, arglang):
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
    if len(args) != 3:
        sys.stderr.write("Usage: python " + args[0] + " twitter_query lang_code\n")
        sys.exit()
    main(args[1], args[2])
