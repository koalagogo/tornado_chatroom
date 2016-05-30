# -*- coding: utf-8 -*-
import os

import tornado.web
import tornado.websocket
import tornado.ioloop
from tornado.options import define, options


define('port', default='8000', help='port')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class WSHandler(tornado.websocket.WebSocketHandler):
    people = set()

    def _broadcast_msg(self, msg, exclude_self=True):
        for person in WSHandler.people:
            if not (exclude_self and person == self):
                person.write_message(msg)

    def open(self):
        WSHandler.people.add(self)
        self._broadcast_msg('someone has join the chat')

    def on_message(self, msg):
        self._broadcast_msg(msg)

    def on_close(self):
        WSHandler.people.remove(self)
        self._broadcast_msg('someone has left the chat')


routers = [
    (r'/', MainHandler),
    (r'/ws', WSHandler),
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
