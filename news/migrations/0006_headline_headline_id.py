# Generated by Django 3.1.6 on 2021-02-20 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20210220_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='headline',
            name='headline_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
