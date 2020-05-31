from django.shortcuts import render
from django.conf import settings
import logging

if settings.DEBUG:
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="logs/imperialcode_debug.log", level=logging.DEBUG)


def landing(request):
    return render(request, "home/landing_page.html")


def all_problems_page(request):
    return render(request, "home/all_problems_page.html")


def forum_page(request):
    return render(request, "home/forum_page.html")


def index(request):
    return render(request, "home/index.html")


def past_papers_page(request):
    return render(request, "home/past_papers_page.html")


def problem_creation_page(request):
    return render(request, "home/problem_creation_page.html")


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
