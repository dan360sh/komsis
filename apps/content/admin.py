from django.contrib import admin

from .models import (Content, Text, Quote, Files, FileBlock, File,
                     TitleUnderline, Certificates, CertificatesBlock,
                     Certificate, Gallery, GalleryBlock, GalleryItem,
                     TypalBlock, Collapser)


class TextInline(admin.TabularInline):
    model = Text
    extra = 0


class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 0


class FileInline(admin.TabularInline):
    model = File
    extra = 1


class FileBlockAdmin(admin.ModelAdmin):
    inlines = [FileInline]


class FilesInline(admin.TabularInline):
    model = Files
    extra = 0


class TitleUnderlineInline(admin.TabularInline):
    model = TitleUnderline
    extra = 0


class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 1


class CertificateBlockAdmin(admin.ModelAdmin):
    inlines = [CertificateInline]


class CertificatesInline(admin.TabularInline):
    model = Certificates
    extra = 0


class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 1


class GalleryBlockAdmin(admin.ModelAdmin):
    inlines = [GalleryItemInline]


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 0


class TypalBlockInline(admin.TabularInline):
    model = TypalBlock
    extra = 0


class CollapserInline(admin.TabularInline):
    model = Collapser
    extra = 0


class ContentAdmin(admin.ModelAdmin):
    inlines = [TextInline, QuoteInline, FilesInline, TitleUnderlineInline,
               CertificatesInline, GalleryInline, TypalBlockInline, CollapserInline]


admin.site.register(FileBlock, FileBlockAdmin)
admin.site.register(CertificatesBlock, CertificateBlockAdmin)
admin.site.register(GalleryBlock, GalleryBlockAdmin)
admin.site.register(Content, ContentAdmin)
