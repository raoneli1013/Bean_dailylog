from django.urls import path, include, re_path
from user import views
from dj_rest_auth.registration.views import VerifyEmailView


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
    #마이페이지,팔로우,회원탈퇴
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name="profile_view"),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'),

    # 유효한 이메일이 유저에게 전달
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # 유저가 클릭한 이메일(=링크) 확인
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', views.ConfirmEmailView.as_view(), name='account_confirm_email'),
]

