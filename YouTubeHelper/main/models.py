from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class LikedVideos(models.Model):
    user = models.ForeignKey(
        UserModel,
        related_name='liked_videos',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    video_id = models.CharField(
        verbose_name='ID Видео',
        max_length=50
    )
    date_time = models.DateTimeField(
        verbose_name='Дата и время',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Понравившееся видео'
        verbose_name_plural = 'Понравившиеся видео'
        ordering = ['-date_time']

    def __str__(self):
        return self.video_id


class SearchStory(models.Model):
    query = models.CharField(
        verbose_name='Запрос',
        max_length=300
    )
    date_time = models.DateTimeField(
        verbose_name='Дата и время',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Поисковый запрос'
        verbose_name_plural = 'История поиска'
        ordering = ['-date_time']

    def __str__(self):
        return self.query


class SearchCache(models.Model):
    query = models.ForeignKey(
        SearchStory,
        related_name='search_cache',
        on_delete=models.CASCADE,
        verbose_name='Запрос'
    )
    video_id = models.CharField(
        verbose_name='ID Видео',
        max_length=50
    )
    video_title = models.CharField(
        verbose_name='Название',
        max_length=300
    )
    video_short_description = models.CharField(
        verbose_name='Краткое описание',
        max_length=155
    )
    video_channel_title = models.CharField(
        verbose_name='Название канала',
        max_length=150
    )
    video_channel_id = models.CharField(
        verbose_name='ID Канала',
        max_length=50
    )
    video_preview_url = models.CharField(
        verbose_name='URL картинки',
        max_length=300
    )

    class Meta:
        verbose_name = 'Кэш поиска'
        verbose_name_plural = 'Кэш поиска'
