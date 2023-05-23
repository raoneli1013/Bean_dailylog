from rest_framework import serializers
from .models import Diary, Comment

class DiarySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()

    def get_user(self, dir):
        return dir.user.nickname
    
    #좋아요 갯수
    def get_likes_count(self, obj):
        return obj.feed_like_set.count()

    #북마크 갯수
    def get_bookmarks_count(self, obj):
        return obj.bookmark_set.count()

    class Meta:
        models = Diary
        fields = ['__all__']


class DiaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['__all__']


class DiaryPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['__all__']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = ["id", "content", "created_at", "updated_at", "user",]