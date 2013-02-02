#!/usr/bin/python
# vim: tabstop=48 expandtab shiftwidth=4 softtabstop=4

import tweepy, sys, os
from collections import Counter
import re
import argparse # requires 2.7

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process news tweets. Send a tweet of latest breaking news. (It's kind of magic, but not really")
    parser.add_argument("-t","--test", help="Run a test run and list top 10 candidates", action="store_true")
    parser.add_argument("-k","--keyfile",help="Twitter account consumer and accesstokens")
    parser.add_argument("-i","--ignore", help="ignore tweets containing this keywords",default="twitter" )
    args = parser.parse_args()

    api = (TweepyHelper(args.keyfile)).api

    words = " ".join([str(x.id_str+ " ")*x.retweet_count for x in api.home_timeline(count=100) if x.text.lower().find(args.ignore) == -1]).split()
    tweetid = Counter(words).most_common(10)[0][0]
    urlre = re.compile("http://\S+")
    text_part = api.get_status(tweetid).text
    url_part = " ".join(urlre.findall(text_part))
    text_part = urlre.sub("",text_part)
    from_part = api.get_status(tweetid).author.screen_name
    tweet = text_part[:120-len(url_part)]+ " " + url_part + " via @" + from_part
    print tweet, "score %s" % api.get_status(tweetid).retweet_count
    if not args.test:
        api.update_status(tweet)
    else:
        candidates = Counter(words).most_common(10)
        for c in candidates:
            twid = c[0]
            text = api.get_status(twid).text
            print "Candidate with score %d: %s" % (c[1],text) 
