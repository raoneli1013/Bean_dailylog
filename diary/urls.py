from django.urls import path
from diary import views



urlpatterns = [
    path('', views.DiaryView.as_view()),
    path('<int:id>/', views.DiaryDetailView.as_view()),
    path('comment/<int:diary_id>/', views.CommentView.as_view(), name="comment"),
    #좋아요
    path('<int:diary_id>/likes/', views.DiaryLikeView.as_view(), name="likes_diary"),
    path('<int:diary_id>/bookmark/', views.BookMarksView.as_view(), name="likes_diary"),

]
