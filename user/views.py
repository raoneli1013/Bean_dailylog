from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from user.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import *

# user/signup/
class UserView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "회원 탈퇴 완료"})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# user/<int:user_id>/
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)
    

#user/follow/<int:user_id>/
class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        serializers = UserProfileSerializer(you)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user

        if me.is_authenticated:
            if you != request.user:
                if me in you.followers.all():
                    you.followers.remove(me)
                    return Response("unfollow",status=status.HTTP_200_OK)
                else:
                    you.followers.add(me)
                    return Response("follow",status=status.HTTP_200_OK)
            else:
                return Response ("본인은 팔로우 할 수 없습니다",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response ("로그인이 필요합니다",status=status.HTTP_400_BAD_REQUEST)
    
