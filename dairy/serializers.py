from rest_framework import serializers
from dairy.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = ["id", "content", "created_at", "updated_at", "user",]