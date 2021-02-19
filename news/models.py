from django.db import models


class Headline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null=True, blank=True)
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    url = models.TextField()
    publish_date = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.title
