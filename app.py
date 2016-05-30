# -*- coding: utf-8 -*-
import os
import json
import time

import tornado.web
import tornado.ioloop
from tornado.options import define, options


define('port', default='8000', help='port')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class MSGHandler(tornado.web.RequestHandler):
    msg = []

    def get(self, timestamp):
        timestamp = int(timestamp)
        newer = filter(lambda x: x[0] > timestamp, MSGHandler.msg)
        newer = map(lambda x: {'timestamp': x[0], 'message': x[1]}, newer)
        self.write(json.dumps({'messages': newer}, ensure_ascii=False))

    def post(self):
        message = self.get_argument('message')
        timestamp = int(time.time() * 1000)
        MSGHandler.msg.append((timestamp, message))
        self.write('')


routers = [
    (r'/', MainHandler),
    (r'/msg', MSGHandler),
    (r'/msg/(\d+)', MSGHandler),
]


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        routers,
        debug=True,
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static')
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
