from re import L, template
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from flask import request_started
from .models import Post, Tag
from django.views.generic import View
from .utils import *
from .forms import TagForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin # Класс-миксин, ограничивающий пользователю отображение определенных классов
from django.core.paginator import Paginator

from django.db.models import Q
# Посты - CRUD

def post_list(request):
    search_query = request.GET.get('search', '') # Поиск на сайте

    if search_query:
        posts = Post.objects.filter(Q(title__icontains = search_query) | Q(body__icontains = search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 7) # Пагинатор для номера страницы

    page_number = request.GET.get('page', 1);
    page = paginator.get_page(page_number) # Текущий номер страницы

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url=''
    
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, 'blog/index.html', context = context)

class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'

class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True

class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True

class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'post_list_url'
    raise_exception = True

# Теги - CRUD

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})

class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'

class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True

class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True

class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True

    '''
    # TagDelete
    def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact = slug)
        return render(request, 'blog/tag_delete_form.html', context={'tag':tag})
    
    def post(self, request, slug):
        tag = Tag.objects.get(slug__iexact = slug)
        tag.delete()
        return redirect(reverse('tags_list_url'))'''
    
    
    '''def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        bound_form = TagForm(instance=tag)
        return render(request, 'blog/tag_update_form.html', context={'form':bound_form, 'tag': tag})

    def post(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        bound_form = TagForm(request.POST, instance=tag)

        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        return render(request, 'blog/tag_update_form', context={'form': bound_form, 'tag': tag})

    def get(self, request):
        form = TagForm()
        return render(request, 'blog/tag_create.html', context={'form': form})
    
    def post(self, request):
        bound_form = TagForm(request.POST)

        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)    # Вывод результата. redirect - принимает url-шаблон
        return render(request, 'blog/tag_create.html', context={'form': bound_form})

    # PostCreate   
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/post_create_form.html', context={'form': form})

    def post(self, request):
        bound_form = PostForm(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, 'blog/post_create_form.html', context={'form': bound_form})
        '''