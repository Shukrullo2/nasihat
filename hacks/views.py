from typing import Any, Dict
from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
# Create your views here.

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['username'] = self.user.username
        data['telegram'] = self.user.writer.telegram
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




@api_view(['GET'])
def getHacks(request):
    hacks = Hack.objects.all()
    serializer = HackSerializer(hacks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTopHacks(request):
    hacks = Hack.objects.order_by('-vote_net')[:40]
    serializer = HackSerializer(hacks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getNewHacks(request):
    fourteen_days_ago = timezone.now() - timedelta(days=14)
    hacks = Hack.objects.filter(created__gte=fourteen_days_ago).order_by('-created')[:40]
    serializer = HackSerializer(hacks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getHotHacks(request):
    seven_days_ago = timezone.now() - timedelta(days=7)
    hacks = Hack.objects.filter(created__gte=seven_days_ago).order_by('-vote_net')[:40]
    serializer = HackSerializer(hacks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getHack(request,pk):
    hack = Hack.objects.get(id=pk)
    serializer = HackSerializer(hack)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getWriters(request):
    writers = Writer.objects.all()
    serializer = WriterSerializer(writers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getComments(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getReplies(request):
    replies = Reply.objects.all()
    serializer = ReplySerializer(replies, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createHack(request):
    data = request.data 
    if data.get('telegram'):
        writer, created = Writer.objects.get_or_create(username=data['username'], telegram=data['telegram'])
    elif data.get('twitter'):
        writer, created = Writer.objects.get_or_create(username=data['username'], twitter=data['twitter']) 
    else:
        writer, created = Writer.objects.get_or_create(username=data['username'])
    try:
        hack = Hack.objects.create(
            body = data['body'],
            writer = writer,
        )

        serializer = HackSerializer(hack, many=False)
        message = {'success': "true"}
        return Response(message)
    except:
        message = {'detail': 'something_went_wrong'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createComment(request):
    data = request.data 
    hack = Hack.objects.get(id=data['hack_id'])
    if data.get('twitter'):
        writer, created = Writer.objects.get_or_create(username=data['username'], twitter=data['twitter'])
    else:
        writer, created = Writer.objects.get_or_create(username=data['username'])
    try:
        comment = Comment.objects.create(
            body = data['body'],
            writer = writer,
            hack = hack
        )

        serializer = HackSerializer(hack, many=False)
        message = {'success': "true"}
        return Response(message)
    except:
        message = {'detail': 'something_went_wrong'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def createReply(request):
    data = request.data 
    comment = Comment.objects.get(id=data['comment_id'])
    if data.get('twitter'):
        writer, created = Writer.objects.get_or_create(username=data['username'], twitter=data['twitter'])
    else:
        writer, created = Writer.objects.get_or_create(username=data['username'])
    try:
        reply = Reply.objects.create(
            body = data['body'],
            writer = writer,
            comment = comment
        )

        serializer = CommentSerializer(comment, many=False)
        message = {'success': "true"}
        return Response(message)
    except:
        message = {'detail': 'something_went_wrong'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createReport(request):
    data = request.data 
    hack = Hack.objects.get(id=data['hack_id'])
    try:
        report = Report.objects.create(
           hack = hack
        )
        message = {'success': "true"}
        return Response(message)
    except:
        message = {'detail': 'something_went_wrong'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def upVote(request):
    data = request.data
    if data.get('hack_id'):
        hack = Hack.objects.get(id=data['hack_id'])
        try:
            hack.upvote += 1
            hack.vote_net +=1
            hack.save()
            serializer = HackSerializer(hack, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'something_went_wrong'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    elif data.get('comment_id'):
        comment = Comment.objects.get(id=data['comment_id'])
        try:
            comment.upvote += 1
            comment.vote_net +=1
            comment.save()
            serializer = CommentSerializer(comment, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'something_went_wrong'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    elif data.get('reply_id'):
        reply = Reply.objects.get(id=data['reply_id'])
        try:
            reply.upvote += 1
            reply.vote_net +=1
            reply.save()
            serializer = ReplySerializer(reply, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'something_went_wrong'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        message = {'detail': 'something_went_wrong'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def downVote(request):
    data = request.data
    if data.get('hack_id'):
        hack = Hack.objects.get(id=data['hack_id'])
        try:
            hack.downvote += 1
            hack.vote_net -=1
            hack.save()
            serializer = HackSerializer(hack, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'something_went_wrong'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    elif data.get('comment_id'):
        comment = Comment.objects.get(id=data['comment_id'])
        try:
            comment.downvote += 1
            comment.vote_net -=1
            comment.save()
            serializer = CommentSerializer(comment, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'something_went_wrong'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    elif data.get('reply_id'):
        reply = Reply.objects.get(id=data['reply_id'])
        try:
            reply.downvote += 1
            reply.vote_net -=1
            reply.save()
            serializer = ReplySerializer(reply, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'something_went_wrong'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        message = {'detail': 'something_went_wrong'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
