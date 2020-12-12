from celery import shared_task
from .youtube_client import YouTubeClient

from .models import VariableStorage

import datetime

#YT api accepts date time in RFC 3339 format
def convert_time():
    return datetime.datetime.now().isoformat("T") + "Z"

@shared_task
def updateDatabase():
    publishedAfter = None
    if( VariableStorage.objects.filter(key='publishedAfter').exists()):
        publishedAfter = VariableStorage.objects.get(key='publishedAfter')

        print(publishedAfter.value)

        y = YouTubeClient()
        y.fetch_from_youtube(publishedAfter=publishedAfter.value)

        publishedAfter.value = convert_time()
        publishedAfter.save()

    else:
        v = VariableStorage(key='publishedAfter',value=convert_time())
        v.save()

        y = YouTubeClient()
        y.fetch_from_youtube()



    





