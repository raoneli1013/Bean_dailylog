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
        model = Diary
        fields = '__all__'


class DiaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["title", "content",
                  "article_img", "created_at", "updated_at"] # '__all__'하면 user가 필수값이라 게시글 생성 시 user값이 없으면 오류.


class DiaryPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["title", "content",
                  "article_img"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ["id", "content", "created_at", "updated_at", "user",]
