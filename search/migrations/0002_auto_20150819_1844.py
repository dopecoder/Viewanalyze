# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0022_discussion_isfrompublic'),
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchdata',
            name='user',
        ),
        migrations.AddField(
            model_name='searchdata',
            name='analyser',
            field=models.ForeignKey(to='discussion.Analyser', null=True),
        ),
    ]
