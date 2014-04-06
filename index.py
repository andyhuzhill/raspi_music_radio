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
import time

from doubanfm import *

i = 1

g_opener = None

playlist = getPlayList("1", g_opener) 

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        global playlist
        global g_opener
        global i
        if playlist['song'] == []:
            self.render("msg.html", msg = u"无法获取歌曲列表!")
        else:
            if i > getListLength(playlist['song']):
                playlist = getPlayList("1", g_opener)
                i = 1
            success, song, child = playSongOfList(playlist, i)
            if success:
                self.render("index.html", songs=playlist['song'], imgsrc = song['picture'], songtitle=song['title'], singer=song['artist']) 

    def post(self):
        global i
        global playlist
        global g_opener
        i += 1
        if i >  getListLength(playlist['song']):
            playlist = getPlayList("1", g_opener)
            i = 1
        success, song, child = playSongOfList(playlist, i)
        self.render("index.html", songs=playlist['song'], imgsrc= song['picture'], songtitle=song['title'], singer=song['artist']) 


class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")

class ContactHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("contact.html")

class SigninHandler(tornado.web.RequestHandler):
    verifycode_id = ""
    def get(self):
        global verifycode_id
        verifycode_id = getVerifyCode()
        print verifycode_id
        self.render("signin.html")

    def post(self):
        global verifycode_id
        global g_opener
        user = self.get_argument("user")
        passwd = self.get_argument("passwd")
        verifycode = self.get_argument("verifycode")
        success, g_opener = SignIn(user, passwd, verifycode_id, verifycode)
        if success:
            self.render("msg.html", msg = u"登陆成功！")
            time.sleep(1)
            self.redirect("/")
        else:
            self.render("msg.html", msg = u"登陆失败！")
            time.sleep(1)
            self.redirect("/")

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
