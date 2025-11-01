from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import HttpResponse
from django.shortcuts  import render


# fbv for templateview

def indexview(request):
    """
    a function based view to show index page
    """
    name = 'paisa'
    context = {'name':name}
    return render (request,'index.html',context)



class IndexView(TemplateView):
    """
    class based view to show index page
    """

    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "paisa"
        context["post"] = Post.objects.all()
        return context


# fbv for redirectview
"""
def redirecttomaktab(request):
    return redirect("https://maktabkhooneh.org/")
"""


class Redirecttomaktab(RedirectView):
    url = "https://maktabkhooneh.org/"

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        print(post)
        return super().get_redirect_url(*args, **kwargs)


class PostListView(LoginRequiredMixin, ListView):
    # model = Post (
    queryset = Post.objects.all()
    context_object_name = "posts"  # this converts(object_list in templates) to what name we want
    paginate_by = 2
    ordering = "-id"
    # def get_queryset(self): #its work just like model and queryset. its for getting data
    #     posts = Post.objects.filter(status=True)
    #     return posts


class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post


# class PostCreateView(FormView):
#     template_name = 'contact.html'
#     form_class = PostForm
#     success_url = '/blog/post/'

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title','content','category','status','published_date','author']
    success_url = "/blog/post/"
    form_class = (
        PostForm  # we can use formclass instead of fields and vise versa
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post/"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/blog/post/"
