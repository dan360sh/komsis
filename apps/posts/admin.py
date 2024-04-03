from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Category, Post


class CategoryAdmin(DjangoMpttAdmin):
    list_display = ('title','show_index', 'slug', 'parent', 'active')
    prepopulated_fields = {"slug": ("title",)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date', 'active')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('category',)



admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
