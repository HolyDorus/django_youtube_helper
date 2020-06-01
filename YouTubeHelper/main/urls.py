from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('liked/', views.LikedView.as_view(), name='liked'),
    path('watch/', views.WatchView.as_view(), name='watch'),
]
