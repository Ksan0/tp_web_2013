from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.models import User, UserManager
from time import gmtime, strftime
from models import *
from forms import *
from functions import *




class QueWithLike():
    def __init__(self, que, v):
        self.question = que
        self.voice = v


class AnsWithLike():
    def __init__(self, ans, v):
        self.answer = ans
        self.voice = v


def main_question(request, ready_context=None):
    count_of_pages = get_count_of_question_pages()
    current_page_number = 1
    sort_by = "popular"

    if request.method == "GET":
        current_page_number = get_current_page(request)
        if current_page_number < 1 or current_page_number > count_of_pages:
            current_page_number = 1
        sort_by = get_sort_type(request)

    questions_tmp = sort_by == "news" and get_questions_by_date(current_page_number) or get_questions_by_rate(current_page_number)
    link_to_pages_tmp = get_pages_range(current_page_number, count_of_pages, 3)
    link_to_pages_jump_left = link_to_pages_tmp["jtmin"]
    link_to_pages_jump_right = link_to_pages_tmp["jtmax"]
    link_to_pages = link_to_pages_tmp["range"]

    questions = []
    for que in questions_tmp:
        try:
            qlike = question_like.objects.get(question=que, user=request.user)
            questions.append(QueWithLike(que, qlike.voice))
        except:
            questions.append(QueWithLike(que, 0))

    context = {
        "current_page_number": current_page_number,  # paint current page number by black
        "count_of_pages": count_of_pages,  # jump right
        "sort_by": sort_by,  # what branch?
        "questions": questions,  # all objects on this page
        "link_to_pages_jump_left": link_to_pages_jump_left,  # draw arrow to the left
        "link_to_pages_jump_right": link_to_pages_jump_right,  # -||- right
        "link_to_pages": link_to_pages,  # draw pages num: 2, 3, 4, 5...
        "import_from": "question_list.htm",
        "signup_form": SignupForm(),
        "signin_form": SigninForm(),
        "ask_form": AskForm(),
        "user": request.user,
        "last_signedup_users": get_last_10_signedup()
    }
    if ready_context is not None:
        context.update(ready_context)

    return render(request, 'main_template.htm', context)


def main_answer(request, ready_context=None):  # we wanna see answers
    que_tmp = None
    try:
        que_tmp = Question.objects.get(id=request.GET.get("id"))
    except BaseException:
        return HttpResponseRedirect("/")
    que_tmp.views += 1
    que_tmp.save()

    count_of_pages = get_count_of_answer_pages(que_tmp.id)
    current_page_number = 1

    if request.method == "GET":
        current_page_number = get_current_page(request)
        if current_page_number < 1 or current_page_number > count_of_pages:
            current_page_number = 1

    answers_tmp = get_answers_sort(current_page_number, que_tmp.id)
    link_to_pages_tmp = get_pages_range(current_page_number, count_of_pages, 3)
    link_to_pages_jump_left = link_to_pages_tmp["jtmin"]
    link_to_pages_jump_right = link_to_pages_tmp["jtmax"]
    link_to_pages = link_to_pages_tmp["range"]

    answers = []
    for ans in answers_tmp:
        try:
            alike = answer_like.objects.get(answer=ans, user=request.user)
            answers.append(AnsWithLike(ans, alike.voice))
        except:
            answers.append(AnsWithLike(ans, 0))

    que = None
    try:
        qlike = question_like.objects.get(question=que_tmp, user=request.user)
        que = QueWithLike(que_tmp, qlike.voice)
    except:
        que = QueWithLike(que_tmp, 0)

    context = {
        "current_page_number": current_page_number,  # paint current page number by black
        "count_of_pages": count_of_pages,  # jump right
        "que": que, # what question?
        "answers": answers,  # all objects on this page
        "link_to_pages_jump_left": link_to_pages_jump_left,  # draw arrow to the left
        "link_to_pages_jump_right": link_to_pages_jump_right,  # -||- right
        "link_to_pages": link_to_pages,  # draw pages num: 2, 3, 4, 5...
        "import_from": "question_single.htm",
        "signup_form": SignupForm(),
        "signin_form": SigninForm(),
        "ask_form": AskForm(),
        "answer_form": AnswerForm(),
        "user": request.user,
        "last_signedup_users": get_last_10_signedup()
    }
    if ready_context is not None:
        context.update(ready_context)

    return render(request, 'main_template.htm', context)


def index(request):
    return main_question(request)


