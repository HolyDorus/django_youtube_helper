from django.shortcuts import render, redirect
from django.http import JsonResponse

from . import models
from .youtubeapi import YouTubeAPI
from project import settings


def index(request):
    if request.method == 'POST':
        if 'search_keyword' in request.POST:
            search_keyword = request.POST['search_keyword']

            yt = YouTubeAPI(settings.YOUTUBE_API_KEY)
            found_videos = yt.find_videos(search_keyword, maxResults=10)

            context = {
                'search_keyword': search_keyword,
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
            return JsonResponse({'URA': 'gospodi'})
    elif request.method == 'GET':
        return render(request, 'main/index.html')

    if request.method == 'POST':
        print(request.POST.get('video_id'))
        return JsonResponse({'ok': 'super'})


def liked(request):
    if request.method == 'GET':
        current_user = request.user

        if not current_user.is_authenticated:
            return redirect('main:index')

        liked_videos_ids = []

        for video in current_user.liked_videos.all():
            liked_videos_ids.append(video.video_id)

        context = {}

        if liked_videos_ids:
            yt = YouTubeAPI(settings.YOUTUBE_API_KEY)
            found_videos = yt.get_details_about_videos(liked_videos_ids)
            context['liked_videos'] = found_videos

        return render(request, 'main/liked.html', context)


def watch(request):
    if request.method == 'GET':
        context = {}

        if 'v' in request.GET:
            video_id = request.GET['v']

            yt = YouTubeAPI(settings.YOUTUBE_API_KEY)
            found_video = yt.get_details_about_videos((video_id,))
            if found_video:
                context['video'] = found_video[0]
            else:
                context['error'] = 'Такое видео не найдено!'
        else:
            context['error'] = 'Не указан идентификатор видео!'

        return render(request, 'main/watch.html', context)
