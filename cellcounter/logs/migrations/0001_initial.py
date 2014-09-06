# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remote_addr', models.CharField(max_length=200)),
                ('remote_user', models.CharField(max_length=200)),
                ('time_local', models.DateTimeField(max_length=200)),
                ('request', models.CharField(max_length=200)),
                ('request_path', models.CharField(max_length=200)),
                ('status', models.IntegerField(default=0)),
                ('body_bytes_sent', models.IntegerField(default=0)),
                ('http_referrer', models.CharField(max_length=200)),
                ('http_user_agent', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
