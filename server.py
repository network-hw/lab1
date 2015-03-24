import os.path
import cherrypy
import json
import random

from zhihu_parse import Zhihu
from weibo_crawler import WeiboCrawler
from jiandan import Jiandan

ACCEPTS = [ "zhihu", "weibo", "jiandan", "danhuaer"]

class Server:
    def __init__(self):
        self.danhuaer_index = 0;

    @cherrypy.expose
    def index(self):
        return cherrypy.lib.static.serve_file(os.path.join(current_dir, "demo", "index.html"));

    @cherrypy.expose
    def gimme_a_hug(self, accept=""):
        if accept != "":
            accepts = accept.split(',')
        else:
            accepts = ACCEPTS
        result = []
        if "zhihu" in accepts:
            result += zhihu.run()
        if "jiandan" in accepts:
            result += jiandan.run()
        if "danhuaer" in accepts:
            result += danhuaer_data[self.danhuaer_index:self.danhuaer_index+5]
            self.danhuaer_index += 10
        random.shuffle(result)
        if "weibo" in accepts:
            result += weibo.run()
        return json.dumps(result, ensure_ascii=False)

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {
            '/': {
                "tools.staticdir.root": os.path.abspath(os.getcwd())
                },
            '/static': {
                "tools.staticdir.on": True,
                "tools.staticdir.dir": "./demo"
                }
            }
    zhihu = Zhihu()
    weibo = WeiboCrawler()
    jiandan = Jiandan()
    danhuaer_data = eval(open("danhuaer.db", "r").read())
    cherrypy.quickstart(Server(), "/", conf)
