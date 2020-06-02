from django.shortcuts import render, redirect
import logging
from django.contrib.auth import authenticate,login as loginuser
from django.contrib.auth.models import User as Authuser
from home.models import Forum, Comment, PastPaper, Question



# logger = logging.getLogger(__name__)
# logging.basicConfig(filename="logs/imperialcode_debug.log", level=logging.DEBUG)


def landing(request):
    if request.user.is_authenticated:
        return redirect("../index")
    if request.method == "POST":
        uname = request.POST['u4_input']
        pw = request.POST['u5_input']
        user = authenticate (username=uname,password=pw)
        if user is not None:
            loginuser(request,user)
            return redirect("../index")
    return render(request, "home/landing_page.html")

def sign_up(request):
    if request.user.is_authenticated:
        return redirect("../index")
    if request.method == "POST":
        uname = request.POST ["username"]
        pw = request.POST ["password"]
        cpw = request.POST ["confirmpassword"]
        if pw != cpw:
            message = "inconsistent password"
        try:
            user=Authuser.objects.create_user(uname,password=pw)
            user.save()
            return redirect("/")
        except:
            message = "invalid"
    else:
        message = ""
    context={"msg":message}
    return render(request, "home/signup_page.html",context)


def all_problems_page(request):    
    return render(request, "home/all_problems_page.html")


def forum_page(request):
    return render(request, "home/forum_page.html")


def index(request):
    return render(request, "home/index.html")

def past_papers_page(request, papername = ""):
    paper_titles = [p.title for p in PastPaper.objects.all()]
    choosen_paper = PastPaper.objects.filter(title = papername)
    if len(choosen_paper) == 0:
        title = ""
        description = ""
        year = 0
        difficulty = 0
        upvotes = 0
    else :
        paper = choosen_paper[0]
        title = paper.title
        description = paper.desc
        year = paper.year
        difficulty = paper.difficulty
        upvotes = paper.upvotes
    context = {"paper_titles":paper_titles, "title":title, "description": description, "year": year,  "difficulty": difficulty, "upvotes":upvotes}
    return render(request, "home/past_papers_page.html", context)

def problem_creation_page(request):
    context = {"paper_titles":paper_titles, "title":"", "description": "", "year": "", "difficulty": "", "upvotes":""}
    return render(request, "home/problem_creation_page.html", context)


def question_comment_page(request):
    return render(request, "home/question_comment_page.html")


def question_solving_page(request):
    return render(request, "home/question_solving_page.html")


def signup_page(request):
    return render(request, "home/signup_page.html")


def single_post_page(request):
    return render(request, "home/single_post_page.html")


def user_info_page(request):
    return render(request, "home/user_info_page.html")


def start(request):
    return render(request, "home/start.html")


def start_c_1(request):
    return render(request, "home/start_c_1.html")


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
