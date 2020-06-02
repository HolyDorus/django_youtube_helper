import requests
from project import settings


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

            if 'likeCount' in video['statistics']:
                video_details['like_count'] = video['statistics']['likeCount']

            if 'dislikeCount' in video['statistics']:
                video_details['dislike_count'] = video['statistics']['dislikeCount']

            if 'commentCount' in video['statistics']:
                video_details['comment_count'] = video['statistics']['commentCount']

            if 'viewCount' in video['statistics']:
                video_details['view_count'] = video['statistics']['viewCount']

            details_about_videos.append(video_details)

        return details_about_videos


class VideoManager:
    yt = YouTubeAPI(settings.YOUTUBE_API_KEY)

    def __init__(self, video_id):
        self.video_id = video_id

    def get_video_details(self):
        data = {}

        if self.video_id:
            found_video = self.yt.get_details_about_videos((self.video_id,))

            if found_video:
                data['video'] = found_video[0]
            else:
                data['error'] = 'Такое видео не найдено!'
        else:
            data['error'] = 'Не указан идентификатор видео!'

        return data
