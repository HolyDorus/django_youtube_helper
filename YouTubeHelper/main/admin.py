from django.contrib import admin

from . import models


class AdminLikedVideos(admin.ModelAdmin):
    list_display = ('user', 'video_id', 'date_time')
    list_display_links = ('video_id',)
    search_fields = ('video_id',)
    ordering = ('-date_time',)


class AdminSearchStory(admin.ModelAdmin):
    list_display = ('query', 'date_time')
    list_display_links = ('query',)
    search_fields = ('query',)
    ordering = ('-date_time',)
    search_fields = ('query',)


class AdminSearchCache(admin.ModelAdmin):
    list_display = (
        'query', 'video_title',
        'video_short_description', 'video_channel_title'
    )
    list_display_links = ('query',)
    search_fields = ('query',)
    ordering = ('query', 'video_title')
    search_fields = ('query',)


admin.site.register(models.LikedVideos, AdminLikedVideos)
admin.site.register(models.SearchStory, AdminSearchStory)
admin.site.register(models.SearchCache, AdminSearchCache)
