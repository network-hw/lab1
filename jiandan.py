import requests
import pyquery
import json

class Jiandan:
    def __init__(self):
        self.page = 6216
        self.result = []

    def parse(self, page):
        headers = {
                'uesr-agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"
                }
        html = requests.get("http://jandan.net/pic/page-%d"%(page), headers = headers)
        _ = pyquery.PyQuery(html.content)
        for i in _("li[id^=comment] .row .text").items():
            query_obj = pyquery.PyQuery(i)
            content = query_obj("p").text()
            image_list = []
            for image in query_obj("img"):
                image_obj = pyquery.PyQuery(image)
                image_list.append({"image-src": str(image_obj.attr("src"))})
            self.result.append({"content": content, "image-list": image_list, "source": "Jiandan", "logo": "jiandan.png"})

    def run(self):
        while len(self.result) < 5:
            self.parse(self.page)
            self.page -= 1
        ret = self.result[0:5]
        self.result = self.result[5:]
        return ret

if __name__ == "__main__":
    jiandan = Jiandan()
    print jiandan.run()
