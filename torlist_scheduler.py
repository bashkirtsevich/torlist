from datetime import timedelta

from celery import Celery
from celery.task import periodic_task

celery = Celery(__name__,
                broker="redis://localhost:6379/0",
                backend="redis://localhost:6379/0")


@periodic_task(bind=True, max_retries=3, run_every=timedelta(hours=1))
def update_torlist_periodically(self):
    from urllib.request import Request, urlopen
    from datetime import datetime
    import redis

    url = "https://dan.me.uk/torlist/"
    nodes = urlopen(Request(url)).read().decode().split()

    redis_store = redis.StrictRedis(host="localhost", port=6379, db=1)
    redis_store.flushdb()
    redis_store.set("last_list_update", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for node in nodes:
        redis_store.set(node, 1)


update_torlist_periodically.apply_async()
