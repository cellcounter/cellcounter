# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc_kapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keyboard',
            old_name='is_primary',
            new_name='is_default',
        ),
        migrations.AddField(
            model_name='keyboard',
            name='mapping_type',
            field=models.CharField(default=b'desktop', max_length=25),
        ),
    ]
