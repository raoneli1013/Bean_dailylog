from django.urls import path,include
from diary import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'images', views.ImageViewSet, basename='image')

urlpatterns = [
    path('', views.DiaryView.as_view(), name="diary"),
    path('<int:id>/', views.DiaryDetailView.as_view(), name="diary_detail"),
    path('comment/<int:diary_id>/', views.CommentView.as_view(), name="comment"),
    path('', include(router.urls)),
    path('comment/<int:diary_id>/<int:comment_id>/', views.CommentDetailView.as_view(), name="comment_detail"),
    #좋아요
    path('<int:diary_id>/likes/', views.DiaryLikeView.as_view(), name="likes_diary"),
    path('<int:diary_id>/bookmark/', views.BookMarksView.as_view(), name="bookmark_diary"),
]
