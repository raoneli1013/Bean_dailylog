from rest_framework import serializers
from user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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


class UserProfileSerializer(serializers.ModelSerializer):

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