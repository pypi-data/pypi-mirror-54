import unittest
from enum import Enum, unique
from etornado.error_code_manager import *


class ErrorCodeManagerTest(unittest.TestCase):

    def setUp(self):
        error_code_manager.error_infos = {}
        self.assertTrue(error_code_manager.register_error_enum(ErrorCode, ERROR_INFO_MAP))

    def test_singleton(self):
        ecm1 = ErrorCodeManager()
        ecm2 = ErrorCodeManager()
        ecm3 = error_code_manager
        self.assertIs(ecm1, ecm3)
        self.assertIs(ecm2, ecm3)

    def test_register_error_enum(self):
        self.assertDictEqual({
            0: "ok",
            100: "unknown error",
            101: "unsupported url [{url}]",
            102: "unsupported method [{method}] for url [{url}]",
        }, error_code_manager.error_infos)

        @unique
        class ErrorCode1(Enum):
            CODE0 = 1000
            CODE1 = 1001
            CODE2 = 1002

        error_info = {
            ErrorCode1.CODE0: "error code0",
            ErrorCode1.CODE1: "error code1"
        }
        self.assertTrue(error_code_manager.register_error_enum(ErrorCode1, error_info))
        self.assertDictEqual({
            0: "ok",
            100: "unknown error",
            101: "unsupported url [{url}]",
            102: "unsupported method [{method}] for url [{url}]",
            1000: "error code0",
            1001: "error code1",
            1002: "",
        }, error_code_manager.error_infos)
        @unique
        class ErrorCode2(Enum):
            CODE3 = 0
            CODE4 = 1000
            CODE5 = 2000
        self.assertFalse(error_code_manager.register_error_enum(ErrorCode2, {}))
        self.assertDictEqual({
            0: "ok",
            100: "unknown error",
            101: "unsupported url [{url}]",
            102: "unsupported method [{method}] for url [{url}]",
            1000: "error code0",
            1001: "error code1",
            1002: "",
            2000: "",
        }, error_code_manager.error_infos)

    def test_register_error_code(self):
        self.assertDictEqual({
            0: "ok",
            100: "unknown error",
            101: "unsupported url [{url}]",
            102: "unsupported method [{method}] for url [{url}]",
        }, error_code_manager.error_infos)
        self.assertFalse(error_code_manager.register_error_code(0, "conflict error"))
        self.assertDictEqual({
            0: "ok",
            100: "unknown error",
            101: "unsupported url [{url}]",
            102: "unsupported method [{method}] for url [{url}]",
        }, error_code_manager.error_infos)
        self.assertTrue(error_code_manager.register_error_code(1, "new error"))
        self.assertDictEqual({
            0: "ok",
            1: "new error",
            100: "unknown error",
            101: "unsupported url [{url}]",
            102: "unsupported method [{method}] for url [{url}]",
        }, error_code_manager.error_infos)

    def test_format_error_info(self):
        key_error = False
        try:
            error_code_manager.format_error_info(ErrorCode.UNSUPPORTED_URL)
        except KeyError as e:
            key_error = True
        self.assertTrue(key_error)
        self.assertDictEqual({
            "error_code": ErrorCode.UNKNOWN.value,
            "error_message": "unknown error"
        }, error_code_manager.format_error_info(None))
        self.assertDictEqual({
            "error_code": 0,
            "error_message": "ok"
        }, error_code_manager.format_error_info(0))
        self.assertDictEqual({
            "error_code": ErrorCode.UNSUPPORTED_URL.value,
            "error_message": "unsupported url [abc]"
        }, error_code_manager.format_error_info(ErrorCode.UNSUPPORTED_URL, url="abc"))
