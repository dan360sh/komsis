import re

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.template.loader import get_template
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField


class Content(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=300)

    def __str__(self):
        return "Контент: " + self.title

    def get_list_content(self):
        """Сортировка объектов контента.

        В список `content` требуется добавлять все объекты через
        `related_name` блоков(классов) контента.

        Returns:
            `list` -- Отсортированый список блоков(объектов) контента
                относительно поля `sort`
        """

        content = []
        content += list(self.content_texts.all())
        content += list(self.content_quotes.all())
        content += list(self.content_files.all())
        content += list(self.content_title_underline.all())
        content += list(self.content_certificates.all())
        content += list(self.content_gallery.all())
        content += list(self.content_typal_block.all())
        content += list(self.content_collapser.all())
        content.sort(key=self.order_by)
        return content

    def render(self):
        template = get_template("content/base.html")
        return template.render({"content": self.get_list_content()})

    def order_by(self, value):
        return value.sort * (+1)

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"


class Text(models.Model):
    content = models.ForeignKey(
        Content, related_name="content_texts", on_delete=models.CASCADE)
    text = RichTextUploadingField(verbose_name="Текст", null=False,
                                  blank=False, default="")
    sort = models.IntegerField(verbose_name="Сортировка", default=1)

    def __str__(self):
        return "Текстовый блок № " + str(self.id)

    def render(self):
        template = get_template("content/text.html")
        return template.render({"text": self.text})

    class Meta:
        verbose_name = "текст"
        verbose_name_plural = "Тексты"
        ordering = ["sort"]


