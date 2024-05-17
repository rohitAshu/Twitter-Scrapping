from django.urls import path
from . import views

urlpatterns = [
    path("twitter/api/v1/get-profile/", views.get_Tweeted_via_profile_name, name="get_Tweeted_via_profile_name"),
    path("twitter/api/v1/get-tweet-hashtag/", views.fetch_tweets_by_hash_tag, name="fetch_tweets_by_hash_tag"),
]
