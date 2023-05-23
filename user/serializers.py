from rest_framework import serializers, exceptions
from user.models import User
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from diary.models import Feed_like, Boookmark



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

    followers = UserSerializer(many=True)
    # bookmark_diary = serializers.SerializerMethodField() 
    # likes_diary_count = serializers.SerializerMetaclass()
    profile_img = serializers.ImageField(
        max_length=None,
        use_url=True,
        required=False,
    )


    class Meta:
        model = User
        fields = ("id", "email", "nickname", "introduction", "profile_img", "followings", "followers",)
        


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
