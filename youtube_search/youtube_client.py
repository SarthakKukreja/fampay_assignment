from googleapiclient.discovery import build
from .models import Video

from django.db import IntegrityError
from googleapiclient.errors import HttpError
import requests , random

import pprint

def get_full_class_name(obj):
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    return module + '.' + obj.__class__.__name__

class YouTubeClient:

    #move to local_variables.py
    YOUTUBE_API_KEY_BUCKET = [ 'AIzaSyCwtv-k0gkmCGkcIXW3RGCJjdD76XUyyKc',
                            'AIzaSyC6aUUD1-r7pufrT2B2RtINRoyTccw_5EY',
                            'AIzaSyAR_XNJ3ggANdp16avPkauhD5DUv1FRWCE',
                            'AIzaSyDyVkVtaFiaH4IoK-T1gCYm-8qJ6BRoLI4',
                            'AIzaSyC5-w6aM3R9vJZ56Rklx6eHLwIIvK7AbKA',
                            'AIzaSyDunVYmJXmhZ6vUNsedIdmABb0ZZPweci8',
                            'AIzaSyDcMo3gpQme8H9yekpbdWQjLaxbKAYZeYs',
                            'AIzaSyBhEqAvL52QqI9oLex4nctxQXsT0-XqGFk',
                            'AIzaSyBBnlC8s8u_A5vZ-uPhrsqmBlmcnEYHxMg',
                            'AIzaSyCOs9X6tME_n2eOmGYPN2onJzISWk_PFeo',
                            'AIzaSyA1Nn_WHDxtGww8WZItSuznf3VP6lu_hQ0',
                            'AIzaSyD8xr3t49Lj5xybvPiwcApEuMDgWicXbas',
                            'AIzaSyCb8YibdjHmeAD8Qg0Uv3i-9zM45Iw8HZs',]

    SEARCH_STRING = 'Playstation 5'

    def return_valid_api_key(self, old_key=None):
        url = 'https://youtube.googleapis.com/youtube/v3/channels?part=snippet&forUsername=Google&key='
        
        if old_key is None:
            api_key = random.choice(self.YOUTUBE_API_KEY_BUCKET)
        else:
            index = self.YOUTUBE_API_KEY_BUCKET.index(old_key)
            api_key = self.YOUTUBE_API_KEY_BUCKET[ (index + 1) % len(self.YOUTUBE_API_KEY_BUCKET)]

        for i in range(0, len(self.YOUTUBE_API_KEY_BUCKET)):
            
            r = requests.get(url = url + api_key)

            if( r.status_code == 200 ):
                return api_key
            else:
                index = self.YOUTUBE_API_KEY_BUCKET.index(api_key)
                api_key = self.YOUTUBE_API_KEY_BUCKET[ (index + 1) % len(self.YOUTUBE_API_KEY_BUCKET)]

        if old_key:
            return old_key
        return self.YOUTUBE_API_KEY_BUCKET[0]

    def fetch_from_youtube(self , publishedAfter=None):    

        youtube_api_key = self.return_valid_api_key()

        youtube = build('youtube', 'v3', developerKey=youtube_api_key , cache_discovery=False)
        nextPageToken = None

        while True:
            
            print(youtube_api_key)
            print(publishedAfter)

            request = youtube.search().list(
                part="snippet",
                q=self.SEARCH_STRING,
                type="video",
                pageToken=nextPageToken,
                maxResults=100,
                publishedAfter=publishedAfter,
                relevanceLanguage="en"
            )

            try:
                response = request.execute()
                #print(response)
            except HttpError:
                youtube_api_key = self.return_valid_api_key(youtube_api_key)
                youtube = build('youtube', 'v3', developerKey=youtube_api_key , cache_discovery=False)

                request = youtube.search().list(
                    part="snippet",
                    q=self.SEARCH_STRING,
                    type="video",
                    pageToken=nextPageToken,
                    maxResults=100,
                    publishedAfter=publishedAfter,
                    safeSearch="strict",
                    relevanceLanguage="en")

                response = request.execute()
                #print(response)
                
            if not response['items']:
                break

            if 'nextPageToken' in response:
                nextPageToken = response['nextPageToken']

            for yt_video in response['items']:

                print(yt_video["snippet"]["title"])

                v = Video( title = yt_video["snippet"]["title"],
                        description = yt_video["snippet"]["description"],
                        thumbnail_url = yt_video["snippet"]["thumbnails"]["high"]["url"],
                        video_id = yt_video["id"]["videoId"],
                        date_published = yt_video["snippet"]["publishedAt"] )
                
                try:
                    v.save()
                except IntegrityError:
                    print("Value already exists")
            
            if 'nextPageToken' not in response:
                break

            print("test")

