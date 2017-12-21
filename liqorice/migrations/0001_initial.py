# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-21 11:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import liqorice.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.CharField(default=liqorice.models.generateUUID, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=200)),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
