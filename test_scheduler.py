import unittest
from  torlist_scheduler import celery, update_torlist_periodically
import redis


class TestCase(unittest.TestCase):
    def test_task(self):
        r = redis.StrictRedis(host="localhost", port=6379, db=1)
        r.flushdb()

        update_torlist_periodically.apply().get()

        self.assertTrue(r.exists("last_list_update"), "Missed 'last_list_update' key in redis")
        self.assertTrue(r.keys() > 1, "Looks like nodes is missing")


if __name__ == '__main__':
    unittest.main()
