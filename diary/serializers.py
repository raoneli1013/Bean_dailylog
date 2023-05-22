from rest_framework import serializers
from .models import Diary, Comment


class DiarySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField

    def get_user(self, dir):
        return dir.user.nickname

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
