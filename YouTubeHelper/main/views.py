from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from . import utils


class LikedView(View):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('main:index')

        context = utils.VideoManager().get_user_liked_videos(user)
        return render(request, 'main/liked.html', context)

    def post(self, request, *args, **kwargs):
        context = utils.VideoManager().get_action_by_like_or_dislike(request)
        return JsonResponse(context)


class IndexView(View):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        return render(request, 'main/index.html')

    def post(self, request, *args, **kwargs):
        context = utils.VideoManager().find_videos(request)
        return render(request, 'main/index.html', context)


class WatchView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        context = utils.VideoManager().get_video_details(request)
        return render(request, 'main/watch.html', context)
