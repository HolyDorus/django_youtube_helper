from django.contrib import admin
from . import models


class AdminLikedVideos(admin.ModelAdmin):
    list_display = ('user', 'video_id', 'date_time')
    list_display_links = ('video_id',)
    search_fields = ('video_id',)
    ordering = ('-date_time',)


class AdminSearchStory(admin.ModelAdmin):
    list_display = ('user', 'search_query', 'date_time')
    list_display_links = ('search_query',)
    search_fields = ('search_query',)
    ordering = ('-date_time',)
    search_fields = ('search_query',)


admin.site.register(models.LikedVideos, AdminLikedVideos)
admin.site.register(models.SearchStory, AdminSearchStory)
