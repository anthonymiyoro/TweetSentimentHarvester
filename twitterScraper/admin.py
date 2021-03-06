from django.contrib import admin

from .models import Tweet
# Register your models here.

class TweetAdmin(admin.ModelAdmin):
    fields = ['tweet', 'tweet_id', 'date_collected', 'twitter_user', 'number_of_likes', 'number_of_retweets', 'tweet_device', 'sentiment_score']
    list_display = ('tweet', 'tweet_id', 'date_collected', 'twitter_user', 'number_of_likes', 'number_of_retweets', 'tweet_device', 'sentiment_score')
    list_filter = ('tweet_id', 'date_collected', 'number_of_likes', 'number_of_retweets', 'sentiment_score')

admin.site.register(Tweet, TweetAdmin)