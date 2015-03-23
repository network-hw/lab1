# -*- encoding: utf-8 -*-
import requests
import json
import datetime
from pyquery import PyQuery as P

class Zhihu:
    def __init__(self):
        self.date = datetime.datetime.now()
        self.url = "http://news.at.zhihu.com/api/1.2/news/before/%s"

    def parse(self, date):
        headers = {
                'user-agent': 
                "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"
                }
        try:
            res = requests.get(self.url%(date), headers = headers)

            url = filter(lambda x: x['title'] == u"瞎扯 · 如何正确地吐槽", json.loads(res.content)['news'])[0]['url']
            res = requests.get(url, headers = headers)
            html = json.loads(res.content)['body']
        except:
            return []

        d = P(html)
        result = []
        try:
            for i in d('.question').items():
                now = P(i)
                title = now('.question-title').text()
                content = now('.answer .content').text()
                author = now('.answer .meta .author').text()
                if author[-1] == u"，": author = author[:-1]
                content_str = "Q: " + title + " A: " + content
                item = {"content": content_str, "date": date, "author": author, "source": "Zhihu", "logo": "zhihu.png"}
                result.append(item)
        except:
            return result

        return result

    def run(self):
        one_day_ago = datetime.timedelta(days=-1)
        result = []
        while True:
            result = result + self.parse(self.date.strftime("%Y%m%d"))
            if len(result) > 10: break
            self.date += one_day_ago

        return result

if __name__ == "__main__":
    zhihu = Zhihu()
    print zhihu.run()
