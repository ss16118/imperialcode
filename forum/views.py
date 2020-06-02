from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Post
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch') # Protected the class, must be logged in to access.
class ForumCreate(CreateView):
    model = Post
    fields = ['title', 'desc']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def home(request):
    return render(request, "home/forum_page.html")


