from django.contrib import admin

from .models import Question, Choice


# .StackedInline -> .TabularInline 더욱 조밀한 테이블 형태
class ChoiceInline(admin.TabularInline):
    # 모델 및 엑스트라 지정
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    # 제목, 발행일 -> 발행일, 제목으로 순서 변경
    # fields = ['pub_date', 'question_text']
    # fieldset 분할 및 fieldset 제목 추가
    fieldsets = [
        ('Question Title', {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']})
    ]
    # Question 모델 관리 페이지에서 Choice 모델도 관리할 수 있도록 등록
    inlines = [ChoiceInline]
    # 목록 페이지에서 보여줄 정보의 컬럼 추가
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # 생성일 필터링 기능 추가
    list_filter = ['pub_date']
    # 검색 기능 추가
    search_fields = ['question_text']


# 모델 등록
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
