# Generated by Django 2.1.4 on 2019-03-06 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theatre', '0002_auto_20190306_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_actors',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_age_rating',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_directors',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_duration_mins',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_genre',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_language',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_producers',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_release_date',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_writers',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]