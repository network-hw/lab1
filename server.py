import os.path
import cherrypy
import json

from zhihu_parse import Zhihu

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
    cherrypy.quickstart(Server(), "/", conf)
