# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0004_auto_20150720_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussor',
            name='slug',
            field=models.SlugField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='slug',
            field=models.SlugField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='discussiontimeline',
            name='analyser',
            field=models.ForeignKey(blank=True, to='discussion.Analyser', null=True),
        ),
    ]
