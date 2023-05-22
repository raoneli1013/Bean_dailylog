from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dairy.models import Comment, Dairy
from dairy.serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, dairy_id):
        comment = Comment.objects.filter(dairy_id = dairy_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)
    
    def post(self, request, dairy_id):
        dairy = get_object_or_404(Dairy, pk=dairy_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, dairy=dairy)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
    
    def put(slef, request, comment_id):
        pass
    
    def delete(self, request, comment_id):
        pass
    
    
