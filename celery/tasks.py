from celery import Celery
from celery.utils.log import get_task_logger

app = Celery()
app.config_from_object('django.conf:settings')
logger = get_task_logger(__name__)


@app.task(bind=True)
def pull_pangu(self):
    from scripts import pull_pangu
    pull_pangu.run()


@app.task(bind=True)
def backup(self):
    from scripts import backup
    backup.run()
