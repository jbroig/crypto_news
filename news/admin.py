from django.contrib import admin

from news.models import Headline


class HeadlineAdmin(admin.ModelAdmin):
    list_display = ["title", "image_width", "image_height"]
    search_fields = ("title", "url")


admin.site.register(Headline, HeadlineAdmin)
