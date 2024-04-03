from django.db import models


class HrefModel(models.Model):
    object_path = models.CharField(
        verbose_name="Путь к объекту",
        help_text="путь к объекту(модуль.класс.id)",
        max_length=500,
        unique=True,
        blank=False,
        null=False
    )

    def __str__(self):
        obj = self.get_object()
        if obj:
            return obj.title
        return "Объект не существует"

    def get_object(self):
        try:
            modules = self.get_object_path().split(".")
            id_object = int(modules[-1])
            del modules[-1]
            m = __import__(modules[0])
            del modules[0]
            cl = m
            for m1 in modules:
                cl = getattr(cl, m1)
            return cl.objects.get(id=id_object)
        except:
            return None

    def get_object_path(self):
        if self.object_path:
            return self.object_path
        return ""

    @staticmethod
    def generate_object_path(obj):
        return "{0}.{1}.{2}".format(
            str(obj.__class__.__module__),
            str(obj.__class__.__name__),
            str(obj.id)
        )

    @staticmethod
    def set_object(obj):
        object_path = HrefModel.generate_object_path(obj)
        h = HrefModel(object_path=object_path)
        h1 = HrefModel.objects.filter(object_path=object_path)
        if h1:
            return
        try:
            h.save()
        except:
            pass

    @staticmethod
    def del_by_obj(obj):
        object_path = HrefModel.generate_object_path(obj)
        try:
            HrefModel.objects.get(object_path=object_path).delete()
        except:
            pass

    def get_absolute_url(self):
        obj = self.get_object()
        if obj:
            return obj.get_absolute_url()
        return ""

    class Meta:
        verbose_name = "ссылка на объект"
        verbose_name_plural = "ссылки на объект"
