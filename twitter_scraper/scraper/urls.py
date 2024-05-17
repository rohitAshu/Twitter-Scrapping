from django.urls import path
from . import views

urlpatterns = [
    path("twitter/api/v1/get-tweet-profile/", views.get_Tweetes_via_profile_name, name="fetch_tweets_by_hash_tag"),
]
