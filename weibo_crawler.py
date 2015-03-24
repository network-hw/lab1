# -*- coding: utf-8 -*-

# This is the main functionality of our scrawler.
# There're _ parts:
# 1. login weibo and iterate along all the feeds
# 2. extract data out
# 3. find more feeds

import os
import sys
import re
import datetime
import shutil
import requests
from pyquery import PyQuery as pq

from weibo_login import wblogin, check_login_status, session
from weibo_feeds import weibo_fun_feeds

class WeiboFeedData:
    def __init__(self, user, text, prev, full, like, tran, comm, date):
        self.user = user
        self.text = text
        self.prev = prev
        self.full = full
        self.like = like
        self.tran = tran
        self.comm = comm
        self.date = date
    def show(self):
        result = {}
        # add weight
        result['weight'] = int(self.like) * 0.2 + int(self.tran) * 0.3 + int(self.comm) * 0.5
        result['date'] = datetime.date.today().strftime("%Y%m%d")
        result['source'] = 'weibo'
        result['content'] = self.text
        result['image-list'] = [{"image-src":'/static/image/weibo/' + self.prev.split('/')[-1]}]
        result['logo'] = 'weibo.jpg'
        return result
    def download_image(self):
        path = './demo/image/weibo/' + self.prev.split('/')[-1]
        if os.path.isfile(path) == False:
            response = requests.get(self.prev, stream=True)
            # print 'Downloading', path, '...'
            with open(path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

class WeiboCrawler:
    def __init__(self):
        self.feed_list = []
        self.user_name = "echo02200059@sina.cn"
        self.pass_word = "networklab"
        self.curr_pace = 0
        self.init      = 0
    def weibo_parser_feed(self, feed_content):
        if feed_content == None or feed_content == []:
            print "Error: Empty Parameter"
            exit(1)
        # print feed_content
        d = pq(feed_content)
        user_list = d('div.c div a.nk')
        text_list = d('div.c div span.ctt')
        prev_list = d('div.c div a img')
        full_list = d('div.c div a').filter(lambda i, this: pq(this).text() == u'原图')
        like_list = d('div.c div a').filter(lambda i, this: pq(this).text().encode('utf-8').find(u'赞'.encode('utf-8')) != -1)
        tran_list = d('div.c div a').filter(lambda i, this: pq(this).text().encode('utf-8').find(u'转发'.encode('utf-8')) != -1)
        comm_list = d('div.c div a').filter(lambda i, this: pq(this).text().encode('utf-8').find(u'评论'.encode('utf-8')) != -1)
        date_list = d('div.c div span.ct')

        re_like = re.compile(u'赞\[(.*)\]')
        re_tran = re.compile(u'转发\[(.*)\]')
        re_comm = re.compile(u'评论\[(.*)\]')
        for i in xrange(len(user_list)):
            user = user_list[i].text
            text = text_list[i].text
            prev = pq(prev_list[i]).attr['src']
            full = pq(full_list[i]).attr['href']
            like = re_like.search(like_list[i].text).group(1)
            tran = re_tran.search(tran_list[i].text).group(1)
            comm = re_comm.search(comm_list[i].text).group(1)
            date = date_list[i].text.split(' ')[0]
            feed = WeiboFeedData(user, text, prev, full, like, tran, comm, date)
            # Download file
            feed.download_image()
            self.feed_list.append(feed)
        return 0
    def weibo_init_run(self):
        for feed in weibo_fun_feeds:
            # print "Fetching ...", feed[0], feed[1]
            feed_content = session.get(feed[0]).content
            self.weibo_parser_feed(feed_content)
    def weibo_login(self):
        # print "Logging in Weibo ..."
        login_status = wblogin(self.user_name, self.pass_word)
        return check_login_status(login_status)
    def run(self):
        if self.init == 0:
            if self.weibo_login() == 1:
                print "Login failed"
                return 0
            self.weibo_init_run()
            self.init = 1
        start = self.curr_pace
        end = self.curr_pace + 10
        if start >= len(self.feed_list):
            return []
        if end >= len(self.feed_list):
            end = len(self.feed_list)
        self.curr_pace = end

        result = []
        for feed in self.feed_list[start:end]:
            result.append(feed.show())
        return result


if __name__ == '__main__':
    # if len(sys.argv[1:]) < 2:
     #   print "Usage: %s [username] [password]" % sys.argv[0]
     #   exit(1)

    crawler = WeiboCrawler()
    crawler.run()
