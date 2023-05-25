from rest_framework.views import APIView
from .models import Diary, Comment
from rest_framework.response import Response
from .serializers import DiarySerializer, DiaryCreateSerializer, DiaryPutSerializer
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentSerializer
from rest_framework.viewsets import ViewSet

from .tasks import create_image_task
from celery.result import AsyncResult

import os
import requests
from urllib.parse import urlparse
from datetime import datetime
from django.conf import settings

class ImageViewSet(ViewSet):
    def create(self, request):
        user_input = request.data.get('prompt')
        diary_id = request.data.get('diary_id')

        # 이미지 생성 작업을 백그라운드로 실행
        task = create_image_task.delay(user_input)

        # 작업 ID를 반환
        return Response({"task_id": str(task.id)})

    def retrieve(self, request, pk=None):
        task = AsyncResult(pk)

        if task.ready():
            # 작업이 완료되면 이미지 URL 반환
            img_url = task.result

            # 이미지 다운로드 및 저장 작업 시작
            response = requests.get(img_url, stream=True)
            response.raise_for_status()  #만약 다운로드시 문제가 있다면 에러

            subdirs = datetime.now().strftime('%Y/%m/%d')
            os.makedirs(os.path.join('media', subdirs), exist_ok=True)
            image_filename = os.path.join('media', subdirs, os.path.basename(urlparse(img_url).path))

            with open(image_filename, 'wb') as out_file:
                out_file.write(response.content)

            image_url = image_filename.replace(str(settings.MEDIA_ROOT), settings.MEDIA_URL)
            image_url = image_url.replace('\\', '/')

            return Response({"status": "complete","url": image_url})
        else:
            # 작업이 진행 중이면 현재 상태 반환
            return Response({"status": "pending"})


class DiaryView(APIView):
    def get(self,request):
        diaries = Diary.objects.all()
        serialize = DiarySerializer(diaries, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)
        
    
    def post(self,request):
        if not request.user.is_authenticated:
            return Response("로그인을 해주세요.", status=status.HTTP_401_UNAUTHORIZED) 
        serializer = DiaryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response({"message":"diary 작성완료"})
        else:
            return Response({"message":f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST) #요청오류

class DiaryDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self,request,id):
        diary = get_object_or_404(Diary,id=id)
        serialize = DiarySerializer(diary)
        return Response(serialize.data)
    
    
    def put(self,request,id):
        diary = get_object_or_404(Diary,id=id)
        if request.user == diary.user:
            serializer = DiaryPutSerializer(diary,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'권한이 없습니다'},status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self,request,id):
        diary = get_object_or_404(Diary,id=id)
        if request.user == diary.user:
            diary.delete()
            return Response({'message':'삭제되었습니다'},status=status.HTTP_204_NO_CONTENT)
    
    def delete(self,request,id):
        diary = get_object_or_404(Diary,id=id)
        if request.user == diary.user:
            diary.delete()
            return Response({'message':'삭제되었습니다'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':'권한이 없습니다'},status=status.HTTP_401_UNAUTHORIZED)
        
#댓글
class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
     # comment/<diary_id>/ 댓글 리스트
    def get(self, request, diary_id):
        comment = Comment.objects.filter(diary_id = diary_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    #comment/<diary_id>/ 댓글 생성
    def post(self, request, diary_id):
        diary = get_object_or_404(Diary, pk=diary_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, diary=diary)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class CommentDetailView(APIView):
    # comment/<diary_id>/<comment_id>/ 댓글 수정
    def put(self, request, diary_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "댓글이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response({"error": "댓글 작성자만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # comment/<diary_id>/<comment_id>/ 댓글 삭제
    def delete(self, request, diary_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "댓글이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response({"error": "댓글 작성자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




    #좋아요
class DiaryLikeView(APIView):
    def post(self, request, diary_id):
        diary = get_object_or_404(Diary, id=diary_id)
        if request.user in diary.likes.all():
            diary.likes.remove(request.user)
            return Response('좋아요 취소', status=status.HTTP_200_OK)
        else:
            diary.likes.add(request.user)
            return Response('좋아요', status=status.HTTP_200_OK)
        

    
    #북마크
class BookMarksView(APIView):
    def post(self, request, diary_id):
        diary = get_object_or_404(Diary, id=diary_id)
        if request.user in diary.bookmarks.all():
            diary.bookmarks.remove(request.user)
            return Response('북마크 취소', status=status.HTTP_200_OK)
        else:
            diary.bookmarks.add(request.user)
            return Response('북마크', status=status.HTTP_200_OK)

