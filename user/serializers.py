from rest_framework import serializers, exceptions
from user.models import User
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from diary.models import Feed_like,Boookmark,Diary
from diary.serializers import DiarySerializer
from allauth.account.adapter import get_adapter,DefaultAccountAdapter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['nickname'] = user.nickname

        return token




# 유저 프로필 view

#diary model의 좋아요와 북마크를 가져와서 직렬화
class FeedLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed_like
        fields = "__all__"

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boookmark
        fields = "__all__"

class MydiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = "__all__"

#유저 프로필 시리얼라이저 - 팔로우/팔로워,좋아요목록,북마크목록,내가 작성한 게시글목록, 프로필이미지
class UserProfileSerializer(serializers.ModelSerializer):
    followers = UserSerializer(many=True)
    likes_diary = serializers.SerializerMethodField()
    bookmark_diary = serializers.SerializerMethodField()
    my_diary= serializers.SerializerMethodField()
    profile_img = serializers.ImageField(
        max_length=None,
        use_url=True,
        required=False,
    )

    #좋아요 목록
    def get_likes_diary(self, obj):
        likes = Feed_like.objects.filter(user=obj)
        return FeedLikeSerializer(likes, many=True).data
    #북마크 목록
    def get_bookmark_diary(self, obj):
        bookmarks = Boookmark.objects.filter(user=obj)
        return BookmarkSerializer(bookmarks, many=True).data
    #게시글 목록
    def get_my_diary(self, obj):
        diaries = Diary.objects.filter(user=obj)
        return DiarySerializer(diaries, many=True).data

    class Meta:
        model = User
        fields = ("id", "email", "nickname", 
                "introduction", "profile_img", "followings", 
                "followers", "likes_diary", "bookmark_diary","my_diary")



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "nickname", "introduction", "profile_img")
        read_only_fields = ["email","password",]
        extra_kwargs = {
            # "profile_img": {
            #     "read_only": True,
            # },
            "nickname": {
                "required": False,
            },
        }

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
