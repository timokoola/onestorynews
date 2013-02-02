onestorynews
============

Scripts for OneStoryNews

Usage
-----

usage: twittergw.py [-h] [-t] [-k KEYFILE] [-i IGNORE]

Process news tweets. Send a tweet of latest breaking news. (It's kind of
magic, but not really

optional arguments:
  -h, --help            show this help message and exit
  -t, --test            Run a test run and list top 10 candidates
  -k KEYFILE, --keyfile KEYFILE
                        Twitter account consumer and accesstokens
  -i IGNORE, --ignore IGNORE
                        ignore tweets containing this keywords

Example crontab line:
38 * * * * /home/user/onestorynews/twittergw.py --keyfile /home/user/onestorynews/keys.keys 





