#!/usr/bin/python
# vim: tabstop=48 expandtab shiftwidth=4 softtabstop=4

import tweepy, sys, os
from collections import Counter
import re

if __name__ == "__main__":
    f = open("/home/ubuntu/onestorynews/onestorynews/keys.keys")
    lines = f.readlines()
    seckey = lines[0].split("#")[0]
    sectoken = lines[1].split("#")[0]
    accesstoken = lines[2].split("#")[0]
    accesssec = lines[3].split("#")[0]

    auth = tweepy.OAuthHandler(seckey, sectoken)
    auth.set_access_token(accesstoken, accesssec)

    api = tweepy.API(auth)
    words = " ".join([str(x.id_str+ " ")*x.retweet_count for x in api.home_timeline(count=100)]).split()
    tweetid = Counter(words).most_common(10)[0][0]
    urlre = re.compile("http://\S+")
    text_part = api.get_status(tweetid).text
    url_part = " ".join(urlre.findall(text_part))
    text_part = urlre.sub("",text_part)
    from_part = api.get_status(tweetid).author.screen_name
    tweet = text_part[:120-len(url_part)]+ " " + url_part + " via @" + from_part
    print tweet, "score %s" % api.get_status(tweetid).retweet_count
    if len(sys.argv) < 2 or not sys.argv[1].startswith("test"):
        api.update_status(tweet)
    else:
        candidates = Counter(words).most_common(10)
        for c in candidates:
            twid = c[0]
            text = api.get_status(twid).text
            print "Candidate with score %d: %s" % (c[1],text) 
