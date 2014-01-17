# -*- coding: utf-8 -*-

import datetime
from urllib2 import urlopen

start_time = datetime.datetime.now()

URLS = ['http://sebsauvage.net/',
        'http://github.com/',
        'http://sametmax.com/',
        'http://duckduckgo.com/',
        'http://0bin.net/',
        'http://bitstamp.net/']

for url in URLS:
    try:
        result = urlopen(url).read()
        print('%s page: %s bytes' % (url, len(result)))
    except Exception as e:
        print('%s generated an exception: %s' % (url, e))

elsapsed_time = datetime.datetime.now() - start_time

print("Elapsed time: %ss" % elsapsed_time.total_seconds())