from django.urls import path

from . import views

urlpatterns = [
    # ''경로로 요청이 들어올 경우 views파일의 index함수 호출
    path('', views.index, name='index'),
]
