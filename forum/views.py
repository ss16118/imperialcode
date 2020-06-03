from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch') # Protected the class, must be logged in to access.
class ForumListView(ListView):
    model = Post
    context_object_name = "objPosts"
    queryset = Post.objects.order_by('-created_at') # order by creation date

class ForumCreate(CreateView):
    model = Post
    fields = ['title', 'desc']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ForumUserListView(ListView):
    template_name = 'forum/post_by_user.html'
    def get_queryset(self):
        self.user = get_object_or_404(User, username = self.kwargs['username']) # checking if the user exists
        return Post.objects.filter(user = self.user)

class ForumDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['additional'] = 'ImperialCode® 2020'
        return context


# for url security:
class OwnerProtectMixin(object):
    def dispatch(self, request, *args, **kwargs):
        objectUser = self.get_object()
        if objectUser.user != self.request.user:
            return HttpResponseForbidden()
        return super(OwnerProtectMixin, self).dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ForumUpdateView(OwnerProtectMixin ,UpdateView):
    model = Post
    fields = ['title', 'desc']
    template_name = 'forum/post_update_form.html'

@method_decorator(login_required, name='dispatch')
class ForumDeleteView(OwnerProtectMixin, DeleteView):
    model = Post
    success_url = '/forum'


def home(request):
    return render(request, "home/forum_page.html")


