import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
from concurrent.futures import ThreadPoolExecutor
from etornado.buildin_handlers.unsupported_url_handler import UnsupportedUrlHandler


class Application(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.stopping = False
        self.handlers = []
        self.thread_pool_executor = None

    def register_handler(self, url, klass, **kwargs):
        self.handlers.append((url, klass, kwargs))

    def stop(self):
        self.logger.info("call stop")
        self.stopping = True

    def run(self, port, process_count=0, thread_pool_size=0):
        self.logger.info("start service ...")
        if thread_pool_size > 0:
            self.thread_pool_executor = ThreadPoolExecutor(
                    max_workers=thread_pool_size)
        handlers = self.get_handlers()
        self.logger.info("register %d handlers[%s]", len(handlers), handlers)
        app = tornado.web.Application(handlers)
        server = tornado.httpserver.HTTPServer(app)
        server.bind(port)
        server.start(process_count)
        tornado.ioloop.PeriodicCallback(self.check_stop, 100).start()
        tornado.ioloop.IOLoop.current().start()

    def get_handlers(self):
        result = []
        for url, handler, kwargs in self.handlers:
            handler_args = {
                "thread_pool_executor": self.thread_pool_executor
            }
            for k, v in kwargs.items():
                if k in handler_args:
                    raise Exception(
                            "handler argument [%s] conflicts with buildin argument")
                handler_args[k] = v
            result.append((url, handler, handler_args))
        result.append((r".*", UnsupportedUrlHandler))
        return result

    def check_stop(self):
        if self.stopping:
            self.logger.info("stop service ...")
            if self.thread_pool_executor:
                self.thread_pool_executor.shutdown(False)
            tornado.ioloop.IOLoop.current().stop()
            self.logger.info("stop service success!!!")
