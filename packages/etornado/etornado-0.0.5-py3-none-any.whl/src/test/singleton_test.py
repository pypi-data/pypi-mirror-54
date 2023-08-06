import unittest
from etornado.singleton import SingletonMeta


class SingletonTest(unittest.TestCase):

    def test_singleton(self):
        class A(object, metaclass=SingletonMeta):
            pass
        a = A()
        b = A()
        self.assertTrue(a is b)
