from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
# from user.serializers


# class ProfileView(APIView):
#     def get_object(self, user_id):
#         return get_object_or_404(User, id=user_id)
    
