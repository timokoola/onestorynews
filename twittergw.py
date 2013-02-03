#!/usr/bin/python
#
#   Copyright 2013 Moarub Oy
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
#
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import tweepy, sys, os
from collections import Counter
import re
import argparse # requires 2.7


def ignoreTweet(x):
    return x.text.lower().find(args.ignore) == -1

class TweepyHelper:
    def __init__(self,keyfile):
        f = open(keyfile)
        lines = f.readlines()
        f.close()
        consumerkey = lines[0].split("#")[0]
        consumersecret = lines[1].split("#")[0]
        accesstoken = lines[2].split("#")[0]
        accesssec = lines[3].split("#")[0]

        auth = tweepy.OAuthHandler(consumerkey, consumersecret)
        auth.set_access_token(accesstoken, accesssec)
        self.api = tweepy.API(auth)


def generate_tweet(tid,signature=""):
    urlre = re.compile("http://\S+")
    text_part = api.get_status(tid).text
    url_part = " ".join(urlre.findall(text_part))
    text_part = urlre.sub("", text_part)
    from_part = api.get_status(tid).author.screen_name
    tweet = text_part[:120 - len(url_part)] + " " + url_part + " via @" + from_part + " " + signature
    return tweet

def candidate_ids(api):
    return " ".join([str(x.id_str+ " ")*x.retweet_count for x in api.home_timeline(count=100) if ignoreTweet(x)]).split()

def pick_tweet(api):
    return Counter(candidate_ids(api)).most_common(10)[0][0]

def handle_command_line():
    parser = argparse.ArgumentParser(description="Process news tweets. Send a tweet of latest breaking news. (It's kind of magic, but not really)")
    parser.add_argument("-t", "--test", help="Run a test run and list top 10 candidates", action="store_true")
    parser.add_argument("-k", "--keyfile", help="Twitter account consumer and accesstokens")
    parser.add_argument("-i", "--ignore", help="ignore tweets containing this keywords", default="twitter")
    parser.add_argument("-s", "--signature", help="Sign Tweet with a ^name", default="")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = handle_command_line()

    api = (TweepyHelper(args.keyfile)).api

    tweetid = pick_tweet(api)

    tweet = generate_tweet(tweetid,args.signature)
    print tweet, "score %s" % api.get_status(tweetid).retweet_count
    if not args.test:
        api.update_status(tweet)
    else:
        candidates = Counter(candidate_ids(api)).most_common(10)
        for c in candidates:
            twid = c[0]
            text = api.get_status(twid).text
            username = api.get_status(twid).author.screen_name
            print "Candidate from %s with score %d: %s" % (username,c[1],text)
