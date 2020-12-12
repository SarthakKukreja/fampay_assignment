from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import VideoSerializer

from rest_framework.pagination import PageNumberPagination
from rest_framework import generics

from rest_framework import filters

from .models import Video

# Uses Django-Rest framework to return paginated api response.
# Function based view.
@api_view(['GET'])
def video_listrequest(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    videos = Video.objects.all().order_by('-date_published')
    paginated_videos = paginator.paginate_queryset(videos,request)
    serializer = VideoSerializer(paginated_videos, many=True)
    return Response(serializer.data)

# Class based view to return api response w arguments for basic search 
class VideoAPIView(generics.ListCreateAPIView):
    search_fields = ['title' , 'description']
    filter_backends = (filters.SearchFilter,)
    queryset = Video.objects.all()
    serializer_class = VideoSerializer