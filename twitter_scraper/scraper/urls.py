from django.urls import path
from . import views

urlpatterns = [
    path(
        "twitter/api/v1/get-profile/",
        views.get_tweeted_via_profile_name,
        name="get_Tweeted_via_profile_name",
    ),
    path(
        "twitter/api/v1/get-tweet-hashtag/",
        views.fetch_tweets_by_hash_tag,
        name="fetch_tweets_by_hash_tag",
    ),
    path(
        "twitter/api/v1/get-trending-hashtag/",
        views.get_trending_tweets,
        name="get_trending_tweets",
    ),
    path(
        "twitter/api/v1/get-tweets-by-id/",
        views.get_tweets_by_id,
        name="get_tweets_by_id",
    ),
    path(
        "twitter/api/v1/get-comments-for-tweet/",
        views.get_comments_for_tweets,
        name="get_comments_for_tweets",
    ),
]
