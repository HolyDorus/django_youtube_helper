import requests


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

        details_about_videos = []

        for video in response.json()['items']:
            video_details = {
                'video_id': video['id'],
                'title': video['snippet']['title'],
                'description': video['snippet']['description'],
                'channel_title': video['snippet']['channelTitle'],
                'channel_id': video['snippet']['channelId'],
                'published_at': video['snippet']['publishedAt'],
                'preview_url': video['snippet']['thumbnails']['medium']['url'],
                'duration': video['contentDetails']['duration'],
                'view_count': video['statistics']['viewCount'],
                'like_count': video['statistics']['likeCount'],
                'dislike_count': video['statistics']['dislikeCount'],
                'comment_count': video['statistics']['commentCount']
            }

            details_about_videos.append(video_details)

        return details_about_videos
