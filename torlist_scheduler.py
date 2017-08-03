from datetime import timedelta

from celery import Celery
from celery.task import periodic_task

celery = Celery(__name__,
                broker="redis://localhost:6379/0",
                backend="redis://localhost:6379/0")


@periodic_task(bind=True, run_every=timedelta(seconds=10))
def update_torlist_periodically(self):
    from urllib.request import Request, urlopen
    from datetime import datetime
    import redis

    # url = "https://dan.me.uk/torlist/"
    url = "https://raw.githubusercontent.com/bashkirtsevich/autocode/master/nn_model/requirements.txt"
    nodes = urlopen(Request(url)).read().decode().split()

    r = redis.StrictRedis(host="localhost", port=6379, db=1)
    r.flushdb()
    r.set("last_list_update", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for node in nodes:
        r.set(node, 1)
