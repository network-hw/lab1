# -*- coding: utf-8 -*-

# This is the main functionality of our scrawler.
# There're _ parts:
# 1. login weibo and iterate along all the feeds
# 2. extract data out
# 3. find more feeds

#import os
import sys
import json

from weibo_login import wblogin, check_login_status
from weibo_feeds import weibo_fun_feeds


if __name__ == '__main__':
    if len(sys.argv[1:]) < 2:
        print "Usage: %s [username] [password]" % sys.argv[0]
        exit(1)
    print "Logging in Weibo ..."
    login_status = wblogin(sys.argv[1], sys.argv[2])
    if check_login_status(login_status):
        print "Login Succeed!"
    else:
        print "Login Failed"
        exit(1)


