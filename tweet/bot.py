#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from datetime import datetime
import json
import os
import random

import twitter


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.abspath(__file__)) + '/'
    with open(dir_path + 'twitter.json', 'rU') as conf:
        config = json.load(conf)

    with open(config['tweets_file']) as f:
        data = f.read().decode('utf-8')
    tweets = filter(lambda t: t != '', data.split('\n'))

    api = twitter.Api(consumer_key=config['consumer_key'],
                      consumer_secret=config['consumer_secret'],
                      access_token_key=config['access_token_key'],
                      access_token_secret=config['access_token_secret'])
    text = "%s %s" % (tweets[random.randint(0, len(tweets) - 1)], datetime.now());
    api.PostUpdates(text)
