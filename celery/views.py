
import tasks
from django.http import HttpResponse


def pull_pangu(request):
    tasks.pull_pangu.delay()
    return HttpResponse("call tasks.pull_pangu.delay() ok. Do not reflesh, unless you know what is going on.")
