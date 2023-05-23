from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Django 프로젝트의 설정을 'settings.py'에서 가져옵니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bean_dailylog.settings')

# Celery 애플리케이션 객체를 생성합니다.
# 이 객체를 사용하여 Celery 작업을 만들고 관리할 수 있습니다.
app = Celery('bean_dailylog')

# Celery가 Django 프로젝트의 설정 파일을 사용하도록 합니다.
# 'CELERY_'로 시작하는 설정 항목들을 찾아서 읽어옵니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django 앱에 정의된 작업을 자동으로 불러옵니다.
# 'tasks.py' 파일에 작업을 정의해 놓으면 이 코드에 의해 자동으로 불러와집니다.
app.autodiscover_tasks()
