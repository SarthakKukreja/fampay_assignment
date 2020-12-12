from googleapiclient.discovery import build
from .models import Video

from django.db import IntegrityError
from googleapiclient.errors import HttpError
import requests , random

# Client class for communicating with YT Api
class YouTubeClient:

    # Ideally should be kept in local settings file. Keeping here for now.
    YOUTUBE_API_KEY_POOL = [ 'AIzaSyCwtv-k0gkmCGkcIXW3RGCJjdD76XUyyKc',
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

    # Function returns from API-Key pool defined above. Before returning value , functions checks if the api key
    # has not been exhausted. If it has , function selects alternate key.
    def return_valid_api_key(self, old_key=None):
        url = 'https://youtube.googleapis.com/youtube/v3/channels?part=snippet&forUsername=Google&key='
        
        # If old key ( exhausted ) is provided as argument , function checks and returns next key.
        # If no argument has been provided , function selects random key from pool.
        if old_key is None:
            api_key = random.choice(self.YOUTUBE_API_KEY_POOL)
        else:
            index = self.YOUTUBE_API_KEY_POOL.index(old_key)
            # Modulus operator so that 0 index follows nth index.
            api_key = self.YOUTUBE_API_KEY_POOL[ (index + 1) % len(self.YOUTUBE_API_KEY_POOL)]

        # If key is exhausted , try next key in pool. Otherwise return current key.
        for _ in range(0, len(self.YOUTUBE_API_KEY_POOL)):
            
            # Make GET request to check if key is exhausted. Exhausted keys return 403
            r = requests.get(url = url + api_key)

            if( r.status_code == 200 ):
                return api_key
            else:
                index = self.YOUTUBE_API_KEY_POOL.index(api_key)
                api_key = self.YOUTUBE_API_KEY_POOL[ (index + 1) % len(self.YOUTUBE_API_KEY_POOL)]

        # All keys are exhausted
        if old_key:
            return old_key
        return self.YOUTUBE_API_KEY_POOL[0]

    # Use GoogleApiClient to make fetch data from YT and store in db. 
    # publishedAfter is provided as argument to only get videos after given datetime value.
    def fetch_from_youtube(self , publishedAfter=None):    

        youtube_api_key = self.return_valid_api_key()

        youtube = build('youtube', 'v3', developerKey=youtube_api_key , cache_discovery=False)
        nextPageToken = None

        # Start infinte loop to iterate through paginated response.
        while True:
            
            request = youtube.search().list(
                part="snippet",
                q=self.SEARCH_STRING,
                # Filter out playlists and channels from response.
                type="video",
                pageToken=nextPageToken,
                maxResults=100,
                publishedAfter=publishedAfter,
                # Filter out content innappropriate for kids
                safeSearch="strict",
                # Filter out foriegn languages.
                relevanceLanguage="en"
            )

            # Capture exception caused due to api key being exhausted and select alternative key.
            try:
                response = request.execute()
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
                
            # Later pages of response sometimes tend to be empty. 
            if not response['items']:
                break
            
            # Go over next page in next iteration of loop
            if 'nextPageToken' in response:
                nextPageToken = response['nextPageToken']

            # Iterate and save items to db in current page. 
            for yt_video in response['items']:

                v = Video( title = yt_video["snippet"]["title"],
                        description = yt_video["snippet"]["description"],
                        thumbnail_url = yt_video["snippet"]["thumbnails"]["high"]["url"],
                        video_id = yt_video["id"]["videoId"],
                        date_published = yt_video["snippet"]["publishedAt"] )
                
                # Make sure same video is not accidently added twice.
                try:
                    v.save()
                except IntegrityError:
                    print("Value already exists")
            
            # Exit loop if currently on last page.
            if 'nextPageToken' not in response:
                break

