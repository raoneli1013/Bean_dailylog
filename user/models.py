from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        superuser = self.create_user(
            email=email,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser):

    email = models.EmailField("email address", max_length=50, unique=True, null=False, blank=False)
    password = models.CharField("비밀번호", max_length=50)
    nickname = models.CharField("이름", max_length=100)
    introduction = models.TextField("자기소개", null=True, blank=True)
    profile_img = models.ImageField("프로필 이미지", blank=True, upload_to="profile/%Y/%m/")
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True)


    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.email.split("@")[0]
        super().save(*args, **kwargs)
        
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

