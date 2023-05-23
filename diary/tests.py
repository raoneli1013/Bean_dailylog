from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient,APITestCase
from diary.views import *
from user.models import User
from diary.models import Diary, Comment
from django.urls import reverse
# Create your tests here.


# 코멘트 생성 , 조회 뷰
class CommentViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com","nickname":"name", "password": "q1w2e3r4"}
        cls.diary_data = {"title": "test Title", "content": "content"}
        cls.comment_data = {"content": "content"}
        cls.user = User.objects.create_user(
            "test@test.com", "name", "q1w2e3r4")
        cls.diary = Diary.objects.create(**cls.diary_data, user=cls.user)

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    # 코멘트 작성
    def test_create_diary_success(self):
        response = self.client.post(
            path=reverse("comment", kwargs={"diary_id": 1}),
            data=self.comment_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, "content")
        
        
    # 코멘트 리스트 모두보기(아무것도 없을 때)
    def test_comment_list_empty(self):
        response = self.client.get(
            path=reverse("comment", kwargs={"diary_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    # 코멘트 리스트
    def test_comment_list(self):
        self.comments = []
        for _ in range(5):
            self.comments.append(
                Comment.objects.create(
                    **self.comment_data, diary=self.diary, user=self.user
                )
            )
        response = self.client.get(
            path=reverse("comment", kwargs={"diary_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]["content"], "content")


# 코멘트 , 수정, 삭제 뷰
class CommentDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com","nickname":"name", "password": "q1w2e3r4"}
        cls.diary_data = {"title": "test Title", "content": "content"}
        cls.comment_data = [
            {"content": "test 1"},
            {"content": "test 2"},
            {"content": "test 3"},
            {"content": "test 4"},
            {"content": "test 5"},
        ]
        cls.user = User.objects.create_user(
            "test@test.com", "name", "q1w2e3r4")
        cls.diary = Diary.objects.create(**cls.diary_data, user=cls.user)
        cls.comments = []
        for i in range(5):
            cls.comments.append(
                Comment.objects.create(
                    **cls.comment_data[i], diary=cls.diary, user=cls.user
                )
            )

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    # 코멘트 수정
    def test_comment_update(self):
        response = self.client.put(
            path=reverse(
                "comment_detail", kwargs={"diary_id": 1, "comment_id": 1}
            ),
            data={"content": "updated test content"},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(response.data["content"], "updated test content")

    # 코멘트 삭제
    def test_comment_delete(self):
        response = self.client.delete(
            path=reverse(
                "comment_detail", kwargs={"diary_id": 1, "comment_id": 1}
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 4)
        self.assertEqual(response.data, None)
    