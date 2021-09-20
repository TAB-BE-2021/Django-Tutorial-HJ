from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ''경로로 요청이 들어올 경우 views파일의 index함수 호출
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
