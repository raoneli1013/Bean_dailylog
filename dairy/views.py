from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dairy.models import Comment, Dairy
from dairy.serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    
    # comment/<dairy_id>/ 댓글 리스트
    def get(self, request, dairy_id):
        comment = Comment.objects.filter(dairy_id = dairy_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)
    
    #comment/<dairy_id>/ 댓글 생성
    def post(self, request, dairy_id):
        dairy = get_object_or_404(Dairy, pk=dairy_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, dairy=dairy)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
    
    #comment/<dairy_id>/ 댓글 수정
    def put(self, request, dairy_id):
        try:
            comment = Comment.objects.get(id=dairy_id)
        except Comment.DoesNotExist:
            return Response({"error": "댓글이 없습니다."}, status=404)

        if comment.user != request.user:
            return Response({"error": "댓글 작성자만 수정할 수 있습니다."}, status=403)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    #comment/<dairy_id>/ 댓글 삭제
    def delete(self, request, dairy_id):
        try:
            comment = Comment.objects.get(id=dairy_id)
        except Comment.DoesNotExist:
            return Response({"error": "댓글이 없습니다."}, status=404)

        if comment.user != request.user:
            return Response({"error": "댓글 작성자만 삭제할 수 있습니다"}, status=403)

        comment.delete()
        return Response({"message": "삭제되었습니다."}, status=204)
    
    
