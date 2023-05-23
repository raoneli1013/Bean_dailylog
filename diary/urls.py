from django.urls import path
from diary import views




urlpatterns = [
    path('', views.DiaryView.as_view(), name="diary"),
    path('<int:id>/', views.DiaryDetailView.as_view(), name="diary_detail"),
    path('comment/<int:diary_id>/', views.CommentView.as_view(), name="comment"),

]
