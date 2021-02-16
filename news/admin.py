from django.contrib import admin

from news.models import Headline


class HeadlineAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ("title", "url")


admin.site.register(Headline, HeadlineAdmin)
