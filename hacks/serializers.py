from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class WriterSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Writer
        fields = '__all__'

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'created', 'writer', 'body', 'upvote', 'downvote', 'vote_net', 'reply_count', "replies"]

class HackSerializer(serializers.ModelSerializer):
    writer = WriterSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Hack
        fields = ['id', 'created', 'writer', 'body', 'upvote', 'downvote', 'vote_net', 'comment_count', "comments", "writer"]

