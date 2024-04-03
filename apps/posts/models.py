from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey

from apps.configuration.utils import HrefModel, unique_slugify
from apps.content.models import Content
from apps.shop.models.order import on_order_change


class Category(MPTTModel):
    active = models.BooleanField(verbose_name='Активность', default=True)
    show_index = models.BooleanField(verbose_name='Вывести на главную', default=False,
                                     help_text="Если указано несколько,\
                               выводится самая первая")
    parent = TreeForeignKey('self', verbose_name="Родительская категория",
                            related_name='childs', blank=True, null=True,
                            on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок',
                             blank=False, max_length=200)
    slug = models.SlugField(verbose_name='Слаг', blank=False,
                            null=True, unique=True, max_length=100)
    thumbnail = FilerImageField(verbose_name="Миниатюра",
                                null=True, blank=True, on_delete=models.SET_NULL)
    description = RichTextUploadingField(verbose_name='Описание',
                                         blank=True, default='')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self.title, Category)
        super(Category, self).save(*args, **kwargs)
        HrefModel.set_object(self)

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def get_last_posts(self):
        return self.posts.filter(active=True).order_by("-published_date")

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    active = models.BooleanField(verbose_name='Активность', default=True)
    title = models.CharField(verbose_name='Заголовок',
                             blank=False, max_length=200)
    slug = models.SlugField(verbose_name='URL', blank=False,
                            null=True, unique=True, max_length=100)
    description = models.TextField(verbose_name='Краткое описание',
                                   blank=True, null=False)
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 related_name='posts', blank=True, null=True, on_delete=models.SET_NULL,)
    published_date = models.DateTimeField(verbose_name='Дата публикации',
                                          default=timezone.now, blank=False)
    end_date = models.DateTimeField(verbose_name="Дата удаления публикации",
                                    null=True, blank=True)
    thumbnail = FilerImageField(verbose_name="Миниатюра",
                                null=True, blank=True, on_delete=models.SET_NULL)
    content = models.ForeignKey(Content, verbose_name="Контент", blank=True,
                                null=True, related_name="content_posts", on_delete=models.SET_NULL)
    primary_link = models.TextField(verbose_name="Ссылка", blank=True,
                                    null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self.title, Post)
        super(Post, self).save(*args, **kwargs)
        HrefModel.set_object(self)

    def get_absolute_url(self):
        if self.primary_link:
            return self.primary_link
        return reverse('post', kwargs={
            'category_slug': self.category.slug,
            'slug': self.slug})

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'Записи'
        ordering = ['-published_date']
