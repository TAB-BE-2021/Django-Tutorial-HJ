import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        '''시간을 현재로부터 30일 이후(미래)로 설정한 후
        was_published_recently() 함수를 실행했을 때 False가 나오는지 테스트'''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        '''시간을 현재루부터 1일(24시간) 1초 이전(과거)로 설정한 후
        was_published_recently() 함수를 실행했을 때 False가 나오는지 테스트'''
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        '''시간을 현재루부터 23시간 59분 59초 이전(과거)로 설정한 후
        was_published_recently() 함수를 실행했을 때 True가 나오는지 테스트'''
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


# question_text와 days를 파라미터로 전달받아 질문 생성
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexVewTests(TestCase):
    def test_no_questions(self):
        # 질문을 추가하지 않고 요청했을 때 질문 목록 테스트
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        # 30일 전으로 시간이 설정된 질문을 추가한 후 요청했을 때 질문 목록 테스트
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [question])

    def test_future_question(self):
        # 30일 후로 시간이 설정된 질문을 추가한 후 요청했을 때 질문 목록 테스트
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_qustion(self):
        # 30일 전과 후로 시간이 설정된 질문을 각각 추가한 후 요청했을 때 질문 목록 테스트
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [question])

    def test_two_past_questions(self):
        # 30일 전과 5일 전으로 시간이 설정된 질문을 각각 추가한 후 요청했을 때 질문 목록 테스트
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [
                                 question2, question1])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        # 5일 후로 시간이 설정된 질문의 DetailView 요청했을 때 테스트
        future_question = create_question(
            question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def teset_past_question(self):
        # 5일 전으로 시간이 설정된 질문의 DetailView 요청했을 때 테스트
        past_question = create_question(
            question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
