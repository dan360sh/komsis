from django.http import HttpResponse

from apps.configuration.models import Settings


def robots(request):
    settings = Settings.objects.first()
    return HttpResponse(settings.robots_txt, content_type="text/plain")
