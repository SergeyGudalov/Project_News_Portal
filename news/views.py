from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .filters import PostFilter

from django import forms

from .forms import PostForm
from .models import Post


class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(post_type='NW').order_by('-created_at')
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='NW').order_by('-created_at')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    queryset = Post.objects.filter(post_type='NW')
    template_name = 'new.html'
    context_object_name = 'new'


# Создание общих классов создания, редактирования и удаления

class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = self.post_type
        return super().form_valid(form)

class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def get_queryset(self):
        return Post.objects.filter(post_type=self.post_type)

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'

    def get_queryset(self):
        return Post.objects.filter(post_type=self.post_type)

# Создание представлений для новостей

class NewsCreate(PostCreate):
    post_type = 'NW'
    success_url = reverse_lazy('news_list')

class NewsUpdate(PostUpdate):
    post_type = 'NW'
    success_url = reverse_lazy('news_list')

class NewsDelete(PostDelete):
    post_type = 'NW'
    success_url = reverse_lazy('news_list')

# Создание представлений для статей

class ArticleCreate(PostCreate):
    post_type = 'AR'
    success_url = reverse_lazy('article_list')

class ArticleUpdate(PostUpdate):
    post_type = 'AR'
    success_url = reverse_lazy('article_list')

class ArticleDelete(PostDelete):
    post_type = 'AR'
    success_url = reverse_lazy('article_list')