# Generated by Django 3.1.6 on 2021-02-21 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_headline_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='headline',
            name='has_image',
            field=models.BooleanField(default=False),
        ),
    ]