class Quote(models.Model):
    content = models.ForeignKey(
        Content, related_name="content_quotes", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Цитата", default="")
    sort = models.IntegerField(verbose_name="Сортировка", default=1)

    def render(self):
        return get_template("content/quote.html").render({"quote": self.text})

    def __str__(self):
        return "Цитата № " + str(self.id)

    class Meta:
        verbose_name = "цитата"
        verbose_name_plural = "цитаты"


class FileBlock(models.Model):
    title = models.CharField(verbose_name="Подпись",
                             blank=True, null=True, max_length=300)

    def __str__(self):
        return "Блок с файлами № " + str(self.id)

    class Meta:
        verbose_name = "блок с файлами"
        verbose_name_plural = "Блоки с файлами"


class File(models.Model):
    block = models.ForeignKey(
        FileBlock, verbose_name="Блок файлов", related_name="file_items", on_delete=models.CASCADE)
    obj = FilerFileField(verbose_name="файл",
                         related_name="file_objects", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Подпись",
                             default="Подпись", max_length=300)

    def __str__(self):
        return "Файл " + str(self.id)

    def get_type(self):
        try:
            return re.search(
                r"\.(.+?)$", self.obj.original_filename).group(1)
        except AttributeError:
            return "File"

    def get_size(self):
        """Получить размер файла поля `obj`.

        Returns:
            `string` -- Размер файла формата: число и единица измерения
        """

        size = self.obj._file_size
        sizes = [" Б", " Кб", " Мб"]
        size_label = sizes[0]
        if size < 100:
            return str(round(size, 2)) + size_label
        size_label = sizes[1]
        size = size / 1024
        if size < 100:
            return str(round(size, 2)) + size_label
        size_label = sizes[2]
        size = size / 1024
        return str(round(size, 2)) + size_label

    class Meta:
        verbose_name = "файл"
        verbose_name_plural = "файлы"


class Files(models.Model):
    content = models.ForeignKey(
        Content, related_name="content_files", on_delete=models.CASCADE,)
    block = models.OneToOneField(
        FileBlock, verbose_name="Блок файлов", on_delete=models.CASCADE)
    sort = models.IntegerField(verbose_name="Сортировка", default=1)

    def __str__(self):
        return ""

    def render(self):
        template = get_template("content/files.html")
        files = self.block.file_items.all()
        return template.render({"files": files})

    class Meta:
        verbose_name = "файлы"
        verbose_name_plural = "Файлы"


class TitleUnderline(models.Model):
    content = models.ForeignKey(
        Content, related_name="content_title_underline", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст", default="")
    sort = models.IntegerField(verbose_name="Сортировка", default=1)

    def render(self):
        return get_template("content/title-underline.html").render(
            {"text": self.text})

    def __str__(self):
        return "Подзаголовок с подчеркиванием № " + str(self.id)

    class Meta:
        verbose_name = "подзаголовок с подчеркиванием"
        verbose_name_plural = "ползаголовки с подчеркиванием"


class CertificatesBlock(models.Model):
    title = models.CharField(verbose_name="Заголовок",
                             blank=True, null=True, max_length=300)

    def __str__(self):
        if self.title:
            return self.title
        return "Блок с сертификатами " + str(self.id)

    class Meta:
        verbose_name = "блок сертификатов"
        verbose_name_plural = "блоки сертификатов"


class Certificate(models.Model):
    block = models.ForeignKey(
        CertificatesBlock, related_name="certificate_items", on_delete=models.CASCADE)
    image = FilerImageField(verbose_name="Изображение",
                            related_name="certificate_images", on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "сертификат"
        verbose_name_plural = "сертификаты"


class Certificates(models.Model):
    content = models.ForeignKey(
        Content, related_name="content_certificates", on_delete=models.CASCADE)
    block = models.OneToOneField(
        CertificatesBlock, verbose_name="Блок сертификатов", on_delete=models.CASCADE)
    sort = models.IntegerField(verbose_name="Сортировка", default=1)

    def __str__(self):
        return "Сертификаты № " + str(self.id)

    def render(self):
        return get_template("content/certificates.html").render(
            {"certificates": self.block.certificate_items.all()})

    class Meta:
        verbose_name = "сертификаты"
        verbose_name_plural = "Сертификаты"


# Количество элементов в ряду
NUMBER_IN_ROW = (
    (6, "Два"),
    (4, "Три"),
    (3, "Четыре")
)


class GalleryBlock(models.Model):
    """ Модель блока в галереи"""

    title = models.CharField(verbose_name="Заголовок",
                             blank=True, null=True, max_length=300)
    type_show = models.IntegerField(verbose_name="Количество элементов в ряду",
                                    choices=NUMBER_IN_ROW, default=6)

    def __str__(self):
        if self.title:
            return self.title
        return "Блок галереи № " + str(self.id)

    class Meta:
        verbose_name = "Блок галереи "
        verbose_name_plural = "Блок галереи"


class GalleryItem(models.Model):
    """Элемент блока галереи класса `GalleryBlock`"""

    block = models.ForeignKey(
        GalleryBlock, related_name="gallery_items", on_delete=models.CASCADE)
    image = FilerImageField(verbose_name="Изображение",
                            related_name="gallery_images", on_delete=models.CASCADE)
    backing_image = FilerImageField(verbose_name="Дополнительное изображение",
                                    related_name="gallery_backing_images",
                                    null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return ""

    @property
    def has_backing_image(self):
        return self.backing_image is not None

    class Meta:
        verbose_name = "элемент галереи"
        verbose_name_plural = "Элементы галереи"


class Gallery(models.Model):
    """Модель повторителя блоков галереи `GalleryBlock`"""

    content = models.ForeignKey(
        Content, related_name="content_gallery", on_delete=models.CASCADE)
    block = models.OneToOneField(
        GalleryBlock, verbose_name="Галерея", on_delete=models.CASCADE)
    sort = models.IntegerField(verbose_name="Сортировка", default=1)

    def __str__(self):
        return "Галерея № " + str(self.id)

    def render(self):
        return get_template("content/gallery.html").render(
            {
                "gallery": self.block.gallery_items.all(),
                "type": self.block.type_show
            })

    class Meta:
        verbose_name = "галерея"
        verbose_name_plural = "галереи"


class TypalBlock(models.Model):
    content = models.ForeignKey(
        Content, related_name="content_typal_block", on_delete=models.CASCADE)
    sort = models.IntegerField(verbose_name="Сортировка", default=1)
    title = models.CharField(verbose_name="Заголовок",
                             default="", max_length=300)
    text = models.TextField(verbose_name="Текст", default="")
    image = FilerImageField(verbose_name="Изображение", blank=True, null=True,
                            related_name="typal_block_images", on_delete=models.CASCADE)

    def __str__(self):
        return "Типовой блок № " + str(self.id)

    def render(self):
        return get_template("content/typal-block.html").render({"block": self})

    class Meta:
        verbose_name = "типовой блок"
        verbose_name_plural = "Типовые блоки"


class Collapser(models.Model):

    content = models.ForeignKey(
        Content,
        related_name="content_collapser",
        on_delete=models.CASCADE
    )

    title = models.CharField(
        verbose_name="Заголовок",
        default="",
        max_length=300
    )

    text = RichTextUploadingField(
        verbose_name="Текст",
        default=""
    )

    sort = models.IntegerField(
        verbose_name="Сортировка",
        default=1
    )

    def __str__(self):
        return "Схлопывающийся блок " + str(self.title)

    def render(self):
        return get_template("content/collapser.html").render({"collapser": self})

    class Meta:
        verbose_name = "Схлопывающийся блок"
        verbose_name_plural = "Схлопывающиеся блоки"
