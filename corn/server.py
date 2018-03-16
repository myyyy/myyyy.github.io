#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import json
import logging
import threading
import tornado.ioloop
import tornado.web
from pymongo import MongoClient


import tornado.options
from tornado.options import define, options
from issue_task import update_index

define("port", default=8999, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"\/*.*", IndexHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), ""),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    pass
class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html')

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.PeriodicCallback(update_index, 60*10).start()
    logging.info('Serving HTTP on 0.0.0.0 port %d ...' % options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()

