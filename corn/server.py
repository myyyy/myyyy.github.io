#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import json
import logging
import threading
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
from issue_task import update_index
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor



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
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    pass
class IndexHandler(BaseHandler):
    executor = ThreadPoolExecutor(2)
    def get(self):
        tornado.ioloop.IOLoop.instance().add_callback(self.task) 
        print '1'
        self.render('index.html')

    @run_on_executor
    def task(self):
        update_index()
        time.sleep(60*10)
def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    logging.info('Serving HTTP on 0.0.0.0 port %d ...' % options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()

