#!/usr/bin/env python
# *-* encoding: utf-8 *-*
#
# =============================================
#      Author   : Andy Scout
#    Homepage   : http://andyhuzhill.github.io
#    E-mail     : andyhuzhill@gmail.com
#
#  Description  :
#  Revision     :
#
# =============================================


import tornado.web
import tornado.ioloop

from doubanfm import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        playlist = getPlayList("0", None)
        if playlist["song"] == []:
            self.render("index.html", err_msg = u"无法获取歌曲列表")
        else:
            self.render("index.html", err_msg = None, songs = playlist["song"])

class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")

class ContactHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("contact.html")

class SigninHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("signin.html")

    def post(self):
        self.write(self.get_argument("password"))

app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/about", AboutHandler),
    (r"/contact", ContactHandler),
    (r"/signin", SigninHandler),
    ],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug = True
    )

if __name__ == "__main__":
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
