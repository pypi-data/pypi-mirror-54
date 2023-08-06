import unittest
from etornado.application import Application
from etornado.buildin_handlers.unsupported_url_handler import UnsupportedUrlHandler


class ApplicationTest(unittest.TestCase):

    def test_get_handlers(self):
        app = Application()
        handler_args = dict(thread_pool_executor=app.thread_pool_executor)
        self.assertEqual(
                [(".*", UnsupportedUrlHandler, handler_args)],
                app.get_handlers())
        class FakeHandler:
            pass
        app.register_handler("/test", FakeHandler)
        self.assertEqual(
                [
                    ("/test", FakeHandler, handler_args),
                    (".*", UnsupportedUrlHandler, handler_args),
                ],
                app.get_handlers())
