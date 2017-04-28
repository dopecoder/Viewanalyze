# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0013_discussor_ter_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyser',
            name='no_achievements',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
