import requests
from project import settings
from . import models


class YouTubeAPI:
    SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
    VIDEOS_INFO_URL = 'https://www.googleapis.com/youtube/v3/videos'

    def __init__(self, api_key):
        self.api_key = api_key

    def find_videos(self, keyword, **kwargs):
        params = {
            'key': self.api_key,
            'part': 'snippet',
            'type': 'video',
            'maxResults': '20',
            'q': keyword
        }

        params.update(kwargs)

        response = requests.get(self.SEARCH_URL, params)

        if not response.ok:
            return []

        videos_list = []

        for video in response.json()['items']:
            video_data = {
                'video_id': video['id']['videoId'],
                'title': video['snippet']['title'],
                'description': video['snippet']['description'],
                'channel_title': video['snippet']['channelTitle'],
                'channel_id': video['snippet']['channelId'],
                'preview_url': video['snippet']['thumbnails']['medium']['url']
            }

            videos_list.append(video_data)

        return videos_list

    def get_details_about_videos(self, video_ids, **kwargs):
        params = {
            'key': self.api_key,
            'part': 'snippet,contentDetails,statistics',
            'id': ','.join(video_ids)
        }

        params.update(kwargs)

        response = requests.get(self.VIDEOS_INFO_URL, params)

        if not response.ok:
            return []

        def get_short_description(description):
            if len(description) <= 150:
                return description

            return ' '.join(description[:150].split()[:-1]) + '...'

        details_about_videos = []

        for video in response.json()['items']:
            short_description = get_short_description(
                video['snippet']['description']
            )

            video_details = {
                'video_id': video['id'],
                'title': video['snippet']['title'],
                'short_description': short_description,
                'description': video['snippet']['description'],
                'channel_title': video['snippet']['channelTitle'],
                'channel_id': video['snippet']['channelId'],
                'published_at': video['snippet']['publishedAt'],
                'preview_url': video['snippet']['thumbnails']['medium']['url'],
                'duration': video['contentDetails']['duration']
            }

            likes = video['statistics'].get('likeCount')
            if likes is not None:
                video_details['like_count'] = likes

            dislikes = video['statistics'].get('dislikeCount')
            if dislikes is not None:
                video_details['dislike_count'] = dislikes

            views = video['statistics'].get('viewCount')
            if views is not None:
                video_details['view_count'] = views

            comments = video['statistics'].get('commentCount')
            if comments is not None:
                video_details['comment_count'] = comments

            details_about_videos.append(video_details)

        return details_about_videos


class VideoManager:
    yt = YouTubeAPI(settings.YOUTUBE_API_KEY)

    def get_video_details(self, request):
        video_id = request.GET.get('v')
        data = {}

        if not video_id:
            data['error'] = 'Не указан идентификатор видео!'
            return data

        found_video = self.yt.get_details_about_videos((video_id,))

        if found_video:
            data['video'] = found_video[0]
        else:
            data['error'] = 'Такое видео не найдено!'

        return data

    def find_videos(self, request):
        search_keyword = request.POST.get('search_keyword')
        data = {}

        if not search_keyword:
            return data

        found_videos = self.yt.find_videos(search_keyword)

        if request.user.is_authenticated:
            self.update_search_history(request.user, search_keyword)
            self.update_liked_video_data(request.user, found_videos)

        data = {
            'search_keyword': search_keyword,
            'found_videos': found_videos
        }

        return data

    def update_search_history(self, user, search_keyword):
        new_search_query = models.SearchStory(
            user=user,
            search_query=search_keyword
        )
        new_search_query.save()

    def update_liked_video_data(self, user, found_videos):
        for video in found_videos:
            liked_video = user.liked_videos.filter(
                video_id=video['video_id']
            )

            if liked_video.exists():
                video['liked_by_user'] = True
            else:
                video['liked_by_user'] = False
