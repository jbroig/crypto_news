# Generated by Django 3.1.6 on 2021-02-23 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_auto_20210222_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='headline',
            name='web',
            field=models.CharField(blank=True, default='Criptonoticias.com', max_length=30, null=True),
        ),
    ]