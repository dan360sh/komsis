from django.contrib import admin
from .models import Email, Subscriber, LoggingEmail


class LoggingEmailAdmin(admin.ModelAdmin):
    readonly_fields = ("date", "ok", "to", "subject",
                       "result", "exception_body")
    search_fields = ("subject", "to")
    list_filter = ("ok", )
    list_display = ("subject", "to", "ok", "date")

    fields = ("date", "ok", "to", "subject",
              "result", "exception_body")


admin.site.register(Email)
admin.site.register(Subscriber)
admin.site.register(LoggingEmail, LoggingEmailAdmin)
