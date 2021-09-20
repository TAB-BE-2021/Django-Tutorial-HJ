from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Question


# 뷰(URL을 통해 호출할 수 있음)
def index(request):
    # 'pub_date'에 '-'를 붙여 내림차순(최신수)으로 정렬
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # 템플릿 파라미터 변수(JSON과 같은 역할)
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # 객체가 존재하지 않을 경우 404 발생
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
