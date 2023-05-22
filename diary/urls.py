from django.urls import path
from diary import views

urlpatterns = [
    path('', views.DiaryView.as_view()),
    path('<int:id>/', views.DiaryDetailView.as_view()),

]
