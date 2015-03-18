# -*- encoding: utf-8 -*-
import requests
import json
from pyquery import PyQuery as P

def parse(data):
    headers = {
            'user-agent': 
            "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"
            }
    try:
        res = requests.get("http://news.at.zhihu.com/api/1.2/news/before/%d"%(data), headers = headers)

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
            item = {"content": "Q: " + title + " A: " + content, "data": data, "author": author}
            result.append(json.dumps(item))
    except:
        return result

    return result

for i in parse(20150315):
    print i
