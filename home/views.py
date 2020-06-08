from django.shortcuts import render, redirect
import logging
from django.contrib.auth import authenticate, login as loginuser
from django.contrib.auth.models import User as Authuser
from home.models import Problem, Question, CodeSegment, UserProgress, QuestionComment
from django.contrib.auth.decorators import login_required
from home.codeCache import CodeCache
import requests
from django.http import HttpResponse
from django.db.models import Q
import re

# logger = logging.getLogger(__name__)
# logging.basicConfig(filename="logs/imperialcode_debug.log", level=logging.DEBUG)


code_cache = CodeCache()


def landing(request):
    if request.user.is_authenticated:
        return redirect("../index")
    if request.method == "POST":
        uname = request.POST['u4_input']
        pw = request.POST['u5_input']
        user = authenticate(username=uname, password=pw)
        if user is not None:
            loginuser(request, user)
            return redirect("../index")
    return render(request, "home/landing_page.html")


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("../index")
    if request.method == "POST":
        uname = request.POST["username"]
        pw = request.POST["password"]
        cpw = request.POST["confirmpassword"]
        if pw != cpw:
            message = "inconsistent password"
        try:
            user = Authuser.objects.create_user(uname, password=pw)
            user.save()
            return redirect("/")
        except:
            message = "invalid"
    else:
        message = ""
    context = {"msg": message}
    return render(request, "home/signup_page.html", context)


@login_required
def all_problems_page(request):
    return render(request, "home/all_problems_page.html")


@login_required
def forum_page(request):
    return render(request, "home/forum_page.html")


@login_required
def index(request):
    return render(request, "home/index.html")


def past_papers_page(request):
    results = Problem.objects.all()
    if request.GET.get("keywords") is not None:
        kw = request.GET.get("keywords")
        results = results.filter(Q(title__contains=kw) | Q(desc__contains=kw))
        if kw.isdigit():
            results = results.filter(id=kw)
    if request.GET.get("lang") is not None:
        results = results.filter(language=request.GET.get("lang"))
    if request.GET.get("year") is not None:
        results = results.filter(year=request.GET.get("year"))
    if request.GET.get("diff") is not None:
        results = results.filter(difficulty=request.GET.get("diff"))
    if request.GET.get("status") is not None:
        results = results.filter(status=request.GET.get("status"))
    selected_title = request.GET.get("p") if request.GET.get("p") is not None else ""
    selected_paper = Problem.objects.filter(title=selected_title)
    user_progress = UserProgress.objects.filter(user_id=request.user.id, problem__title=selected_title)
    num_subquestions = len(Question.objects.filter(problem__title=selected_title))
    selected_paper_info = {}
    if len(selected_paper) == 0:
        selected_paper_info["title"] = ""
        selected_paper_info["desc"] = ""
        selected_paper_info["year"] = 0
        selected_paper_info["status"] = ""
        selected_paper_info["difficulty"] = 0
        selected_paper_info["upvotes"] = 0
        selected_paper_info["progress"] = 0
    else:
        selected_paper_info["title"] = selected_paper[0].title
        selected_paper_info["desc"] = selected_paper[0].desc
        selected_paper_info["year"] = selected_paper[0].year
        selected_paper_info["status"] = ""
        selected_paper_info["difficulty"] = selected_paper[0].difficulty
        selected_paper_info["upvotes"] = selected_paper[0].upvotes
        selected_paper_info["progress"] = round((len(user_progress[0].progress) / num_subquestions) * 100, 2) \
            if user_progress else 0

    selected_paper_info["difficulty"] = "★" * selected_paper_info["difficulty"]
    context = {"display_papers": results, "selected_paper": selected_paper_info}
    return render(request, "home/past_papers_page.html", context)


@login_required
def problem_creation_page(request):
    context = {}
    return render(request, "home/problem_creation_page.html", context)


@login_required
def question_comment_page(request):
    # if request.method == "POST":
    #     pname = request.POST["papername"]
    #     qindex = int(request.POST["question_index"])
    # else:
    pname = request.GET.get("papername")
    qindex = int(request.GET.get("question_index"))
    qname = pname + " question " + str(qindex)
    question = Question.objects.filter(question_index= qindex, problem__title= pname)[0]
    question_id = question.id
    if request.method == "POST":
        comment_title = request.POST["post_title"]
        content = request.POST["post_content"]
        comment = QuestionComment(question = question, parent_comment= None, user = request.user,
             title= comment_title, desc = content)
        comment.save()
    comments = QuestionComment.objects.filter(question = question_id)
    context = {"qname":qname, "posts": comments, "pname":pname, "qindex" : qindex}

    return render(request, "home/question_comment_page.html", context)


