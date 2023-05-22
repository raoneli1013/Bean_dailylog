from django.contrib import admin
from django.urls import path, include
from dairy import views

urlpatterns = [
    path('comment/<int:dairy_id>/', views.CommentView.as_view(), name="comment"),
]
