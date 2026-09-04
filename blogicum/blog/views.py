from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Post, Category


POST_LIMIT = 5


def get_base_query_set():
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def index(request):
    template = 'blog/index.html'
    posts = get_base_query_set()[:POST_LIMIT]
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        get_base_query_set(),
        pk=id
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )
    posts = get_base_query_set().filter(category=category)
    context = {
        'category': category,
        'post_list': posts
    }
    return render(request, template, context)
