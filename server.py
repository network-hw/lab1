import os.path
import cherrypy
import json

from zhihu_parse import Zhihu
from weibo_crawler import WeiboCrawler

ACCEPTS = ["zhihu", "weibo"]

class Server:
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
    cherrypy.quickstart(Server(), "/", conf)
