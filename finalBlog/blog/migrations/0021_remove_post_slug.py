# Generated by Django 3.1.3 on 2021-02-17 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_post_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]