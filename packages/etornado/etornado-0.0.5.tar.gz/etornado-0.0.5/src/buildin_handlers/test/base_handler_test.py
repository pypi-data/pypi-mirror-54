import unittest
import asyncio
import types
import logging
from etornado.buildin_handlers.base_handler import BaseHandler
from etornado.error_code_manager import ErrorCode


class BaseHandlerTest(unittest.TestCase):

    def test_method_redirection(self):
        class FakeHandler(BaseHandler):
            def __init__(self):
                self.count = 0
            async def process(self, *args, **kwargs):
                self.count += 1
        loop = asyncio.get_event_loop()
        h = FakeHandler()
        self.assertEqual(0, h.count)
        loop.run_until_complete(h.head())
        self.assertEqual(1, h.count)
        loop.run_until_complete(h.get())
        self.assertEqual(2, h.count)
        loop.run_until_complete(h.post())
        self.assertEqual(3, h.count)
        loop.run_until_complete(h.delete())
        self.assertEqual(4, h.count)
        loop.run_until_complete(h.patch())
        self.assertEqual(5, h.count)
        loop.run_until_complete(h.put())
        self.assertEqual(6, h.count)
        loop.run_until_complete(h.options())
        self.assertEqual(7, h.count)

    def test_write_error(self):

        class FakeRequest(object):
            def __init__(self, method, uri):
                self.method = method
                self.uri = uri

        class FakeHandler(BaseHandler):
            def __init__(self):
                self.logger = logging.getLogger()
                self.request = FakeRequest("get", "/fake")
                self.reset()

            def write(self, data):
                self.message.append(data)

            def finish(self):
                self.finished = True

            def reset(self):
                self.finished = False
                self.message = []

        h = FakeHandler()
        h.write_error(500)
        self.assertEqual([{
            "error_code": ErrorCode.UNKNOWN.value,
            "error_message": "unknown error"
        }], h.message)
        self.assertTrue(h.finished)
        h.reset()
        h.write_error(500, ec=ErrorCode.UNSUPPORTED_URL, url="abc")
        self.assertEqual([{
            "error_code": ErrorCode.UNSUPPORTED_URL.value,
            "error_message": "unsupported url [abc]"
        }], h.message)
        self.assertTrue(h.finished)

    def test_process(self):

        class FakeRequest(object):
            def __init__(self, method, uri):
                self.method = method
                self.uri = uri

        class FakeHandler(BaseHandler):
            def __init__(self, method):
                self.logger = logging.getLogger()
                self.request = FakeRequest(method, "/fake")
                self.reset()

            def write(self, data):
                self.message.append(data)

            def send_error(self, status_code, **kwargs):
                self.write_error(status_code, **kwargs)

            def finish(self):
                self.finished = True

            def reset(self):
                self.finished = False
                self.message = []

        loop = asyncio.get_event_loop()
        h = FakeHandler("GET")
        loop.run_until_complete(h.process())
        self.assertTrue(h.finished)
        self.assertEqual([{
            "error_code": ErrorCode.UNSUPPORTED_METHOD.value,
            "error_message": "unsupported method [GET] for url [/fake]"
        }], h.message)
        h.reset()
        def sync_do_get(self):
            return 1
        h.do_get = types.MethodType(sync_do_get, h)
        loop.run_until_complete(h.process())
        self.assertTrue(h.finished)
        self.assertEqual([{
            "error_code": ErrorCode.NONE.value,
            "error_message": "ok",
            "result": 1
        }], h.message)
        h.reset()
        async def async_do_get(self):
            await asyncio.sleep(0.1)
            return {"a": 1}
        h.do_get = types.MethodType(async_do_get, h)
        loop.run_until_complete(h.process())
        self.assertTrue(h.finished)
        self.assertEqual([{
            "error_code": ErrorCode.NONE.value,
            "error_message": "ok",
            "result": {"a": 1}
        }], h.message)
        h.reset()
        def exception_do_get(self):
            raise Exception("aaa")
        h.do_get = types.MethodType(exception_do_get, h)
        loop.run_until_complete(h.process())
        self.assertTrue(h.finished)
        self.assertEqual([{
            "error_code": ErrorCode.UNKNOWN.value,
            "error_message": "unknown error",
        }], h.message)
        h.reset()
        def return_tuple_with_error_do_get(self):
            return 1000, {"a": "b"}
        h.do_get = types.MethodType(return_tuple_with_error_do_get, h)
        loop.run_until_complete(h.process())
        self.assertTrue(h.finished)
        self.assertEqual([{
            "error_code": 1000,
            "error_message": "",
        }], h.message)
        h.reset()
        def return_tuple_without_error_do_get(self):
            return ErrorCode.NONE, "abc"
        h.do_get = types.MethodType(return_tuple_without_error_do_get, h)
        loop.run_until_complete(h.process())
        self.assertTrue(h.finished)
        self.assertEqual([{
            "error_code": ErrorCode.NONE.value,
            "error_message": "ok",
            "result": "abc",
        }], h.message)

    def test__parse_result(self):
        class FakeHandler(BaseHandler):
            def __init__(self):
                self.logger = logging.getLogger()
        h = FakeHandler()
        exception = False
        try:
            h.__parse_result((1,2,3))
        except Exception as e:
            exception = True
        self.assertTrue(exception)
        exception = False
        try:
            h.__parse_result((1, "abc"))
        except Exception as e:
            exception = True
        self.assertTrue(exception)
        self.assertEqual((1, {}, {"a": "b"}),
                         h._BaseHandler__parse_result((1, {"a": "b"})))
        self.assertEqual((0, {"a": "b"}, {}),
                         h._BaseHandler__parse_result((0, {"a": "b"})))
        self.assertEqual((0, {"a": "b"}, {}),
                         h._BaseHandler__parse_result({"a": "b"}))