@login_required
def past_paper_update_progress(request):
    if request.method == "POST":
        q_index = int(request.POST.get("index"))
        pname = request.POST.get("pname")
        progress = UserProgress.objects.filter(problem__title=pname, user_id=request.user.id)
        if progress:
            user_progress = progress[0]
            completed_questions = user_progress.progress
            if q_index not in completed_questions:
                completed_questions.append(q_index)
                user_progress.progress = completed_questions
                user_progress.save()
        else:
            problem_id = Problem.objects.filter(title=pname)[0].id
            new_progress = UserProgress(user_id=request.user.id, problem_id=problem_id, stopped_at=0, progress=[q_index])
            new_progress.save()

    return HttpResponse("", content_type="text/plain")


@login_required
def save_code(request):
    if request.method == "POST":
        pname = request.POST.get("pname")
        q_index = int(request.POST.get("index"))
        code = request.POST.get("code")
        code_cache.add(pname, q_index, request.user.id, code)
    return HttpResponse("", content_type="text/plain")


@login_required
def record_current_question(request):
    if request.method == "POST":
        pname = request.POST.get("pname")
        index = int(request.POST.get("index"))
        progress = UserProgress.objects.filter(problem__title=pname, user_id=request.user.id)
        print("Stopped at question {} for paper {}".format(index, pname))
        if progress:
            user_progress = progress[0]
            user_progress.stopped_at = index
            user_progress.save()
        else:
            problem_id = Problem.objects.filter(title=pname)[0].id
            new_progress = UserProgress(user_id=request.user.id, problem_id=problem_id, stopped_at=index, progress=[])
            new_progress.save()
    return HttpResponse("", content_type="text/plain")


@login_required
def run_code(request):
    output = ""
    if request.method == "POST":
        all_code = request.POST.get("code", "")
        response = requests.post('https://api.jdoodle.com/v1/execute',
                                 json={'clientId': "e3762b799cdb4c3ee07e092f6041ce08",
                                       'clientSecret': '123904cc5aa37569cb7fecc393154e7e4d9d3375d08932ef4f7109affd2dda6b',
                                       'script': all_code,
                                       'stdin': "",
                                       'language': "haskell",
                                       'versionIndex': '0'})
        try:
            # try except is used because the external api may not be reliable
            output = response.json()["output"]
            output = re.sub('\( jdoodle.hs, jdoodle.o \)', '', output)
            output = re.sub('Linking jdoodle ...', '', output)
        except:
            pass
    return HttpResponse(output, content_type="text/plain")


@login_required
def question_solving_page(request):
    pname = request.GET.get("papername")
    paper = Problem.objects.filter(title=pname)[0]

    questions = Question.objects.filter(problem__title=pname).order_by("question_index")
    code_segments_stored = CodeSegment.objects.filter(problem__title=pname).order_by("index")
    code_segments = []
    progress = UserProgress.objects.filter(problem__title=pname, user_id=request.user.id)
    for i in range(len(code_segments_stored)):
        cached_segment = code_cache.get(pname, code_segments_stored[i].index, request.user.id)
        if cached_segment is not None:
            code_segments.append(cached_segment)
        else:
            code_segments.append(code_segments_stored[i].code)
    questions_clean = []
    for question in questions:
        questions_clean.append({
            "desc": question.question_desc,
            "test_script": question.test_script.replace("\\", "\\\\").replace("`", "\`")
        })
    code_segments_clean = []
    for code_segment in code_segments:
        code_segments_clean.append(code_segment.replace("\\", "\\\\").replace("`", "\`"))
    context = {"paper": paper, "questions": questions_clean, "code_segments": code_segments_clean,
               "stopped_at": progress[0].stopped_at if progress else 0}
    return render(request, "home/question_solving_page.html", context)


def comment_detail(request):
    comment_id = int(request.GET.get("id"))
    return HttpResponse(comment_id)


def signup_page(request):
    return render(request, "home/signup_page.html")


@login_required
def single_post_page(request):
    return render(request, "home/single_post_page.html")


@login_required
def user_info_page(request):
    return render(request, "home/user_info_page.html")


def start(request):
    return render(request, "home/start.html")


def start_c_1(request):
    return render(request, "home/start_c_1.html")


@login_required
def start_with_pages(request):
    return render(request, "home/start_with_pages.html")


def expand(request):
    return render(request, "home/expand.html")


def Other(request):
    return render(request, "home/Other.html")


def reload(request):
    return render(request, "home/reload.html")


def page_not_found_view(request, *args, **kwargs):
    response = render(request, "home/404.html")
    response.status_code = 404
    return response


def server_error_view(request, *args, **kwargs):
    response = render(request, "home/404.html")
    response.status_code = 500
    return response
