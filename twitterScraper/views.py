# Django Imports
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Rest Framework Imports
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status

#Custom App Imports
from twitterScraper.models import Tweet
from twitterScraper.serializers import TweetSerializer, TwitterAnalyserSerializer

# File imports
from .twitter_streamer import TweetAnalyzer
tweetanalyzer = TweetAnalyzer()



########################## This view returns a JSON object with all the tweets collected so far ###############################
@csrf_exempt
def tweet_list(request):
    """
    List all tweets, or create a new tweet.
    """
    if request.method == 'GET':
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TweetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)




######################## This view searches for twitter mentions from the provided tweeter username #####################
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def analyse_tweet(request, format=None):
    """
    This function takes in a POST request with a twitter username. The given username has all its mentions searched for and
    the resuts are sent as JSON objects. The average runtime of a request is 29 seconds :(
    """

    if request.method == 'POST':
        # A serializer allows data to be collected from a POST request
        serializer = TwitterAnalyserSerializer(data=request.data)

        # If the serializer is valid, send twitter username to function that collects and
        # analyses tweets
        if serializer.is_valid():
            try:
                tweet_username = (serializer.validated_data['twitter_user'])
                analysed_json = tweetanalyzer.query_topic_from_twitter(tweet_username)

            except Exception as e:
                return JsonResponse(str(e), safe=False)
                print(e)

            return JsonResponse(analysed_json, safe=False, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




########################## This function allows for the updating, deleting and putting of tweets. ###############################
@csrf_exempt
def tweet_detail(request, pk):
    """
    Retrieve, update or delete a tweet.
    """
    try:
        tweet = Tweet.objects.get(pk=pk)
    except Tweet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TweetSerializer(tweet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TweetSerializer(tweet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        tweet.delete()
        return HttpResponse(status=204)





