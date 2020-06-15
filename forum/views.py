from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Post, Comment, PostVotes, PostCommentVotes
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db.models import Q, Sum

@method_decorator(login_required, name='dispatch')  # Protected the class, must be logged in to access.
class ForumListView(SuccessMessageMixin, ListView):
    context_object_name = "objPosts"

    def get(self, request):
        posts = []
        for post in Post.objects.order_by('-created_at').iterator():
            num_comments = len(Comment.objects.filter(forum_id=post.id))
            posts.append({
                "slug": post.slug,
                "title": post.title,
                "user": post.user,
                "created_at": post.created_at,
                "upvotes": get_post_votes(post.id),
                "num_comments": num_comments,
                "views": post.views
            })
        context = {"posts": posts}
        return render(request, "forum/post_list.html", context)

    def post(self, request):
        post_title = request.POST['post_title']
        post_desc = request.POST['post_content']
        new_post = Post(user_id=request.user.id, title=post_title, desc=post_desc, upvotes=0, views=0)
        new_post.save()
        context = {"posts": Post.objects.order_by('-created_at')}
        return render(request, "forum/post_list.html", context)


class ForumCreate(SuccessMessageMixin, CreateView):
    model = Post
    fields = ['title', 'desc']
    success_message = 'Post was successfully created'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ForumUserListView(ListView):
    template_name = 'forum/post_by_user.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])  # checking if the user exists
        return Post.objects.filter(user=self.user)


def get_post_votes(post_id):
    total_votes = PostVotes.objects.filter(post_id=post_id).aggregate(Sum("vote"))["vote__sum"]
    return total_votes if total_votes else 0


def get_comment_votes(comment_id):
    total_votes = PostCommentVotes.objects.filter(comment_id=comment_id).aggregate(Sum("vote"))["vote__sum"]
    return total_votes if total_votes else 0


class ForumDetailView(DetailView):
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_comment'] = CommentForm()
        return context
    '''

    def post(self, request, slug):
        if request.method == "POST":
            pk = request.POST["pk"]
            post_title = request.POST["title"]
            post_content = request.POST["content"]
            post = Post.objects.get(id=pk)
            post.title = post_title
            post.desc = post_content
            post.save()
        return HttpResponse("", content_type="text/plain")

    def get(self, request, slug):
        post = Post.objects.filter(slug=slug)[0]
        post.views += 1
        post.save()
        comments = Comment.objects.filter(forum_id=post.id).order_by("-created_at")
        comments_with_extra_info = []
        for comment in comments.iterator():
            comments_with_extra_info.append({
                "id": comment.id,
                "user": comment.user,
                "desc": comment.desc,
                "created_at": comment.created_at,
                "upvotes": get_comment_votes(comment.id)
            })
        context = {
            "post": post,
            "post_votes": get_post_votes(post.id),
            "comments": comments_with_extra_info
        }
        return render(request, "forum/post_detail.html", context=context)


# for url security:
class OwnerProtectMixin(object):
    def dispatch(self, request, *args, **kwargs):
        objectUser = self.get_object()
        if objectUser.user != self.request.user:
            return HttpResponseForbidden()
        return super(OwnerProtectMixin, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ForumUpdateView(OwnerProtectMixin, UpdateView):
    model = Post
    fields = ['title', 'desc']
    template_name = 'forum/post_update_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('forum-detail', kwargs={'slug': self.object.slug})


@method_decorator(login_required, name='dispatch')
class ForumDeleteView(SuccessMessageMixin, OwnerProtectMixin, DeleteView):
    model = Post
    success_url = '/forum/'
    success_message = 'Post was successfully deleted'


@method_decorator(login_required, name='dispatch')
class CommentCreateView(SuccessMessageMixin, CreateView):
    model = Comment
    fields = ['desc']
    success_message = 'Comment was successfully posted'

    def post(self, request, pk):
        context = {}
        if request.method == "POST":
            comment_content = request.POST["comment_content"]
            comment_content = comment_content.replace("`", "\`")
            post = Post.objects.get(id=pk)
            new_comment = Comment(user_id=request.user.id, forum_id=post.id, desc=comment_content)
            new_comment.save()
            comments = Comment.objects.filter(forum_id=post.id)
            context["post"] = post
            context["comments"] = comments
        return redirect("forum-detail", slug=post.slug)


@method_decorator(login_required, name='dispatch')
class CommentUpdateView(OwnerProtectMixin, UpdateView):
    model = Comment
    fields = ['desc']
    template_name = 'forum/forum_update_comment.html'
    success_url = '/forum/'


@method_decorator(login_required, name='dispatch')
class CommentDeleteView(SuccessMessageMixin, OwnerProtectMixin, DeleteView):
    model = Comment
    success_url = '/forum/'
    success_message = 'Comment was successfully deleted'


def home(request):
    return render(request, "home/forum_page.html")


class VoteRegisterView(CreateView):
    def post(self, request):
        if request.method == "POST":
            if request.POST['is_post'] == 'true':
                post_id = request.POST["id"]
                vote_type = int(request.POST["type"])
                post_vote = PostVotes.objects.filter(user_id=request.user.id, post_id=post_id)
                if post_vote:
                    post_vote[0].vote = vote_type
                    post_vote[0].save()
                else:
                    new_vote = PostVotes(user=request.user, post_id=post_id, vote=vote_type)
                    new_vote.save()
            else:
                comment_id = request.POST["id"]
                vote_type = int(request.POST["type"])
                comment_vote = PostCommentVotes.objects.filter(user_id=request.user.id, comment_id=comment_id)
                if comment_vote:
                    comment_vote[0].vote = vote_type
                    comment_vote[0].save()
                else:
                    new_vote = PostCommentVotes(user=request.user, comment_id=comment_id, vote=vote_type)
                    new_vote.save()
        return HttpResponse("", content_type="text/plain")


class SaveCommentView(UpdateView):
    def post(self, request):
        if request.method == "POST":
            comment_id = request.POST["id"]
            new_content = request.POST["content"]
            sub_comment = Comment.objects.get(id=comment_id)
            sub_comment.desc = new_content
            sub_comment.save()
        return HttpResponse("", content_type="text/plain")


class DeleteCommentView(DeleteView):
    def post(self, request):
        if request.method == "POST":
            comment_id = request.POST["id"]
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
        return HttpResponse("", content_type="text/plain")