from django.db import models


class Headline(models.Model):
    headline_id = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200, null=True, blank=True)
    has_image = models.BooleanField(default=False)
    image = models.URLField(null=True, blank=True)
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    url = models.TextField()
    publish_date = models.CharField(max_length=30, null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
