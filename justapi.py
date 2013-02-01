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
