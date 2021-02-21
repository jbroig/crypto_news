from django.contrib import admin

from news.models import Headline


class HeadlineAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "created_date", "has_image"]
    search_fields = ("title", "url")


admin.site.register(Headline, HeadlineAdmin)
