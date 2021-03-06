import json

from django.utils import dateformat

import requests
from isodate import parse_duration, parse_datetime

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
                'title': self._replace_special_expressions(
                    video['snippet']['title']
                ),
                'short_description': self._replace_special_expressions(
                    video['snippet']['description']
                ),
                'channel_title': self._replace_special_expressions(
                    video['snippet']['channelTitle']
                ),
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

        details_about_videos = []

        for video in response.json()['items']:
            short_description = self._get_short_description(
                self._replace_special_expressions(
                    video['snippet']['description']
                )
            )

            video_details = {
                'video_id': video['id'],
                'title': self._replace_special_expressions(
                    video['snippet']['title']
                ),
                'short_description': short_description,
                'description': self._replace_special_expressions(
                    video['snippet']['description']
                ),
                'channel_title': self._replace_special_expressions(
                    video['snippet']['channelTitle']
                ),
                'channel_id': video['snippet']['channelId'],
                'published_at': self._get_pretty_published_date(
                    video['snippet']['publishedAt']
                ),
                'preview_url': video['snippet']['thumbnails']['medium']['url'],
                'duration': self._get_pretty_duration(
                    video['contentDetails']['duration']
                )
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

    def _get_pretty_published_date(self, datetime_string):
        dt = parse_datetime(datetime_string)
        return dateformat.format(dt, 'd E Y г.')

    def _get_pretty_duration(self, duration):
        parsed = parse_duration(duration)
        sec = parsed.seconds
        time = str(parsed)

        if sec / 60 / 60 < 1:
            time = time[2:]

            if sec / 60 < 10:
                time = time[1:]

        return time

    def _get_short_description(self, description):
        max_description_len = 150
        if len(description) <= max_description_len:
            return description

        return ' '.join(description[:max_description_len].split()[:-1]) + '...'

    def _replace_special_expressions(self, text):
        expressions = {
            '&quot;': '"',
            '&nbsp;': ' ',
            '&#39;': '\'',
            '&gt;': '>',
            '&lt': '<',
            '&amp;': '&',
            '&apos;': '\'',
            '&cent;': '¢',
            '&pound;': '£',
            '&yen;': '¥',
            '&euro;': '€',
            '&copy;': '©',
            '&reg;': '®'
        }

        for k, v in expressions.items():
            text = text.replace(k, v)

        return text


class VideoManager:
    yt = YouTubeAPI(settings.YOUTUBE_API_KEY)

    def get_video_details(self, request):
        video_id = request.GET.get('v')

        if not video_id:
            return {'error': 'Не указан идентификатор видео!'}

        found_video = self.yt.get_details_about_videos((video_id,))

        if found_video:
            found_video[0]['liked_by_user'] = self._is_video_liked_by_user(
                request.user,
                found_video[0]['video_id']
            )

            return {'video': found_video[0]}
        else:
            return {'error': 'Такое видео не найдено!'}

    def find_videos(self, request):
        search_query = request.GET.get('q')

        if not search_query:
            return {}

        if settings.SEARCH_RESULTS_CACHE:
            videos = self._get_videos_from_cache(request.user, search_query)
        else:
            videos = self._get_videos(request.user, search_query)

        data = {
            'q': search_query,
            'videos': videos
        }

        return data

    def get_user_liked_videos(self, user):
        liked_videos_ids = user.liked_videos.values_list('video_id', flat=True)

        if liked_videos_ids:
            found_videos = self.yt.get_details_about_videos(liked_videos_ids)
            return {'liked_videos': found_videos}

        return {}

    def get_action_by_like_or_dislike(self, request):
        response_data = json.loads(request.body.decode())
        video_id = response_data.get('video_id')

        if video_id:
            user = request.user

            if not user.is_authenticated:
                return {'error': 'Необходимо войти в аккаунт!'}

            video = user.liked_videos.filter(video_id=video_id)

            if video.exists():
                video.last().delete()
                return {'video_status': 'removed'}
            else:
                new_video = models.LikedVideos(
                    user=user,
                    video_id=video_id
                )
                new_video.save()
                return {'video_status': 'added'}
        else:
            return {'error': f'Видео \'{video_id}\' не найдено!'}

    def _get_videos(self, user, search_query):
        videos = self.yt.find_videos(search_query)

        if user.is_authenticated:
            self._update_liked_video_data(user, videos)

        return videos

    def _get_videos_from_cache(self, user, search_query):
        videos = []
        query = models.SearchStory.objects.filter(query=search_query)

        if query.exists():
            found_cache = query.last().search_cache.all()

            for cache in found_cache:
                video_data = {
                    'video_id': cache.video_id,
                    'title': cache.video_title,
                    'short_description': cache.video_short_description,
                    'channel_title': cache.video_channel_title,
                    'channel_id': cache.video_channel_id,
                    'preview_url': cache.video_preview_url
                }
                videos.append(video_data)
        else:
            videos = self.yt.find_videos(search_query)
            self._add_videos_to_cache(search_query, videos)

        if user.is_authenticated:
            self._update_liked_video_data(user, videos)

        return videos

    def _add_videos_to_cache(self, search_query, videos):
        new_query_in_history = models.SearchStory(query=search_query)
        new_query_in_history.save()

        for video in videos:
            new_seqrch_cache = models.SearchCache(
                query=new_query_in_history,
                video_id=video['video_id'],
                video_title=video['title'],
                video_short_description=video['short_description'],
                video_channel_title=video['channel_title'],
                video_channel_id=video['channel_id'],
                video_preview_url=video['preview_url']
            )
            new_seqrch_cache.save()

    def _update_liked_video_data(self, user, found_videos):
        for video in found_videos:
            video['liked_by_user'] = self._is_video_liked_by_user(
                user,
                video['video_id']
            )

    def _is_video_liked_by_user(self, user, video_id):
        if not user.is_authenticated:
            return False

        video = user.liked_videos.filter(
            video_id=video_id
        )

        return video.exists()
