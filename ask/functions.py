from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
from models import *


def get_current_page(request):
    page_num = request.GET.get("page")
    try:
        if page_num is None or int(page_num)<= 0:
            return 1
    except:
        return 1

    return int(page_num)


def get_count_of_question_pages():
    cnt = Question.objects.count()
    if cnt % 20 == 0:
        return cnt / 20
    return cnt / 20 + 1


def get_count_of_answer_pages(byid):
    que = Question.objects.get(id=byid)
    cnt = Answer.objects.filter(question=que).count()
    if cnt % 30 == 0:
        return cnt / 30
    return cnt / 30 + 1


def get_sort_type(request, default="popular"):
    t = request.GET.get("sort_by")
    if t is None:
        return default
    if t == "news":
        return "news"
    return "popular"


def get_questions_by_date(page):
    return Question.objects.order_by("-date")[(page-1)*20:page*20]


def get_questions_by_rate(page):
    return Question.objects.order_by("-rate", "date")[(page-1)*20:page*20]


def get_answers_sort(page, byid):
    return Answer.objects.filter(question=Question.objects.get(id=byid)).order_by("-rate", "date")[(page-1)*30:page*30]


def get_pages_range(current_page, count_of_pages, delta):
    if 2*delta > count_of_pages:
        return {"jtmin": False, "jtmax": False, "range": range(1, count_of_pages+1)}
    min_page = current_page - delta
    max_page = current_page + delta

    jump_to_min = False
    jump_to_max = False

    if min_page < 1:
        max_page += 1 - min_page
        min_page = 1
    elif min_page > 1:
        jump_to_min = True

    if max_page > count_of_pages:
        min_page += count_of_pages - max_page + 1
        max_page = count_of_pages + 1
    elif max_page < count_of_pages:
        jump_to_max = True

    return {"jtmin": jump_to_min, "jtmax": jump_to_max, "range": range(min_page, max_page)}


def get_last_10_signedup():
    return User.objects.filter(is_superuser=0).order_by("-date_joined")[0:10]