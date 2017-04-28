# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0014_analyser_no_achievements'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='analyser_upvoted',
            field=models.ForeignKey(related_name='upvoted', blank=True, to='discussion.Analyser', null=True),
        ),
    ]
