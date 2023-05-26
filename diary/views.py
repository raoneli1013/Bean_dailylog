from rest_framework.views import APIView
from .models import Diary, Comment
from rest_framework.response import Response
from .serializers import DiarySerializer, DiaryCreateSerializer, DiaryPutSerializer
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentSerializer
from rest_framework.viewsets import ViewSet

import os
import requests
from urllib.parse import urlparse
from datetime import datetime
from django.conf import settings

from rest_framework.decorators import api_view
from .tasks import create_image_task
from celery.result import AsyncResult
from rest_framework.permissions import BasePermission # 비밀글 작성자만 보기

class ImageViewSet(ViewSet):
    def create(self, request):
        user_input = request.data.get('prompt')

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


class ImageViewSet(ViewSet):
    def create(self, request):
        user_input = request.data.get('prompt')

        # 이미지 생성 작업을 백그라운드로 실행
        task = create_image_task.delay(user_input)

        # 작업 ID를 반환
        return Response({"task_id": str(task.id)})

    def retrieve(self, request, pk=None):
        task = AsyncResult(pk)

        if task.ready():
            # 작업이 완료되면 이미지 URL 반환
            return Response({"status": "completed", "url": task.result})
        else:
            # 작업이 진행 중이면 현재 상태 반환
            return Response({"status": "pending"})


class Test_add(ViewSet):
    def create(self,request):
        user_input = request.data.get('num')
        task = add.delay(*user_input)

        # 작업 ID를 반환합니다.
        return Response({"task_id": task.id})

    def retrieve(self, request, pk=None):
        task = AsyncResult(pk)

        if task.ready():
            return Response({"status": "completed", "result": task.result})
        else:
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
            return Response({"message":"diary 작성완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST) #요청오류

class IsOwnerOrPublicRead(BasePermission): # 사용자 정의 권한 클래스
    def has_object_permission(self, request, view, diary): # 비공개 다이어리 GET요청시 작성자만 접근할 수 있도록 하는 함수
        
        if request.method in ['GET']:
            return not diary.is_private or (request.user.is_authenticated and diary.user == request.user) # 공개 다이어리는 누구나 접근 가능
        return diary.user == request.user # 사용자가 작성자인지 확인
    
# class DiaryDetailView(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     def get(self,request,id):
#         diary = get_object_or_404(Diary,id=id)
#         serialize = DiarySerializer(diary)
#         return Response(serialize.data)
    

class DiaryDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        dir = get_object_or_404(Diary, id=self.kwargs["id"])
        self.check_object_permissions(self.request, dir)
        return dir

    def get(self, request, id):
        diary = get_object_or_404(Diary, id=id)
        if diary.is_private == True: # 비공개인 경우
            if diary.user != request.user:
                self.permission_classes = [IsOwnerOrPublicRead] # 사용자 권한 변경
                self.dispatch(request)  # 퍼미션 클래스를 다시 적용하기 위해 dispatch 메서드 호출
                self.check_permissions(request) # request에 대한 권한을 확인
                return Response({'message': '작성자 본인만 접근할 수 있습니다.'})
            else:
                serialize = DiarySerializer(diary)
                return Response(serialize.data)
        else:
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

