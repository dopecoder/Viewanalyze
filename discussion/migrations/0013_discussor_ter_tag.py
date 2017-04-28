# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0012_auto_20150807_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussor',
            name='ter_tag',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
