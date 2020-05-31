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
    user = models.ForeignKey(
        UserModel,
        related_name='search_story',
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    search_query = models.CharField(
        verbose_name='Search query',
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
        return self.search_query
