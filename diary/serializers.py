from rest_framework import serializers
from .models import Diary, Comment


class DiarySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField
    likes_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()

    def get_user(self, dir):
        return dir.user.nickname
    
    #좋아요 갯수
    def get_likes_count(self, obj):
        return obj.diary_likes.count()

    #북마크 갯수
    def get_bookmarks_count(self, obj):
        return obj.bookmarks.count()
    

    
    class Meta:
        model = Diary
        fields = '__all__'


class DiaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["title", "content",
                  "article_img", "created_at", "updated_at", "is_private"] # '__all__'하면 user가 필수값이라 게시글 생성 시 user값이 없으면 오류.


class DiaryPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["title", "content",
                  "article_img"]


class CommentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    def get_name(self, dir):
        return dir.user.nickname
    
    def get_user(self, dir):
        return dir.user.id

    class Meta:
        model = Comment
        fields = ["id", "content", "created_at", "updated_at", "name", "user",]
        extra_kwargs = {
            "user": {
                "required": False,  # 유저필드를 사용은 하지만 있어도 되고 없어도 되게 만드는 법
            }
        }
