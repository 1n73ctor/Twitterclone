import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from .models import Tweet
from .forms import TweetForm
from .serializers import (
        TweetSerializer, 
        TweetActionSerializer,
        TweetCreateSerializer
     )
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

Allowed_host = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", status=200)

@api_view(['POST']) # specific methods 
@permission_classes([IsAuthenticated])
# @permission_classes([SessionAuthentication])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.POST or None)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response({}, status=400)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({'You Are Not Valid To Delete This Post'}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({'Tweet Removed'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    if action =="like":
        obj.likes.add(request.user)
        serializer = TweetSerializer(obj)
        return Response(serializer.data, status=200)
    elif action == "unlike":
        obj.likes.remove(request.user)
    elif action == "retweet":
        new_tweet = Tweet.objects.create(
            user=request.user,
            parent=obj,
            content=content
        )
        serializer = TweetSerializer(new_tweet)
        return Response(serializer.data, status=200)
    return Response({'liked'}, status=200)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)


# def tweet_create_view_pure_django(request, *args, **kwargs):
#     user = request.user
#     if not request.user.is_authenticated:
#         user = None
#         if request.is_ajax():
#             return JsonResponse({}, status=401)
#     print(request.is_ajax())
#     Form = TweetForm(request.POST or None)
#     nxt_url = request.POST.get("next") or None
#     print(nxt_url)
#     if Form.is_valid:
#         obj = Form.save(commit=False)
#         obj.user = request.user or None
#         obj.save()
#         if request.is_ajax():
#             return JsonResponse(obj.serialize(), status=201)
#         if nxt_url != None and is_safe_url(nxt_url, Allowed_host):
#             return redirect(nxt_url)
#         Form = TweetForm()
#         if Form.errors:
#             if request.is_ajax():
#                 return JsonResponse(form.erros, status=400)
        
#     return render(request, 'components/form.html', context={"form": Form})


# def tweet_list_view(request, *args, **kwargs):
#     qs = Tweet.objects.all()
#     tweet_list = [tweets.serialize() for tweets in qs]
#     data = {
#         "isUser": False, 
#         "response": tweet_list
#     }

#     return JsonResponse(data)


# def tweet_detail_view(request, tweet_id, *args, **kwargs):
#     data = {
#         "id": tweet_id,
#     }
#     status = 200
#     try:
#         obj = Tweet.objects.get(id=tweet_id)
#         data['content'] = obj.content
#     except:
#         data['message'] = 'data not found'
#         status = 404
    
#     return JsonResponse(data, status=status)