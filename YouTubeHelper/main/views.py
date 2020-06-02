from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from . import models
from . import utils
from project import settings
import json


class IndexView(View):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        return render(request, 'main/index.html')

    def post(self, request, *args, **kwargs):
        search_keyword = request.POST.get('search_keyword')

        if search_keyword:
            yt = utils.YouTubeAPI(settings.YOUTUBE_API_KEY)
            found_videos = yt.find_videos(search_keyword, maxResults=10)

            current_user = request.user
            if current_user and current_user.is_authenticated:
                new_search_query = models.SearchStory(
                    user=current_user,
                    search_query=search_keyword
                )
                new_search_query.save()

                for video in found_videos:
                    tmp = current_user.liked_videos.filter(
                        video_id=video['video_id']
                    )

                    if tmp.exists():
                        video['liked_by_user'] = 'yes'
                    else:
                        video['liked_by_user'] = 'no'

            context = {
                'search_keyword': search_keyword,
                'found_videos': found_videos
            }

            return render(request, 'main/index.html', context)
        else:
            return redirect('main:index')


class LikedView(View):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        current_user = request.user

        if not current_user or not current_user.is_authenticated:
            return redirect('main:index')

        liked_videos_ids = []

        for video in current_user.liked_videos.all():
            liked_videos_ids.append(video.video_id)

        context = {}

        if liked_videos_ids:
            yt = utils.YouTubeAPI(settings.YOUTUBE_API_KEY)
            found_videos = yt.get_details_about_videos(liked_videos_ids)
            context['liked_videos'] = found_videos

        return render(request, 'main/liked.html', context)

    def post(self, request, *args, **kwargs):
        response = json.loads(request.body.decode())
        video_id = response.get('video_id')

        if video_id:
            current_user = request.user

            if not current_user or not current_user.is_authenticated:
                return JsonResponse({'error': 'user is not authenticated'})

            video = current_user.liked_videos.filter(video_id=video_id)

            if video.exists():
                video[0].delete()
                return JsonResponse({'video_status': 'removed'})
            else:
                new_video = models.LikedVideos(
                    user=current_user,
                    video_id=video_id
                )
                new_video.save()
                return JsonResponse({'video_status': 'added'})


class WatchView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        video_id = request.GET.get('v')

        context = utils.VideoManager(video_id).get_video_details()

        return render(request, 'main/watch.html', context)
