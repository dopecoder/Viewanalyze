# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0003_auto_20150719_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='slug',
            field=models.SlugField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='discussiontimeline',
            name='analyser',
            field=models.ForeignKey(to='discussion.Analyser', null=True),
        ),
        migrations.AlterField(
            model_name='discussiontimeline',
            name='discussion',
            field=models.ForeignKey(to='discussion.Discussion'),
        ),
        migrations.AlterField(
            model_name='discussor',
            name='reply_to',
            field=models.ForeignKey(related_name='reply_to', blank=True, to='discussion.DiscussionTimeLine', null=True),
        ),
    ]
