from django.urls import path, include
from user import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.UserView.as_view(), name="user_view"),
    path('<int:user_id>/', views.ProfileView.as_view(), name="user_profile_view"),
    # dj-rest-auth
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # 구글 소셜로그인
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
#     #마이페이지,팔로우,회원탈퇴
#     path('profile/<int:user_id>/', views.ProfileView.as_view(), name="profile_view"), # /users/profile/<int:user_id>/
#     path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'), # /users/follow/<int:user_id>/
#     path("withdrawal/", views.WithdrawalView.as_view(), name='withdrawal'), # /users/withdraw/

]

