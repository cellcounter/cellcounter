# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CountInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('session_id', models.CharField(max_length=32)),
                ('ip_address', models.GenericIPAddressField()),
                ('count_total', models.IntegerField()),
                ('user', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