def signup(request):
    if request.method == "GET":
        return main_question(request)

    signup_form = SignupForm(request.POST)
    if signup_form is None or not signup_form.is_valid():
        signup_form.errors.clear()
        return main_question(request, {
            "signup_form": signup_form,
            "overlay": "Signup",
            "signup_error": "One or more fields was input incorrectly"
        })

    if signup_form.data["password"] == "" or signup_form.data["password"] != signup_form.data["confirm_password"]:
        return main_question(request, {
            "signup_form": signup_form,
            "overlay": "Signup",
            "signup_error": "Passwords don't matches"
        })

    user_login = signup_form.data["login"].strip()
    if user_login.count("") < 2:
        return main_question(request, {
            "signup_form": signup_form,
            "overlay": "Signup",
            "signup_error": "Choose another nickname"
        })

    try:
        new_user = User.objects.create_user(user_login, signup_form.data["mail"], signup_form.data["password"])
    except BaseException:
        return main_question(request, {
            "signup_form": signup_form,
            "overlay": "Signup",
            "signup_error": "Choose another nickname"
        })
    new_user = authenticate(username=user_login, password=signup_form.data["password"])

    if new_user is None:
        return main_question(request, {
            "signup_form": signup_form,
            "overlay": "Signup",
            "signup_error": "Try once more"
        })

    login(request, new_user)

    return HttpResponseRedirect("/")


def signin(request):
    if request.method == "GET":
        return main_question(request)

    signin_form = SigninForm(request.POST)
    if signin_form is None:
        return main_question(request, {
            "signin_form": signin_form,
            "overlay": "Signin",
            "signin_error": "Try once more"
        })

    user = authenticate(username=signin_form.data["login"], password=signin_form.data["password"])
    if user is None:
        return main_question(request, {
            "signin_form": signin_form,
            "overlay": "Signin",
            "signin_error": "Bad login or password"
        })

    login(request, user)

    return HttpResponseRedirect("/")


def signout(request):
    logout(request)
    return HttpResponseRedirect("/")


def ask(request):
    if request.method == "GET":
        return main_question(request)

    if not request.user.is_authenticated():
        return main_question(request, {
            "overlay": "Signin",
            "signin_error": "Sign in to add the question"
        })

    ask_form = AskForm(request.POST)
    if ask_form is None:
        return main_question(request, {
            "ask_form": ask_form,
            "overlay": "Ask",
            "ask_error": "Try once more"
        })

    title = ask_form.data["title"].strip()
    text = ask_form.data["text"].strip()
    if title.count("") <= 5 or text.count("") <= 5:
        return main_question(request, {
            "ask_form": ask_form,
            "overlay": "Ask",
            "ask_error": "less than 5 chars were inputed"
        })

    try:
        date = strftime('%Y-%m-%d %H:%M:%S', gmtime())
        new_que = Question.objects.create(title=title, text=text, author=request.user, date=date)
        if new_que is None:
            return main_question(request, {
                "ask_form": ask_form,
                "overlay": "Ask",
                "ask_error": "Try once more"
            })
        # here que had been added
        userrate = None
        try:
            userrate = UserRate.objects.get(user=request.user)
        except:
            userrate = UserRate.objects.create(user=request.user)
        userrate.rate += 1
        userrate.save()
    except:
        return main_question(request, {
            "ask_form": ask_form,
            "overlay": "Ask",
            "ask_error": "Try once more"
        })

    return HttpResponseRedirect("/?sort_by=news")


def question(request):
    return main_answer(request)


def answer(request):
    if request.method == "GET":
        try:
            return HttpResponseRedirect("/question?id=" + request.GET["id"])
        except BaseException:
            HttpResponseRedirect("/")

    if not request.user.is_authenticated():
        return main_question(request, {
            "overlay": "Signin",
            "signin_error": "Sign in to add the question"
        })

    try:
        que = Question.objects.get(id = request.GET["id"])
    except BaseException:
        HttpResponseRedirect("/")

    form = AnswerForm(request.POST)
    form.errors.clear()
    try:
        text = form.data["text"].strip()
        if text.count("") <= 5:
            return main_answer(request, {
                    "answer_form": form,
                    "answer_error": "less than 5 chars were inputed",
                    "anchor": "answer_field"
                })
    except BaseException:
        magic = 5  # another kind of magic. I willn't use this varible

    date = strftime('%Y-%m-%d %H:%M:%S', gmtime())
    try:
        new_ans = Answer.objects.create(text=text, author=request.user, date=date, question=que)
        if new_ans is None:
            return main_answer(request, {
                "answer_form": form,
                "answer_error": "Try once more",
                "anchor": "answer_field"
            })
    except BaseException:
        return main_answer(request, {
            "answer_form": form,
            "answer_error": "Try once more",
            "anchor": "answer_field"
        })

    return HttpResponseRedirect("/question?id=" + str(que.id))


def solved(request):
    try:
        user = request.user
        if not user.is_authenticated():
            HttpResponseRedirect("/")

        que = Question.objects.get(id=request.GET["id"])
        if que.author != user:
            HttpResponseRedirect("/")
        que.solved = 1 - que.solved
        que.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"] + "#que" + str(que.id))
    except BaseException:
        return HttpResponseRedirect("/")


