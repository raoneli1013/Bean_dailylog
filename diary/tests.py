from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from user.models import User
from .models import Diary, Comment
from .serializers import DiarySerializer
# 이미지 업로드에 필요한 import
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile, random
# 가상 데이터
from faker import Faker


# 임시파일로 임시이미지 만들기
def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file,'png')
    return temp_file

# diary test
class DiaryUploadAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls): # test 할 때 모든 메소드에서 실행이 된다 (setUpTestData)
        cls.user_data = {"email":"testdiary@gmail.com",
                         "password":"password"
                         } # 회원가입을 위한 데이터
        cls.diary_data = {"title":"test title","content":"test content"} # diary 작성을 위한 데이터
        cls.user = User.objects.create_user("testdiary@gmail.com","password") # 회원가입
        cls.diary = Diary.objects.create(**cls.diary_data, user=cls.user) # diary

    def setUp(self): # client는 클래스 메소드가 아니라 setUp으로 만듦.
        self.access_token = self.client.post(
            reverse("users:token_obtain_pair"), self.user_data).data["access"] # 로그인하여 access token 가져오기

    def test_fail_if_not_logged_in(self): # 로그인 안 되어 있을 때
        url = reverse("diary")
        response = self.client.post(url, self.diary_data)
        self.assertEqual(response.status_code, 401)

    def test_create_diary(self): # diary 생성
        response = self.client.post(
            path=reverse("diary"),
            data=self.diary_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.data["message"], "diary 작성완료")

    def test_create_diary_image(self):
        # 임시 이미지 파일 생성
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)

        # 첫 번째 프레임 받아오기
        image_file.seek(0)
        self.diary_data["article_img"]=image_file

        # 전송
        response = self.client.post(
            path=reverse("diary"),
            data=encode_multipart(data=self.diary_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.data["message"], "diary 작성완료")

class DiaryReadAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.diaries = []
        for i in range(10):
            cls.user = User.objects.create_user(cls.faker.name(), cls.faker.word())
            cls.diaries.append(Diary.objects.create(title=cls.faker.sentence(), content=cls.faker.text(), user=cls.user))
            # faker를 이용해서 title, content, user를 매번 랜덤으로 생성

    def test_get_diary(self):
        for diary in self.diaries:
            url = diary.get_absolute_url() # diary의 url을 받아온다.
            response = self.client.get(url)
            serializer = DiarySerializer(diary).data # response와 diary를 비교
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value) # self.assertEqual(diary.title, response.data["title"]) 등 일일히 하지 않도록.
                



# 코멘트 생성 , 조회 뷰
class CommentViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "q1w2e3r4"}
        cls.diary_data = {"title": "test Title", "content": "content"}
        cls.comment_data = {"content": "content"}
        cls.user = User.objects.create_user(
            "test@test.com", "q1w2e3r4")
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
        cls.user_data = {"email": "test@test.com", "password": "q1w2e3r4"}
        cls.diary_data = {"title": "test Title", "content": "content"}
        cls.comment_data = [
            {"content": "test 1"},
            {"content": "test 2"},
            {"content": "test 3"},
            {"content": "test 4"},
            {"content": "test 5"},
        ]
        cls.user = User.objects.create_user(
            "test@test.com", "q1w2e3r4")
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
    

