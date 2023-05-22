from rest_framework.views import APIView
from .models import Diary
from rest_framework.response import Response
from .serializers import DiarySerializer, DiaryCreateSerializer, DiaryPutSerializer
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404



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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST) #요청오류
        
class DiaryDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,id):
        Diary = get_object_or_404(Diary,id=id)
        serialize = DiarySerializer(Diary)
        return Response(serialize.data)
    
    
    def put(self,request,id):
        Diary = get_object_or_404(Diary,id=id)
        if request.user == Diary.user:
            serializer = DiaryPutSerializer(Diary,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'권한이 없습니다'},status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self,request,id):
        Diary = get_object_or_404(Diary,id=id)
        if request.user == Diary.user:
            Diary.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':'권한이 없습니다'},status=status.HTTP_401_UNAUTHORIZED)