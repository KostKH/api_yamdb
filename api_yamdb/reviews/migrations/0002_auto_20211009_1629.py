# Generated by Django 2.2.16 on 2021-10-09 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='titles',
            name='description',
            field=models.CharField(default=' ', max_length=200),
        ),
        migrations.AddField(
            model_name='titles',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]