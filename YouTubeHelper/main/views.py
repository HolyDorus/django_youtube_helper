from django.shortcuts import render
from random import randint
from django.http import JsonResponse
from django.shortcuts import redirect

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
        if 'search_keyword' in request.POST:
            search_keyword = request.POST['search_keyword']

            yt = YouTubeAPI(settings.YOUTUBE_API_KEY)
            found_videos = yt.find_videos(search_keyword, maxResults=10)

            context = {
                'r': 0,
                'g': 0,
                'b': 0,
                'found_videos': found_videos
            }

            current_user = request.user
            if current_user.is_authenticated:
                new_search_query = models.SearchStory(
                    user=current_user,
                    search_query=search_keyword
                )
                new_search_query.save()

            return render(request, 'main/index.html', context)
        if 'video_id' in request.POST:
            return JsonResponse({'ok': 'super'})

    return render(request, 'main/index.html')


def liked(request):
    if request.method == 'GET':
        current_user = request.user

        if not current_user.is_authenticated:
            return redirect('main:index')

        liked_videos_ids = []

        for video in current_user.liked_videos.all():
            liked_videos_ids.append(video.video_id)

        yt = YouTubeAPI(settings.YOUTUBE_API_KEY)
        found_videos = yt.get_details_about_videos(liked_videos_ids)

        context = {
            'liked_videos': found_videos
        }

        return render(request, 'main/liked.html', context)
