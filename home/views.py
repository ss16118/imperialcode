from django.shortcuts import render, redirect
import logging
from django.contrib.auth import authenticate, login as loginuser
from django.contrib.auth.models import User as Authuser
from home.models import PastPaper, Question, Code_Segment
from django.contrib.auth.decorators import login_required
from home.codeCache import CodeCache
import requests

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
    papername = request.GET.get("p")
    paper_titles = [p.title for p in PastPaper.objects.all()]
    choosen_paper = PastPaper.objects.filter(title=papername)
    if len(choosen_paper) == 0:
        title = ""
        description = ""
        year = 0
        difficulty = 0
        upvotes = 0
    else:
        paper = choosen_paper[0]
        title = paper.title
        description = paper.desc
        year = paper.year
        difficulty = paper.difficulty
        upvotes = paper.upvotes
    context = {"paper_titles": paper_titles, "title": title, "description": description, "year": year,
               "difficulty": difficulty, "upvotes": upvotes}
    return render(request, "home/past_papers_page.html", context)

@login_required
def problem_creation_page(request):
    context = {}
    return render(request, "home/problem_creation_page.html", context)

@login_required
def question_comment_page(request):
    return render(request, "home/question_comment_page.html")

@login_required
def question_solving_page(request):
    pname = request.GET.get("p")
    qindex = request.GET.get("i")
    answer = request.GET.get("code")
    question = Question.objects.filter(paper__title=pname).filter(question_index = qindex)
    if len(question) == 0:
        desc = ""
        code = ""
        output = ""
    else:
        desc = question[0].question_desc
        code = Code_Segment.objects.filter(id=question[0].code_segment)[0]
        output = ""
        if answer != None:
            code_segments = Code_Segment.objects.filter(paper__title=pname).order_by('index')
            code_cache.add(pname, qindex, request.user.id, answer)
            all_code = ""
            for i in range (len(code_segments)):
                cached_segment = code_cache.get(pname, qindex,request.user.id)
                if cached_segment is not None:
                    all_code += cached_segment
                    cached_segment = None
                else:
                    all_code += code_segments[i].code
            all_code += question[0].test_script
            response = requests.post('https://api.jdoodle.com/v1/execute',
             json={'clientId': "e3762b799cdb4c3ee07e092f6041ce08",
             'clientSecret': '123904cc5aa37569cb7fecc393154e7e4d9d3375d08932ef4f7109affd2dda6b',
             'script': all_code,
             'stdin': "",
             'language':"haskell",
             'versionIndex':'0'})
            try:
                #try except is used because the external api may not be reliable
                output = response.json()["output"]
            except:
                pass

    context = {"desc":desc,"code":code, "output":output}
    return render(request, "home/question_solving_page.html",context)


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
