from googleapiclient.discovery import build
from .models import Video

from django.db import IntegrityError

class YouTubeClient:
    #move to local_variables.py
    YOUTUBE_API_KEY = 'AIzaSyD-bktHaiANj-1kuP4qrdhASwZUDeXf93s'
    SEARCH_STRING = 'Playstation 5'

    def fetch_from_youtube(self):    

        youtube = build('youtube', 'v3', developerKey=self.YOUTUBE_API_KEY)
        nextPageToken = None

        while True:
        
            request = youtube.search().list(
                part="snippet",
                q=self.SEARCH_STRING,
                type="video",
                pageToken=nextPageToken,
                maxResults=100,
            )
            
            response = request.execute()
            if 'nextPageToken' in response:
                nextPageToken = response['nextPageToken']

            for yt_video in response['items']:

                v = Video( title = yt_video["snippet"]["title"],
                        description = yt_video["snippet"]["description"],
                        thumbnail_url = yt_video["snippet"]["thumbnails"]["default"]["url"],
                        video_id = yt_video["id"]["videoId"],
                        date_published = yt_video["snippet"]["publishedAt"] )
                
                try:
                    v.save()
                except IntegrityError:
                    print("Value already exists")
            
            if 'nextPageToken' not in response:
                break

