# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0009_auto_20150805_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussor',
            name='reply_to',
            field=models.ForeignKey(related_name='reply_to', blank=True, to='discussion.DiscussionReply', null=True),
        ),
    ]
