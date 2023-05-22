from django.urls import path
from user import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.UserView.as_view(), name="user_view"),
    path('<int:user_id>/', views.ProfileView.as_view(), name="user_profile_view"),


#     #마이페이지,팔로우,회원탈퇴
#     path('profile/<int:user_id>/', views.ProfileView.as_view(), name="profile_view"), # /users/profile/<int:user_id>/
#     path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'), # /users/follow/<int:user_id>/
#     path("withdrawal/", views.WithdrawalView.as_view(), name='withdrawal'), # /users/withdraw/

]

