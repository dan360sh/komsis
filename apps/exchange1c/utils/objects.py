from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet

class SubclassingQuerySet(QuerySet):
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model):
            return result.as_leaf_class()
        return result

    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()

class HrefManager(models.Manager):
    def get_queryset(self):
        return SubclassingQuerySet(self.model)


class HrefModelBase(models.Model,):
    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    objects = HrefManager()

    def __str__(self):
        content_type = self.content_type
        model = content_type.model_class()
        return "{} - {}".format(model._meta.verbose_name, model.objects.get(id=self.id).title)

    def get_absolute_url(self):
        try:
            return self.as_leaf_class().get_absolute_url()
        except AttributeError:
            raise NotImplementedError("Класс {} не реализует метод get_absolute_url".format(self.__class__.__name__))

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(HrefModelBase, self).save(*args, **kwargs)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if model == HrefModelBase:
            return self
        return model.objects.get(id=self.id)
