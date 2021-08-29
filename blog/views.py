from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from blog.forms import ArticleForm, CommentForm
from blog.models import Article, Category, Comment
from blog.utils import create_comments_tree


@login_required(login_url='login')
def home(request):
    articles = Article.objects.all()
    return render(request, 'blog/home.html', {'articles': articles})


def index(request):
    return redirect('blog:home')


@login_required(login_url='login')
def profile(request):
    articles = Article.objects.filter(user=request.user).order_by('id')
    return render(request, 'blog/profile.html', {'articles': articles})


@login_required(login_url='login')
def football(requrest):
    category = Category.objects.get(title='Футбол')
    articles = Article.objects.filter(category=category).order_by('id')
    return render(requrest, 'blog/football.html', {'articles': articles})


@login_required(login_url='login')
def judo(request):
    category = Category.objects.get(title='Дзюдо')
    articles = Article.objects.filter(category=category).order_by('id')
    return render(request, 'blog/judo.html', {'articles': articles})


@login_required(login_url='login')
def box(request):
    category = Category.objects.get(title='Бокс')
    articles = Article.objects.filter(category=category).order_by('id')
    return render(request, 'blog/box.html', {'articles': articles})


@login_required(login_url='login')
def basketball(request):
    category = Category.objects.get(title='Баскетбол')
    articles = Article.objects.filter(category=category).order_by('id')
    return render(request, 'blog/basketball.html', {'articles': articles})


def detail_delete(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, 'blog/detail_delete.html', {'object': article})


# class ArticleDetailView(DetailView):
#     queryset = Article.objects.all()
#     template_name = 'blog/detail.html'
def detail(request, article_id):
    object = Article.objects.get(id=article_id)
    comments = Article.objects.get(id=article_id).comments.all()
    result = create_comments_tree(comments)
    comment_form = CommentForm(request.POST or None)
    return render(request, 'blog/detail.html', {'comments': result,
                                                'comment_form': comment_form,
                                                'object': object,
                                                'article_id':article_id})


class ArticleCreateView(CreateView):
    model = Article
    # title = forms.CharField(label='Название', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Введите название статьи'}))
    # description = forms.CharField(label='Статья', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Напишите статью'}))
    form_class = ArticleForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/update.html'
    success_url = reverse_lazy('blog:home')


class ArticleDeleteView(DeleteView):
    model = Article
    # template_name = 'cities/delete.html'
    success_url = reverse_lazy('blog:home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def create_comment(request, article_id):
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.user = request.user
        new_comment.text = comment_form.cleaned_data['text']
        new_comment.content_type = ContentType.objects.get(model='article')
        new_comment.object_id = Article.objects.get(id=article_id)
        new_comment.parent = None
        new_comment.is_child = False
        new_comment.save()
    url = reverse('blog:detail',args=[article_id])
    return HttpResponseRedirect(url)


@transaction.atomic
def create_child_comment(request,article_id):
    user_name = request.POST.get('user')
    current_id = request.POST.get('id')
    text = request.POST.get('text')
    user = User.objects.get(username=user_name)
    content_type = ContentType.objects.get(model='article')
    parent = Comment.objects.get(id=int(current_id))
    is_child = False if not parent else True
    Comment.objects.create(
        user=user,
        text=text,
        content_type=content_type,
        object_id=Article.objects.get(id=article_id),
        parent=parent,
        is_child=is_child
    )
    comments_ = Article.objects.get(id=article_id).comments.all()
    comments_list = create_comments_tree(comments_)
    url = reverse('blog:detail', args=[article_id])
    return HttpResponseRedirect(url)
    # return render(request, 'blog/detail.html', {'comments': comments_list})
