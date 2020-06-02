from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [   
                  url(r'^sign_up/',views.sign_up),
                  url(r'^landing_page', views.landing),
                  url(r'^all_problems_page', views.all_problems_page),
                  url(r'^forum_page', views.forum_page),
                  url(r'^index', views.index),
                  url(r'^past_papers_page/(.*)', views.past_papers_page),
                  url(r'^past_papers_page', views.past_papers_page),
                  url(r'^problem_creation_page', views.problem_creation_page),
                  url(r'^question_comment_page', views.question_comment_page),
                  url(r'^question_solving_page', views.question_solving_page),
                  url(r'^signup_page', views.signup_page),
                  url(r'^single_post_page', views.single_post_page),
                  url(r'^user_info_page', views.user_info_page),
                  url(r'^start', views.start),
                  url(r'^start_c_1', views.start_c_1),
                  url(r'^start_with_pages', views.start_with_pages),
                  url(r'^expand', views.expand),
                  url(r'^Other', views.Other),
                  url(r'^reload', views.reload),
                  url(r'^$', views.landing),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'home.views.page_not_found_view'
handler500 = 'home.views.server_error_view'
