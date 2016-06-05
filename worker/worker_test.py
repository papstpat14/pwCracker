import unittest
from worker_type import call_api
from worker_type import brute_force


class ApiTestCase(unittest.TestCase):
    def test_call_api(self):
        self.call_worker_type(self, "1c0b76fce779f78f51be339c49445c49", "secure", call_api)
        self.call_worker_type(self, "3fc89c714a0bdcaef4ea2fdd23a40527", "IAmTheHodor39@", call_api)

    def test_brute_force(self):
        self.call_worker_type(self, "128ecf542a35ac5270a87dc740918404", "bla", brute_force)
        self.call_worker_type(self, "187ef4436122d1cc2f40dc2b92f0eba0", "ab", brute_force)

    @staticmethod
    def call_worker_type(x, md5, pw, func):
        body = '{"md5":"' + md5 + '"}'
        obj = func(body)
        x.assertEqual(obj.success, True)
        x.assertEqual(obj.md5, md5)
        x.assertEqual(obj.pw, pw)
        x.assertEqual(obj.err, "")


if __name__ == '__main__':
    unittest.main()
