from rest_framework import serializers, exceptions
from user.models import User
from django.conf import settings

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

    # def get_dairy_like_count(self, obj):
    #     return obj.

    # class Meta:

