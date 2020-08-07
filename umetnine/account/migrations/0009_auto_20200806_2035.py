# Generated by Django 3.0.8 on 2020-08-06 18:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20200730_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserArtwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(default='unknown', max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('year', models.IntegerField(validators=[django.core.validators.MaxValueValidator(2020)])),
                ('technique', models.CharField(default='unspecified', max_length=100)),
                ('medium', models.CharField(default='unspecified', max_length=100)),
                ('style', models.CharField(default='unspecified', max_length=100)),
                ('genre', models.CharField(default='unspecified', max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]