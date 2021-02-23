from django.contrib import admin

from news.models import Headline


class HeadlineAdmin(admin.ModelAdmin):
    list_display = ["title", "intern_category", "created_date", "has_image", "image_width"]
    search_fields = ("title", "url", "web")


admin.site.register(Headline, HeadlineAdmin)