def is_right(request):
    try:
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect("/")

        ans = Answer.objects.get(id=request.GET["id"])
        if ans.question.author != user or ans.author == user:
            return HttpResponseRedirect("/")
        ans.is_right = 1 - ans.is_right
        ans.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"] + "#ans" + str(ans.id))
    except BaseException:
        return HttpResponseRedirect("/")


def qvoice(request):
    try:
        que = Question.objects.get(id=request.GET["id"])
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect(request.META["HTTP_REFERER"] + "#que" + str(que.id))

        delta = 0
        if request.GET["vtype"] == "up":
            delta = 1
        elif request.GET["vtype"] == "down":
            delta = -1
        else:
            return HttpResponseRedirect(request.META["HTTP_REFERER"] + "#que" + str(que.id))

        if que.author == user:
            return HttpResponseRedirect(request.META["HTTP_REFERER"] + "#que" + str(que.id))

        userrate = None
        try:
            userrate = UserRate.objects.get(user=que.author)
        except:
            userrate = UserRate.objects.create(user=que.author)

        try:
            qlike = question_like.objects.get(user=user, question=que)
        except:  # there isn't note in db. create and out
            question_like.objects.create(user=user, question=que, voice=delta)
            que.rate += delta
            que.save()
            userrate.rate += delta > 0 and 3 or -2
            userrate.save()
            return HttpResponseRedirect(request.META["HTTP_REFERER"] + "#que" + str(que.id))

        if qlike.voice != delta:  # for example here was like. It means that user press "dislike" and now voice = 0
            qlike.delete()
            que.rate += delta
            que.save()
            userrate.rate += delta > 0 and 2 or -3  # we want to move "rate" from this voice to 0. If it was +3, we need -3
            userrate.save()

        return HttpResponseRedirect(request.META["HTTP_REFERER"] + "#que" + str(que.id))
    except BaseException:
        return HttpResponseRedirect("/")


def avoice(request):
    try:
        ans = Answer.objects.get(id=request.GET["id"])
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect(request.META["HTTP_REFERER"] + "#ans" + str(ans.id))

        delta = 0
        if request.GET["vtype"] == "up":
            delta = 1
        elif request.GET["vtype"] == "down":
            delta = -1
        else:
            return HttpResponseRedirect(request.META["HTTP_REFERER"] + "#ans" + str(ans.id))

        if ans.author == user:
            return HttpResponseRedirect(request.META["HTTP_REFERER"] + "#ans" + str(ans.id))

        userrate = None
        try:
            userrate = UserRate.objects.get(user=ans.author)
        except:
            userrate = UserRate.objects.create(user=ans.author)

        try:
            alike = answer_like.objects.get(user=user, answer=ans)
        except:  # there isn't note in db. create and out
            answer_like.objects.create(user=user, answer=ans, voice=delta)
            ans.rate += delta
            ans.save()
            userrate.rate += delta > 0 and 5 or -2
            userrate.save()

            return HttpResponseRedirect(request.META["HTTP_REFERER"] + "#ans" + str(ans.id))

        if alike.voice != delta:
            alike.delete()
            ans.rate += delta
            ans.save()
            userrate.rate += delta > 0 and 2 or -5
            userrate.save()

        return HttpResponseRedirect(request.META["HTTP_REFERER"] + "#ans" + str(ans.id))
    except BaseException:
        return HttpResponseRedirect("/")


def userinfo(request):
    try:
        user_about = User.objects.get(id=request.GET["id"])

        userrate = None
        try:
            userrate = UserRate.objects.get(user=user_about)
        except:
            userrate = UserRate.objects.create(user=user_about)

        questions = Question.objects.filter(author=user_about).order_by("-date")
        answers = Answer.objects.filter(author=user_about).order_by("-date")

        return render(request, "main_template.htm", {
            "user": request.user,
            "import_from": "userinfo.htm",
            "user_about": user_about,
            "userrate": userrate.rate,
            "questions": questions,
            "answers": answers,
            "last_signedup_users": get_last_10_signedup(),
            "signup_form": SignupForm(),
            "signin_form": SigninForm(),
            "ask_form": AskForm(),
        })
    except:
        return HttpResponseRedirect("/")


def error404(request):
    return main_question(request, {
        "errcode": 404,
        "errmsg": "Page not found",
        "import_from": "",
        "link_to_pages_jump_left": False,  # not draw arrow to the left
        "link_to_pages_jump_right": False,  # -||- right
        "link_to_pages": ""
    })


# browser -> request -> nginx -> apache2 (match urls.py) -> viewv (db request, gen context, render template) -> return page
