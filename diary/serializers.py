from rest_framework import serializers
from .models import Diary, Comment

class DiarySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField

    def get_user(self, dir):
        return dir.user.nickname

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