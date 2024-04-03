from django.views.generic.detail import DetailView

from .models import Category, Post


class CategoryView(DetailView):
    model = Category
    template_name = 'posts/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category = context['object']
        context['posts'] = Post.objects.filter(category=category, active=True)
        return context


class PostView(DetailView):
    model = Post
    template_name = 'posts/post.html'
    context_object_name = 'post'
