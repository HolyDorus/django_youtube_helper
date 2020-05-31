from django.shortcuts import render
from random import randint
from django.http import JsonResponse

from .youtubeapi import YouTubeAPI
from project import settings
from . import models


def index(request):

    if request.method == 'GET':
        context = {
            'r': randint(0, 255),
            'g': randint(0, 255),
            'b': randint(0, 255)
        }
        return render(request, 'main/index.html', context)
    elif request.method == 'POST':
        if 'keyword' in request.POST:
            keyword = request.POST['keyword']

            yt = YouTubeAPI(settings.YOUTUBE_API_KEY)
            found_videos = yt.find_videos(keyword, maxResults=5)

            context = {
                'r': 0,
                'g': 0,
                'b': 0,
                'found_videos': found_videos
            }

            return render(request, 'main/index.html', context)
        if 'video_id' in request.POST:
            return JsonResponse({'ok': 'super'})

    return render(request, 'main/index.html')


def liked(request):
    if request.method == 'GET':
        yt = YouTubeAPI(settings.YOUTUBE_API_KEY)

        # liked_videos_ids = request.user.liked_videos.# %%
        # models.LikedVideos.objects.
        found_videos = yt.get_details_about_videos(('BL_nFPi8ib0', '1yDkh9_eaDQ', 'DDHFvbxh3Go', 'eHpuISRUdbs'))

        context = {
            'liked_videos': found_videos
        }

        return render(request, 'main/liked.html', context)
