from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User
from rest_framework.test import APIClient
from .serializers import UserProfileSerializer



# Create your tests here.

class UserAPITestcase(APITestCase):
    def test_signup(self):
        client = APIClient()
        url = reverse("user_view")
        user_data = {
                "email": "testcode@ccc.com",
                "password": "123",
                "nickname": "testcode"
        }
        response= self.client.post(url,user_data, format="json")
        self.assertEqual(response.status_code, 201)
        # 가입된 사용자의 ID 값을 추출
        user_id = response.data
        print("???",user_id)
        
        # 이후의 요청에서 가입자의 ID 값을 사용하여 테스트 진행
        # 예를 들어, 가입자 프로필 조회 요청
        profile_response = client.get(f"/api/user/{user_id}/")

        self.assertEqual(response.status_code, 201)



class  LoginUserTest(APITestCase):

    def setUp(self):
        self.data = {'email':'testcode@ccc.com','password':'123',"nickname": "testcode" }
        self.user = User.objects.create_user('testcode@ccc.com','testcode','123')

    
    def test_login(self):
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        self.assertEqual(response.status_code, 200)


# 프로필 테스트코드
# class ProfileReadTest(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user_data = {"email": "test@test.com", "password": "q1w2e3r4"}
#         cls.users = []
#         cls.user = User.objects.create_user(
#             email=cls.user_data["email"], password=cls.user_data["password"])

#     def setUp(self):
#         self.access_token = self.client.post(
#             reverse("dj_rest_auth.registration.urls"), self.user_data
#         ).data["access"]

    # def test_get_profile(self):
    #     url = self.user.get_absolute_url()
    #     response = self.client.get(url)
    #     serializer = UserProfileSerializer(self.user).data
    #     self.assertEqual(response.data, serializer)
        
