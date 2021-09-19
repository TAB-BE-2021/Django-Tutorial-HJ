from django.http import HttpResponse


# 뷰(URL을 통해 호출할 수 있음)
def index(request):
    return HttpResponse("Hello, world. Your're at the polls index.")
