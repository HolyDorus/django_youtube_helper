from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class LikedVideos(models.Model):
    user = models.ForeignKey(
        UserModel,
        related_name='liked_videos',
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    video_id = models.CharField(
        verbose_name='Video ID',
        max_length=50
    )
    date_time = models.DateTimeField(
        verbose_name='Date and time',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Liked video'
        verbose_name_plural = 'Liked videos'
        ordering = ['-date_time']

    def __str__(self):
        return self.video_id


class SearchStory(models.Model):
    query = models.CharField(
        verbose_name='Query',
        max_length=300
    )
    date_time = models.DateTimeField(
        verbose_name='Date and time',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Search query'
        verbose_name_plural = 'Search story'
        ordering = ['-date_time']

    def __str__(self):
        return self.query


class SearchCache(models.Model):
    query = models.ForeignKey(
        SearchStory,
        related_name='search_cache',
        on_delete=models.CASCADE,
        verbose_name='Query'
    )
    video_id = models.CharField(
        verbose_name='Video ID',
        max_length=50
    )
    video_title = models.CharField(
        verbose_name='Title',
        max_length=300
    )
    video_short_description = models.CharField(
        verbose_name='Short Description',
        max_length=155
    )
    video_channel_title = models.CharField(
        verbose_name='Channel Title',
        max_length=150
    )
    video_channel_id = models.CharField(
        verbose_name='Channel ID',
        max_length=50
    )
    video_preview_url = models.CharField(
        verbose_name='Preview URL',
        max_length=300
    )
