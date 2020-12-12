from celery import shared_task
from .youtube_client import YouTubeClient

from .models import VariableStorage

import datetime


# YT api accepts date time in RFC 3339 format
def convert_time():
    return datetime.datetime.now().isoformat("T") + "Z"


# Keep calling YouTube API and updating database continuously in background
# periodicly and asynchronously as celery task.
@shared_task
def updateDatabase():
    publishedAfter = None

    # If data exists in db , only fetch data uploaded since last update.
    if(VariableStorage.objects.filter(key='publishedAfter').exists()):
        publishedAfter = VariableStorage.objects.get(key='publishedAfter')

        y = YouTubeClient()
        y.fetch_from_youtube(publishedAfter=publishedAfter.value)

        # Update 'last updated' time variable so that future calls need not
        # fetch already existing data.
        publishedAfter.value = convert_time()
        publishedAfter.save()

    # DB is unpopulated so fetch all data from api.
    else:
        v = VariableStorage(key='publishedAfter', value=convert_time())
        v.save()

        y = YouTubeClient()
        y.fetch_from_youtube()
