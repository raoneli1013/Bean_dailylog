from rest_framework import serializers, exceptions
from user.models import User
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dairy.models import Feed_like, Boookmark



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
class UserProfileSerializer(serializers.ModelSerializer):

    followings = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)
    bookmark_dairy_count = serializers.SerializerMetaclass()
    likes_dairy_count = serializers.SerializerMetaclass()
    profile_img = serializers.ImageField(
        max_length=None,
        use_url=True,
        required=False,
    )

    #
    def get_bookmark_count(self):
        return Boookmark.feed.count()

    class Meta:
        model = User
        fields = ("id","email","nickname","introduction","profile_img","followings")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "nickname", "introduction", "profile_img")
        read_only_fields = ["email",]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
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
