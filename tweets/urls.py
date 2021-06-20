from django.urls import path
from .import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('tweets', views.tweet_list_view),
    path('create', views.tweet_create_view),
    path('tweets/action', views.tweet_action_view),
    path('delete/<int:tweet_id>', views.tweet_delete_view),
    path('tweetdetail/<int:tweet_id>', views.tweet_detail_view)
]