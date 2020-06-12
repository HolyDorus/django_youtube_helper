from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from . import utils


class IndexView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(request, 'main/index.html')


class ResultsView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        context = utils.VideoManager().find_videos(request)
        return render(request, 'main/results.html', context)


class WatchView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        context = utils.VideoManager().get_video_details(request)
        return render(request, 'main/watch.html', context)


class LikedView(View):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')

        context = utils.VideoManager().get_user_liked_videos(request.user)
        return render(request, 'main/liked.html', context)

    def post(self, request, *args, **kwargs):
        context = utils.VideoManager().get_action_by_like_or_dislike(request)
        return JsonResponse(context)


def error_404(request, exception):
    return render(request, 'main/404.html')
